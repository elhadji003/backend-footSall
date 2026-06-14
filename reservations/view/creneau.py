from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from ..models import Creneau
from ..serializers import CreneauSerializer

class CreneauViewSet(viewsets.ModelViewSet):
    serializer_class = CreneauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        # 1. Le Super-Admin voit ABSOLUMENT TOUS les créneaux
        if user.is_authenticated and user.is_superuser:
            return Creneau.objects.all()

        # 2. Un Admin (staff) ne voit que les créneaux des salles qu'il gère
        if user.is_authenticated and user.is_staff:
            return Creneau.objects.filter(salle__admin=user)

        # 3. Les clients / utilisateurs anonymes ne voient que les créneaux actifs
        return Creneau.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        salle = serializer.validated_data["salle"]

        # Si l'utilisateur est super-admin, il contourne la vérification
        if user.is_superuser:
            serializer.save()
            return

        # Si c'est un admin normal, on vérifie qu'il possède bien cette salle
        if salle.admin != user:
            # Levée d'une exception DRF propre (renverra un code HTTP 403)
            raise PermissionDenied("Tu n'as pas l'autorisation de gérer les créneaux de cette salle.")

        serializer.save()