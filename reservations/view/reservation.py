from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers import ReservationSerializer
from ..models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Reservation.objects.filter(salle__admin=user)

        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
