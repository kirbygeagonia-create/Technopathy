from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer
from apps.users.permissions import IsAnyAdmin, IsSuperAdmin


class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        """GET requires admin auth; POST is open for anyone to submit feedback."""
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAnyAdmin()]
        return []  # Anyone can POST feedback

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsSuperAdmin]

