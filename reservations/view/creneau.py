from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers import CreneauSerializer
from ..models import Creneau

class CreneauViewSet(viewsets.ModelViewSet):
    serializer_class = CreneauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            return Creneau.objects.filter(salle__admin=user)

        return Creneau.objects.filter(is_active=True)

    def perform_create(self, serializer):
        salle = serializer.validated_data["salle"]

        if salle.admin != self.request.user:
            raise PermissionError("Tu ne peux pas gérer cette salle")

        serializer.save()
