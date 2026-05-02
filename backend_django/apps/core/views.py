from rest_framework import generics, permissions, filters, status as http_status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.permissions import ReadOnlyOrSuperAdmin, CanViewAuditLog
from .models import (
    Department, MapMarker, MapLabel,
    NotificationType, NotificationPreference, AdminAuditLog,
    SearchHistory, AppConfig
)
from .serializers import (
    DepartmentSerializer, MapMarkerSerializer, MapLabelSerializer,
    NotificationTypeSerializer,
    NotificationPreferenceSerializer, AdminAuditLogSerializer,
    SearchHistorySerializer, AppConfigSerializer
)


class AppRatingView(APIView):
    """Public endpoint for app ratings submitted from HomeView."""
    permission_classes = [AllowAny]

    def post(self, request):
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
            return Response({'error': 'rating must be an integer 1–5'},
                            status=http_status.HTTP_400_BAD_REQUEST)
        # Store as a Feedback entry so it appears in the admin Feedback panel
        from apps.feedback.models import Feedback
        Feedback.objects.create(
            rating=rating,
            comment=comment,
            category='general',
        )
        return Response({'message': 'Rating submitted. Thank you!'}, status=http_status.HTTP_201_CREATED)


# Department Views
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Map Marker Views
class MapMarkerListCreateView(generics.ListCreateAPIView):
    queryset = MapMarker.objects.filter(is_active=True)
    serializer_class = MapMarkerSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['marker_type', 'facility']
    search_fields = ['name']


class MapMarkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MapMarker.objects.all()
    serializer_class = MapMarkerSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


# Map Label Views
class MapLabelListCreateView(generics.ListCreateAPIView):
    queryset = MapLabel.objects.filter(is_active=True)
    serializer_class = MapLabelSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


class MapLabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MapLabel.objects.all()
    serializer_class = MapLabelSerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


# Notification Type Views
class NotificationTypeListCreateView(generics.ListCreateAPIView):
    queryset = NotificationType.objects.filter(is_active=True)
    serializer_class = NotificationTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NotificationTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
    permission_classes = [IsAuthenticated]


# Notification Preference Views
class NotificationPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)


class NotificationPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]


# Admin Audit Log Views
class AdminAuditLogListView(generics.ListAPIView):
    queryset = AdminAuditLog.objects.all()
    serializer_class = AdminAuditLogSerializer
    permission_classes = [CanViewAuditLog]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action', 'entity_type', 'user']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# Search History Views
class SearchHistoryListCreateView(generics.ListCreateAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()



# App Config Views
class AppConfigListCreateView(generics.ListCreateAPIView):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AppConfigDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'config_key'


# Dashboard Stats
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Returns a snapshot of key system stats for the admin dashboard homepage."""
    from apps.facilities.models import Facility
    from apps.rooms.models import Room
    from apps.announcements.models import Announcement
    from apps.feedback.models import Feedback
    from apps.notifications.models import Notification
    from django.db.models import Avg

    return Response({
        'facilities':     Facility.objects.count(),
        'rooms':          Room.objects.count(),
        'announcements':  Announcement.objects.filter(is_archived=False).count(),
        'feedback': {
            'total':      Feedback.objects.count(),
            'flagged':    Feedback.objects.filter(is_flagged=True).count(),
            'avg_rating': Feedback.objects.aggregate(avg=Avg('rating'))['avg'],
        },
        'notifications': {
            'total':      Notification.objects.count(),
            'unread':     Notification.objects.filter(is_read=False).count(),
        },
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Lightweight health check for Render, uptime monitors, and frontend PWA."""
    from django.db import connection
    db_ok = False
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        pass

    return Response({
        'status':    'ok' if db_ok else 'degraded',
        'database':  'connected' if db_ok else 'error',
        'timestamp': timezone.now().isoformat(),
        'version':   '1.0.0',
    }, status=200 if db_ok else 503)
