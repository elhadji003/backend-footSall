from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q # 👈 AJOUTE CET IMPORT
from ..serializers import ReservationSerializer
from ..models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        
        # Sécurité si l'utilisateur n'est pas connecté (AnonymousUser)
        if not user or user.is_anonymous:
            return Reservation.objects.none()

        # Si c'est un admin/staff, il voit ses réservations PERSO + celles de ses salles gérées
        if user.is_staff:
            return Reservation.objects.filter(Q(user=user) | Q(salle__admin=user)).distinct()

        # Pour un utilisateur classique, uniquement ses réservations
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)