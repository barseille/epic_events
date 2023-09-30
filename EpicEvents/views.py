from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, Contrat, Event ,User 
from .serializers import ClientSerializer, ContratSerializer, EventSerializer, UserSerializer
from .permissions import IsCommercial, IsAdministration, IsSupport
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """ 
    Créer un utilisateur avec le bon rôle
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = get_user_model().objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                role=serializer.validated_data['role'] 
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)      
    
class ClientViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour gérer les opérations CRUD sur les objets 'Client'.
    Les permissions sont définies pour permettre uniquement aux utilisateurs 
    avec le rôle 'Commercial' d'accéder aux ressources.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action effectuée.
        """
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsCommercial]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsCommercial]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsCommercial]
        elif self.action == 'delete':
            self.permission_classes = [IsAuthenticated, IsCommercial]
        return [permission() for permission in self.permission_classes]

class ContratViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour gérer les opérations CRUD sur les objets 'Contrat'.
    Les permissions sont définies pour permettre uniquement aux utilisateurs avec le rôle 'Administration' d'accéder aux ressources.
    """

    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer
    
    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action effectuée.
        """
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsAdministration]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdministration]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdministration]
        elif self.action == 'delete':
            self.permission_classes = [IsAuthenticated, IsAdministration]
        return [permission() for permission in self.permission_classes]



class EventViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour gérer les opérations CRUD sur les objets 'Event'.
    Les permissions sont définies pour permettre uniquement aux utilisateurs avec le rôle 'Support' d'accéder aux ressources.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action effectuée.
        """
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsSupport]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsSupport]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsSupport]
        elif self.action == 'delete':
            self.permission_classes = [IsAuthenticated, IsSupport]
        return [permission() for permission in self.permission_classes]

    
    def create(self, request, *args, **kwargs):
        # Récupérer l'ID du contrat depuis les données de la requête
        contrat_id = request.data.get('contrat')

        # Vérifier si un événement pour ce contrat existe déjà
        existing_event = Event.objects.filter(contrat_id=contrat_id).first()
        if existing_event:
            return Response({"error": "Un événement pour ce contrat existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si le contrat existe et est signé
        try:
            contrat = Contrat.objects.get(id=contrat_id)
            
            # Vérifier si le contrat est signé
            if not contrat.is_signed:
                return Response({"error": "Le contrat doit être signé avant de créer un événement."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Nouvelle condition : Vérifier si le paiement a été reçu
            if contrat.payment_received != 'OUI':
                return Response({"error": "Le paiement doit être reçu avant de créer un événement."}, status=status.HTTP_400_BAD_REQUEST)
                
        except Contrat.DoesNotExist:
            return Response({"error": "Contrat non trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        # Si tout est bon, procéder à la création de l'événement
        return super(EventViewSet, self).create(request, *args, **kwargs)

