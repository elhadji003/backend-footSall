# reservations/serializers.py
from rest_framework import serializers
from ..models import Salle, Creneau, Reservation
from .creneau import CreneauSerializer
from django.conf import settings

User = settings.AUTH_USER_MODEL


class SalleSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    creneaux = serializers.SerializerMethodField()

    class Meta:
        model = Salle
        fields = [
            "id",
            "admin",
            "nom",
            "adresse",
            "telephone",
            "latitude",
            "longitude",
            "prix",
            "created_at",
            'creneaux',
        ]
        
    def get_creneaux(self, obj):
        creneaux = (
            Creneau.objects
            .filter(salle=obj, is_active=True)
            .order_by("date", "heure_debut")
        )
        return CreneauSerializer(creneaux, many=True).data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["admin"] = request.user
        return super().create(validated_data)
