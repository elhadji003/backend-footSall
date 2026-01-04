from rest_framework.routers import DefaultRouter
from .view import (
    SalleViewSet,
    CreneauViewSet,
    ReservationViewSet,
    NotificationViewSet,
)

router = DefaultRouter()
router.register("salles", SalleViewSet, basename="salle")
router.register("creneaux", CreneauViewSet, basename="creneau")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("notifications", NotificationViewSet, basename="notification")

urlpatterns = router.urls
