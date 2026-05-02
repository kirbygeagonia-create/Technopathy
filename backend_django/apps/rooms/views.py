from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from apps.users.permissions import CanManageRoom
from apps.facilities.models import Facility


class RoomListView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [CanManageRoom]

    def get_queryset(self):
        qs = Room.objects.select_related('facility').filter(is_deleted=False)
        q = self.request.query_params.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(room_number__icontains=q) |
                Q(facility__name__icontains=q)
            )
        return qs.order_by('facility__name', 'name')

    def perform_create(self, serializer):
        """
        On POST, validate that non-super-admin users can only create rooms
        in facilities belonging to their department.
        """
        user = self.request.user
        if user.role != 'super_admin':
            facility_id = self.request.data.get('facility')
            if facility_id:
                try:
                    facility = Facility.objects.get(pk=facility_id)
                    if facility.department and facility.department.code != user.department:
                        from rest_framework.exceptions import PermissionDenied
                        raise PermissionDenied(
                            'You can only add rooms to facilities in your department.'
                        )
                except Facility.DoesNotExist:
                    pass  # Let serializer validation handle invalid FK
        serializer.save()


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.filter(is_deleted=False)
    serializer_class = RoomSerializer
    permission_classes = [CanManageRoom]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

