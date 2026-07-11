from django.contrib import admin
from .models import Event, Service, GalleryPhoto, Inquiry, SiteSetting


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['name', 'date', 'price', 'deposit', 'departure', 'status', 'created_at']
    list_filter   = ['status', 'date']
    search_fields = ['name', 'description', 'departure']
    list_editable = ['status']
    ordering      = ['date']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'date', 'status', 'departure')}),
        ('Pricing',    {'fields': ('price', 'deposit')}),
        ('Details',    {'fields': ('description', 'included', 'excluded')}),
        ('Image',      {'fields': ('image', 'image_url')}),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'icon', 'price', 'status', 'sort_order']
    list_editable = ['status', 'sort_order']
    list_filter   = ['status', 'icon']
    search_fields = ['name', 'description']
    ordering      = ['sort_order']


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display  = ['caption', 'category', 'year', 'sort_order', 'created_at']
    list_editable = ['sort_order']
    list_filter   = ['category', 'year']
    search_fields = ['caption', 'category']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'email', 'service', 'is_read', 'created_at']
    list_filter   = ['is_read', 'service']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    ordering      = ['-created_at']
    actions       = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'updated_at']
    search_fields = ['key']
