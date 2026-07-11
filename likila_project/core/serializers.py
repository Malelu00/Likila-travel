from rest_framework import serializers
from .models import Event, Service, GalleryPhoto, Inquiry, SiteSetting


class EventSerializer(serializers.ModelSerializer):
    display_image = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class GalleryPhotoSerializer(serializers.ModelSerializer):
    display_url = serializers.ReadOnlyField()

    class Meta:
        model = GalleryPhoto
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['is_read', 'created_at']


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ['key', 'value', 'updated_at']


class BulkSettingSerializer(serializers.Serializer):
    """Accept any key-value pairs for bulk settings update."""
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError('Expected a JSON object.')
        return data
