from django.contrib import admin
from .models import Salle, Creneau, Reservation, Notification

# Register your models here.
@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nom",
        "admin",
        "adresse",
        "telephone",
        "prix",
        "created_at",
    )

    list_filter = ("created_at",)
    search_fields = ("nom", "adresse", "telephone")

@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "salle",
        "nombre_joueur",
        "date",
        "heure_debut",
        "heure_fin",
        "is_active",
    )

    list_filter = ("date", "is_active")
    search_fields = ("salle__nom",)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "salle",
        "creneau",
        "created_at",
    )

    list_filter = ("created_at",)
    search_fields = ("user__username", "salle__nom")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "message",
        "is_read",
        "created_at",
    )

    list_filter = ("is_read", "created_at")
    search_fields = ("user__username", "message")
