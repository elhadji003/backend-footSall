from rest_framework import serializers
from ..models import Creneau

class CreneauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creneau
        fields = [
            "id",
            "salle",
            "date",
            "heure_debut",
            "heure_fin",
            "is_active",
        ]
