from django.db import models
from users.models.user import User
from .salle import Salle
from .creneau import Creneau

class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    creneau = models.ForeignKey(
        Creneau,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ("pending", "En attente"),
        ("confirmed", "Confirmée"),
        ("cancelled", "Annulée"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"{self.user} - {self.salle.nom}"
