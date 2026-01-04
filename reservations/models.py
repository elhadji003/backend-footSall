# reservations/models.py
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Salle(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="salles"
    )

    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    # localisation (pour map / trajectoire)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    prix = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

