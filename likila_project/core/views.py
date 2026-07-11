from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Event, Service, GalleryPhoto, Inquiry, SiteSetting
from .serializers import (
    EventSerializer, ServiceSerializer, GalleryPhotoSerializer,
    InquirySerializer, SiteSettingSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminUser

User = get_user_model()


# ── AUTH ─────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email    = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=401)

        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=401)

        if not user.is_staff:
            return Response({'error': 'Admin access required'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'token':   str(refresh.access_token),
            'refresh': str(refresh),
            'admin': {
                'id':    user.id,
                'email': user.email,
                'name':  user.get_full_name() or user.username,
            }
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({'id': u.id, 'email': u.email, 'name': u.get_full_name() or u.username})

    def put(self, request):
        u = request.user
        u.first_name = request.data.get('first_name', u.first_name)
        u.last_name  = request.data.get('last_name',  u.last_name)
        u.email      = request.data.get('email', u.email)
        u.save()
        return Response({'message': 'Profile updated'})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        current = request.data.get('current_password', '')
        new     = request.data.get('new_password', '')
        if not current or not new:
            return Response({'error': 'Both passwords required'}, status=400)
        if len(new) < 8:
            return Response({'error': 'New password must be at least 8 characters'}, status=400)
        if not request.user.check_password(current):
            return Response({'error': 'Current password is incorrect'}, status=401)
        request.user.set_password(new)
        request.user.save()
        return Response({'message': 'Password updated successfully'})


# ── DASHBOARD ────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard(request):
    stats = {
        'total_events':    Event.objects.count(),
        'upcoming_events': Event.objects.filter(status__in=['upcoming', 'active']).count(),
        'total_services':  Service.objects.filter(status='active').count(),
        'total_gallery':   GalleryPhoto.objects.count(),
        'total_inquiries': Inquiry.objects.count(),
        'unread_inquiries':Inquiry.objects.filter(is_read=False).count(),
    }
    recent_events = EventSerializer(
        Event.objects.order_by('date')[:5], many=True
    ).data
    recent_inquiries = InquirySerializer(
        Inquiry.objects.order_by('-created_at')[:5], many=True
    ).data
    return Response({
        'stats': stats,
        'recent_events': recent_events,
        'recent_inquiries': recent_inquiries,
    })


# ── EVENTS ───────────────────────────────────────────────────────────────────

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Event.objects.all()
        # Public requests only see live events
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            qs = qs.filter(status__in=['upcoming', 'active'])

        status_f = self.request.query_params.get('status')
        search   = self.request.query_params.get('search')
        if status_f:
            qs = qs.filter(status=status_f)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def set_status(self, request, pk=None):
        event = self.get_object()
        new_status = request.data.get('status')
        valid = [c[0] for c in Event.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'error': f'Status must be one of {valid}'}, status=400)
        event.status = new_status
        event.save()
        return Response(EventSerializer(event).data)


# ── SERVICES ─────────────────────────────────────────────────────────────────

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Service.objects.all()
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            qs = qs.filter(status='active')
        status_f = self.request.query_params.get('status')
        if status_f:
            qs = qs.filter(status=status_f)
        return qs

    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser])
    def reorder(self, request):
        """Bulk reorder: send [{"id": 1, "sort_order": 0}, ...]"""
        for item in request.data:
            Service.objects.filter(pk=item['id']).update(sort_order=item['sort_order'])
        return Response({'message': 'Order saved'})


# ── GALLERY ──────────────────────────────────────────────────────────────────

class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryPhotoSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = GalleryPhoto.objects.all()
        category = self.request.query_params.get('category')
        year     = self.request.query_params.get('year')
        limit    = self.request.query_params.get('limit')
        if category:
            qs = qs.filter(category__icontains=category)
        if year:
            qs = qs.filter(year=year)
        if limit:
            qs = qs[:int(limit)]
        return qs

    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser])
    def reorder(self, request):
        for item in request.data:
            GalleryPhoto.objects.filter(pk=item['id']).update(sort_order=item['sort_order'])
        return Response({'message': 'Order saved'})


# ── INQUIRIES ────────────────────────────────────────────────────────────────

class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer

    def get_permissions(self):
        # Anyone can POST (submit from website); only admins can GET/DELETE
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Inquiry.objects.all()
        is_read = self.request.query_params.get('is_read')
        search  = self.request.query_params.get('search')
        if is_read is not None:
            qs = qs.filter(is_read=is_read == '1' or is_read == 'true')
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) |
                Q(email__icontains=search)       | Q(message__icontains=search)
            )
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        inquiry = self.get_object()
        inquiry.is_read = True
        inquiry.save()
        return Response({'message': 'Marked as read'})

    @action(detail=False, methods=['patch'])
    def mark_all_read(self, request):
        Inquiry.objects.filter(is_read=False).update(is_read=True)
        return Response({'message': 'All marked as read'})


# ── SETTINGS ─────────────────────────────────────────────────────────────────

PUBLIC_KEYS = [
    'business_name', 'tagline', 'location', 'email',
    'whatsapp', 'facebook', 'stat_travellers',
    'stat_destinations', 'stat_countries', 'stat_years',
]

SETTING_DEFAULTS = {
    'business_name':    'Likila Travel & Tours',
    'tagline':          'Your Destination is Our Concern',
    'location':         'Botha-Buthe, Lesotho',
    'email':            'info@likilatours.co.ls',
    'whatsapp':         '',
    'facebook':         '',
    'stat_travellers':  '2000+',
    'stat_destinations':'50+',
    'stat_countries':   '5+',
    'stat_years':       '9+',
}


@api_view(['GET'])
@permission_classes([AllowAny])
def public_settings(request):
    result = {}
    for key in PUBLIC_KEYS:
        obj = SiteSetting.objects.filter(key=key).first()
        result[key] = obj.value if obj else SETTING_DEFAULTS.get(key, '')
    return Response(result)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def admin_settings(request):
    if request.method == 'GET':
        settings_qs = SiteSetting.objects.all()
        result = dict(SETTING_DEFAULTS)
        for s in settings_qs:
            result[s.key] = s.value
        return Response(result)

    # PUT — bulk upsert
    for key, value in request.data.items():
        SiteSetting.objects.update_or_create(key=key, defaults={'value': str(value)})
    return Response({'message': 'Settings saved'})


# ── FRONTEND PAGES ───────────────────────────────────────────────────────────
from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')
def gallery_page(request):
    photos = GalleryPhoto.objects.all().order_by('sort_order', '-id')
    categories = photos.values_list('category', flat=True).distinct().exclude(category='')
    return render(request, 'gallery.html', {'photos': photos, 'categories': categories})
