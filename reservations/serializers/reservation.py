from rest_framework import serializers
from ..models import Notification, Reservation
from .creneau import CreneauSerializer
from .salle import SalleSerializer

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # Correction de ready_only -> read_only et source (salles -> salle selon tes fields ?)
    salle_details = SalleSerializer(source="salle", read_only=True)
    creneau_details = CreneauSerializer(source="creneau", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "salle",
            "creneau",
            "salle_details",
            "creneau_details",
            "status",
            "created_at",
        ]

    def validate(self, data):
        creneau = data.get("creneau")

        if creneau:
            if not creneau.is_active:
                raise serializers.ValidationError("Ce créneau n'est plus disponible.")

            # Correction : On exclut la réservation actuelle si c'est une modification
            query = Reservation.objects.filter(creneau=creneau)
            if self.instance:
                query = query.exclude(pk=self.instance.pk)
                
            if query.exists():
                raise serializers.ValidationError("Ce créneau est déjà réservé.")

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user

        reservation = super().create(validated_data)

        # Désactiver le créneau
        if reservation.creneau:
            reservation.creneau.is_active = False
            reservation.creneau.status = "Confirmée"
            reservation.creneau.save()

        # Notification admin
        if reservation.salle and hasattr(reservation.salle, "admin"):
            Notification.objects.create(
                user=reservation.salle.admin,
                message=f"Nouvelle réservation pour {reservation.salle.nom}"
            )

        return reservation  
    
    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)

        # Si annulation → remettre le créneau disponible
        if new_status == "cancelled" and instance.status != "cancelled":
            if instance.creneau:
                instance.creneau.is_active = True
                instance.creneau.status = "Disponible"
                instance.creneau.save()

        return super().update(instance, validated_data)