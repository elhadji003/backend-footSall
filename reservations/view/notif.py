from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers import NotificationSerializer
from ..models import Notification

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
