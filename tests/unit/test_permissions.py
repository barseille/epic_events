import pytest
from rest_framework.test import APIClient 
from EpicEvents.permissions import IsCommercial, IsAdministration, IsSupport
from EpicEvents.models import User  

@pytest.mark.django_db
def test_IsCommercial_permission():
    # Arrange
    client = APIClient()  # Crée une instance de APIClient
    user = User.objects.create(username='commercial_user', role='COMMERCIAL')
    client.force_authenticate(user=user)  # Utilise force_authenticate sur l'instance de APIClient

    response = client.get('/api/clients/')  # Utilise une URL existante qui utilise la permission IsCommercial
    permission = IsCommercial()

    # Act
    has_permission = permission.has_permission(response.wsgi_request, None)  # Utilise response.wsgi_request pour obtenir la requête WSGI

    # Assert
    assert has_permission == True

@pytest.mark.django_db
def test_IsAdministration_permission():
    # Arrange
    client = APIClient()
    user = User.objects.create(username='admin_user', role='ADMINISTRATION')
    client.force_authenticate(user=user)

    response = client.get('/api/contrats/')  # Utilise une URL existante qui utilise la permission IsAdministration
    permission = IsAdministration()

    # Act
    has_permission = permission.has_permission(response.wsgi_request, None)

    # Assert
    assert has_permission == True
    
@pytest.mark.django_db
def test_IsSupport_permission():
    # Arrange
    client = APIClient()
    user = User.objects.create(username='support_user', role='SUPPORT')
    client.force_authenticate(user=user)

    response = client.get('/api/events/')  # Utilise une URL existante qui utilise la permission IsSupport
    permission = IsSupport()

    # Act
    has_permission = permission.has_permission(response.wsgi_request, None)

    # Assert
    assert has_permission == True

