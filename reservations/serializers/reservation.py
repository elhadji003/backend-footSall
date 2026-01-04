from rest_framework import serializers
from ..models import Notification
from ..models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "salle",
            "creneau",
            "status",
            "created_at",
        ]
        read_only_fields = ["status"]

    def validate(self, data):
        creneau = data["creneau"]

        if not creneau.is_active:
            raise serializers.ValidationError(
                "Ce créneau n'est plus disponible."
            )

        # blocage double réservation
        if Reservation.objects.filter(creneau=creneau).exists():
            raise serializers.ValidationError(
                "Ce créneau est déjà réservé."
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user

        reservation = super().create(validated_data)

        # désactiver le créneau
        reservation.creneau.is_active = False
        reservation.creneau.save()

        # notification admin
        Notification.objects.create(
            user=reservation.salle.admin,
            message=f"Nouvelle réservation pour {reservation.salle.nom}"
        )

        return reservation
