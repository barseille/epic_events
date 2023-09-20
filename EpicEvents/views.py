from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, Contrat, Event , User 
from .serializers import ClientSerializer, ContratSerializer, EventSerializer, UserSerializer
from .permissions import IsCommercial, IsAdministration, IsSupport

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
            self.permission_classes = [IsAuthenticated, IsCommercial]
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