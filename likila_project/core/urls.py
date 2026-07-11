from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'events',    views.EventViewSet,    basename='event')
router.register(r'services',  views.ServiceViewSet,  basename='service')
router.register(r'gallery',   views.GalleryViewSet,  basename='gallery')
router.register(r'inquiries', views.InquiryViewSet,  basename='inquiry')

urlpatterns = [
    # Auth
    path('auth/login/',           views.LoginView.as_view(),          name='login'),
    path('auth/refresh/',         TokenRefreshView.as_view(),         name='token_refresh'),
    path('auth/me/',              views.MeView.as_view(),             name='me'),
    path('auth/password/',        views.ChangePasswordView.as_view(), name='change_password'),

    # Dashboard
    path('dashboard/',            views.dashboard,                    name='dashboard'),

    # Settings
    path('settings/public/',      views.public_settings,              name='public_settings'),
    path('settings/',             views.admin_settings,               name='admin_settings'),

    # ViewSets
    path('', include(router.urls)),
]
