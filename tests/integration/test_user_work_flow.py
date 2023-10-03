from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from EpicEvents.models import Client
from rest_framework import status


class UserWorkflowTest(APITestCase):
    """
    Classe de test pour simuler le workflow d'un utilisateur avec le rôle commercial.
    Ce test couvre l'authentification, la création d'un client, et la vérification de ce client.
    """
    
    def setUp(self):
        """
        Configuration initiale du test.
        Crée un utilisateur avec le rôle commercial et génère un token d'authentification JWT.
        Initialise également les données pour un nouveau client.
        """
        self.user = get_user_model().objects.create_user(
            username='commercial_user',
            password='pass',
            email='commercial@example.com',
            role='COMMERCIAL'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.client_data = {
            'name': 'Test Client',
            'email': 'testclient@example.com',
            'phone': '1234567890',
            'company_name': 'Test Company',
            'commercial_contact': self.user.id
        }

    def test_user_workflow(self):
        """
        Teste le workflow complet d'un utilisateur commercial.
        - Authentification
        - Création d'un client
        - Vérification que le client a bien été créé
        """
        # Création d'un client
        response = self.client.post('/api/clients/', self.client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Récupère l'ID du client créé
        client_id = response.data['id']

        # Vérification que le client a bien été créé
        response = self.client.get(f'/api/clients/{client_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Client')
