from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    head_user = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name


class MapMarker(models.Model):
    MARKER_TYPES = [
        ('facility', 'Facility'),
        ('room', 'Room'),
        ('entrance', 'Entrance'),
        ('waypoint', 'Waypoint'),
        ('amenity', 'Amenity'),
    ]
    
    facility = models.ForeignKey('facilities.Facility', on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey('rooms.Room', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    x_position = models.FloatField()
    y_position = models.FloatField()
    marker_type = models.CharField(max_length=20, choices=MARKER_TYPES, default='facility')
    icon_name = models.CharField(max_length=100, default='location_on')
    color_hex = models.CharField(max_length=7, default='#FF9800')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'map_markers'

    def __str__(self):
        return self.name


class MapLabel(models.Model):
    label_text = models.CharField(max_length=200)
    x_position = models.FloatField()
    y_position = models.FloatField()
    font_size = models.IntegerField(default=14)
    color_hex = models.CharField(max_length=7, default='#000000')
    rotation = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'map_labels'

    def __str__(self):
        return self.label_text


class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=100, default='notifications')
    color_hex = models.CharField(max_length=7, default='#FF9800')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_types'

    def __str__(self):
        return self.name


class NotificationPreference(models.Model):
    user = models.ForeignKey('users.AdminUser', on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_preferences'
        unique_together = ['user', 'notification_type']

    def __str__(self):
        return f"{self.user.username} - {self.notification_type.name}"


class AdminAuditLog(models.Model):
    ACTION_CHOICES = [
        ('login',          'Login'),
        ('logout',         'Logout'),
        ('create',         'Create'),
        ('update',         'Update'),
        ('soft_delete',    'Soft Delete'),
        ('restore',        'Restore'),
        ('approve',        'Approve'),
        ('reject',         'Reject'),
        ('publish',        'Publish'),
        ('reset_password', 'Reset Password'),
    ]

    admin         = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL,
        null=True, related_name='audit_entries'
    )
    action        = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type   = models.CharField(max_length=50, blank=True, null=True)
    entity_id     = models.IntegerField(blank=True, null=True)
    entity_label  = models.CharField(max_length=200, blank=True, null=True)
    old_value_json= models.TextField(blank=True, null=True)
    new_value_json= models.TextField(blank=True, null=True)
    ip_address    = models.CharField(max_length=50, blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_audit_log'
        ordering = ['-created_at']


class SearchHistory(models.Model):
    user = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=500)
    results_count = models.IntegerField(default=0)
    was_clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"Search: {self.query}"


class AppConfig(models.Model):
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.TextField()
    description = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_config'

    def __str__(self):
        return self.config_key
