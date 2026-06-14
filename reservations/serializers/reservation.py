from rest_framework import serializers
from ..models import Notification, Reservation
from .creneau import CreneauSerializer 

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    creneau_details = CreneauSerializer(source="creneau", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "salle",
            "creneau",
            "creneau_details",
            "status",
            "created_at",
        ]
        # On garde status en read_only pour les clients, 
        # mais attention : si l'admin doit le changer via ce ViewSet, 
        # il faudra le gérer dans le ViewSet ou enlever read_only ici.
        read_only_fields = ["status"]

    def validate(self, data):
        # 1. Utiliser .get() pour éviter le KeyError si le champ est absent (ex: en PATCH)
        creneau = data.get("creneau")

        # 2. On n'applique les règles de blocage QUE si un créneau est fourni
        if creneau:
            if not creneau.is_active:
                raise serializers.ValidationError("Ce créneau n'est plus disponible.")

            # Blocage double réservation
            if Reservation.objects.filter(creneau=creneau).exists():
                raise serializers.ValidationError("Ce créneau est déjà réservé.")

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user

        reservation = super().create(validated_data)

        # Désactiver le créneau
        reservation.creneau.is_active = False
        reservation.creneau.save()

        # Notification admin
        Notification.objects.create(
            user=reservation.salle.admin,
            message=f"Nouvelle réservation pour {reservation.salle.nom}"
        )

        return reservation  