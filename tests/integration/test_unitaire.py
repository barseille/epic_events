from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status


class UserWorkflowTest(APITestCase):
    """
    Classe de test pour simuler le workflow d'un utilisateur avec le rôle commercial.
    Ce test couvre l'authentification, la création d'un client, et la modification de ce client.
    """
    
    def setUp(self):
        """
        Configuration initiale du test.
        Crée un utilisateur avec le rôle commercial et génère un token d'authentification.
        """
        self.user = get_user_model().objects.create_user(username='commercial_user',
                                                         password='pass',
                                                         email='commercial@example.com',
                                                         role='COMMERCIAL')

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """
        Authentifie l'utilisateur pour les requêtes API.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_user_workflow(self):
        """
        Teste le workflow complet d'un utilisateur commercial.
        - Authentification
        - Création d'un client
        - Modification du client
        """
        # Simule l'authentification de l'utilisateur
        self.client.login(username='commercial_user', password='pass')

        # Création d'un client
        data = {'name': 'Client Test',
                'email': 'client@test.com',
                'phone': '1234567890',
                'company_name': 'Test Company'}

        response = self.client.post('/api/clients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Récupère l'ID du client créé
        client_id = response.data['id']

        # Modification du client
        data = {'phone': '0987654321'}
        response = self.client.put(f'/api/clients/{client_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
