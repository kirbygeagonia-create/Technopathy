from rest_framework import generics, permissions
from .models import FAQEntry, AIChatLog
from .serializers import FAQEntrySerializer, AIChatLogSerializer
from apps.users.permissions import ReadOnlyOrSuperAdmin


class FAQListView(generics.ListCreateAPIView):
    queryset = FAQEntry.objects.filter(is_deleted=False)
    serializer_class = FAQEntrySerializer
    permission_classes = [ReadOnlyOrSuperAdmin]


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQEntry.objects.filter(is_deleted=False)
    serializer_class = FAQEntrySerializer
    permission_classes = [ReadOnlyOrSuperAdmin]

