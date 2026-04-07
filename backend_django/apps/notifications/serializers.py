from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_is_read(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if hasattr(obj, 'is_read_by_user'):
            return obj.is_read_by_user
        return obj.notificationreadstatus_set.filter(user=request.user).exists()
