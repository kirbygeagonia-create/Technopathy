from django.db.models import Q
from rest_framework import generics, permissions
from .models import Facility
from .serializers import FacilitySerializer
from apps.users.permissions import ReadOnlyOrSuperAdmin


class FacilityListView(generics.ListCreateAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [ReadOnlyOrSuperAdmin]

    def get_queryset(self):
        qs = Facility.objects.filter(is_deleted=False)
        q = self.request.query_params.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(floor__icontains=q) |
                Q(building__icontains=q)
            )
        return qs.order_by('name')


class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.filter(is_deleted=False)
    serializer_class = FacilitySerializer
    permission_classes = [ReadOnlyOrSuperAdmin]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

