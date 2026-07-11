from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', core_views.index_page, name='home'),
    path('gallery/', core_views.gallery_page, name='gallery_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
