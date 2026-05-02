from django.db import models
from apps.facilities.models import Facility

class Room(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    floor = models.IntegerField(default=1)
    map_svg_id = models.CharField(max_length=100, blank=True, null=True, help_text='SVG element ID e.g. RST-F1-CL1')
    room_type = models.CharField(max_length=50, default='classroom',
        choices=[('classroom','Classroom'),('office','Office'),('lab','Laboratory'),
                 ('facility','Facility'),('staircase','Staircase'),('restroom','Restroom'),('other','Other')])
    capacity = models.IntegerField(default=30)
    is_office = models.BooleanField(default=False)
    is_crucial = models.BooleanField(default=False)
    search_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Room occupancy/availability status
    STATUS_CHOICES = [
        ('available',    'Available'),
        ('occupied',     'Occupied'),
        ('maintenance',  'Under Maintenance'),
        ('restricted',   'Restricted Access'),
        ('closed',       'Closed'),
    ]
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    status_note = models.CharField(max_length=200, blank=True, help_text='Optional note about current status.')
    status_updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return f'{self.facility.code} - {self.name} (Floor {self.floor})'
