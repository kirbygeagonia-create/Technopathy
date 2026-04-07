from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from apps.users.permissions import CanManageRoom
from apps.facilities.models import Facility


class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.filter(is_deleted=False)
    serializer_class = RoomSerializer
    permission_classes = [CanManageRoom]

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

