from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Feedback
from .serializers import FeedbackSerializer
from apps.users.permissions import IsAnyAdmin, IsSuperAdmin


class FeedbackPagination(PageNumberPagination):
    page_size             = 20
    page_size_query_param = 'page_size'
    max_page_size         = 100


class FeedbackListView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    pagination_class = FeedbackPagination

    def get_permissions(self):
        """GET requires admin auth; POST is open for anyone to submit feedback."""
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAnyAdmin()]
        return []  # Anyone can POST feedback

    def get_queryset(self):
        qs = Feedback.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        flagged  = self.request.query_params.get('flagged')
        if category:
            qs = qs.filter(category=category)
        if flagged == 'true':
            qs = qs.filter(is_flagged=True)
        return qs

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsSuperAdmin]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feedback_analytics(request):
    """
    Returns a summary of feedback for the admin dashboard.
    Query params:
      days (int, default 30) — how many days back to look
    """
    try:
        days = max(1, min(int(request.query_params.get('days', 30)), 365))
    except (TypeError, ValueError):
        days = 30

    since = timezone.now() - timedelta(days=days)
    qs    = Feedback.objects.filter(created_at__gte=since)

    # Overall stats
    total      = qs.count()
    avg_rating = qs.filter(rating__isnull=False).aggregate(avg=Avg('rating'))['avg']
    flagged    = qs.filter(is_flagged=True).count()

    # Breakdown by category
    by_category = list(
        qs.values('category')
          .annotate(count=Count('id'), avg_rating=Avg('rating'))
          .order_by('-count')
    )

    # Daily submission trend
    daily_trend = list(
        qs.annotate(day=TruncDate('created_at'))
          .values('day')
          .annotate(count=Count('id'))
          .order_by('day')
    )

    # Rating distribution (1–5 stars)
    rating_dist = {}
    for r in range(1, 6):
        rating_dist[str(r)] = qs.filter(rating=r).count()

    return Response({
        'period_days':   days,
        'total':         total,
        'avg_rating':    round(avg_rating, 2) if avg_rating else None,
        'flagged':       flagged,
        'by_category':  by_category,
        'daily_trend':  [{'date': str(d['day']), 'count': d['count']} for d in daily_trend],
        'rating_dist':  rating_dist,
    })

