from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Admin peut créer/modifier
    User peut seulement lire
    """

    def has_permission(self, request, view):
        if request.method in ["GET"]:
            return True
        return request.user.is_authenticated and request.user.is_staff
