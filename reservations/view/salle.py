# reservations/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Salle, Creneau, Reservation, Notification
from ..serializers import (
    SalleSerializer,
    ReservationSerializer,
    NotificationSerializer,
    CreneauSerializer,
    
)
from ..permissions import IsAdminOrReadOnly


class SalleViewSet(viewsets.ModelViewSet):
    serializer_class = SalleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            # admin → ses salles
            return Salle.objects.filter(admin=user)

        # user → toutes les salles
        return Salle.objects.all()
