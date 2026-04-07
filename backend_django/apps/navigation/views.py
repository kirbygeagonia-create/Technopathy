from rest_framework import generics, permissions
from .models import NavigationNode, NavigationEdge
from .serializers import NavigationNodeSerializer, NavigationEdgeSerializer
from apps.users.permissions import ReadOnlyOrSuperAdmin


class NavigationNodeListView(generics.ListCreateAPIView):
    queryset = NavigationNode.objects.filter(is_deleted=False)
    serializer_class = NavigationNodeSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


class NavigationNodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NavigationNode.objects.filter(is_deleted=False)
    serializer_class = NavigationNodeSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


class NavigationEdgeListView(generics.ListCreateAPIView):
    queryset = NavigationEdge.objects.filter(is_deleted=False)
    serializer_class = NavigationEdgeSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


class NavigationEdgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NavigationEdge.objects.filter(is_deleted=False)
    serializer_class = NavigationEdgeSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]

