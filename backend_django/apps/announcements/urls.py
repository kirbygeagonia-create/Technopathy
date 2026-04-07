from django.urls import path
from .views import (AnnouncementPublicListView, AnnouncementCreateView,
                    AnnouncementDetailView, AnnouncementApproveView,
                    AnnouncementRejectView, PendingApprovalsView, MyAnnouncementsView,
                    AnnouncementArchiveView)

urlpatterns = [
    path('',                  AnnouncementPublicListView.as_view()),   # GET public
    path('create/',           AnnouncementCreateView.as_view()),        # POST admin
    path('<int:pk>/',         AnnouncementDetailView.as_view()),        # PUT/DELETE
    path('<int:pk>/approve/', AnnouncementApproveView.as_view()),
    path('<int:pk>/reject/',  AnnouncementRejectView.as_view()),
    path('<int:pk>/archive/', AnnouncementArchiveView.as_view()),
    path('pending/',          PendingApprovalsView.as_view()),
    path('mine/',             MyAnnouncementsView.as_view()),
]
