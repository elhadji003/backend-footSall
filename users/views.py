from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers.profile_user import ProfileUserSerializer
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .serializers.user import UserSerializer


# ----- Listes des Users -----
User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    """Configuration de la pagination par défaut"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class GetUsersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # 1. Récupération de tous les utilisateurs (triés par date d'inscription ou ID)
            users = User.objects.all().order_by('-id')
            
            # 2. Optionnel: Ajout d'un filtre de recherche simple (ex: /api/users/?search=john)
            search_query = request.query_params.get('search', None)
            if search_query:
                users = users.filter(
                    first_name=search_query
                ) | users.filter(
                    email__icontains=search_query
                )
            
            # 3. Application de la pagination
            paginator = StandardResultsSetPagination()
            paginated_users = paginator.paginate_queryset(users, request, view=self)
            
            # 4. Sérialisation des données
            serializer = UserSerializer(paginated_users, many=True)
            
            # 5. Retour des résultats paginés
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": f"Une erreur est survenue lors de la récupération : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
# ----- Recupérer le Profile du User ----
class GetProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileUserSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

# ----- Recupérer le Profile du User Par ID -----
class GetProfileUserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = request.user.__class__.objects.get(id=user_id)
        except request.user.__class__.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileUserSerializer(
            user,
            context={"request": request}
        )
        return Response(serializer.data)

# ----- Modifier le Profile du User -----
class UpdateProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ProfileUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----- Supprimer le Compte du User -----
class DeleteAccountWithPwd(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        password = request.data.get("password")

        if not password:
            return Response(
                {"error": "Mot de passe requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            email=request.user.email,
            password=password
        )

        if not user:
            return Response(
                {"error": "Mot de passe incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.user.delete()
        return Response(
            {"message": "Compte supprimé définitivement"},
            status=status.HTTP_200_OK
        )
    