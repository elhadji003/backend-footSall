from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

class DeleteUserView(APIView):
    # Sécurité : Seul un admin connecté peut supprimer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def delete(self, request, pk):
        try:
            # 1. Récupère l'utilisateur à supprimer ou renvoie une erreur 404 s'il n'existe pas
            user_to_delete = get_object_or_404(User, pk=pk)
            
            # 2. Sécurité supplémentaire : Empêcher un admin de se supprimer lui-même
            if user_to_delete == request.user:
                return Response(
                    {"error": "Vous ne pouvez pas supprimer votre propre compte administrateur."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 3. Suppression de l'utilisateur
            user_to_delete.delete()
            
            # 4. Retourne un message de succès (Statut 200 OK ou 204 NO CONTENT)
            return Response(
                {"message": "L'utilisateur a été supprimé avec succès."},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Une erreur est survenue lors de la suppression : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )