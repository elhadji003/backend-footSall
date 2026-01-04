from django.db import models
from .salle import Salle    

class Creneau(models.Model):
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name="creneaux"
    )

    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.salle.nom} - {self.date} {self.heure_debut}"
