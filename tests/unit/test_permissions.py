import pytest
from rest_framework.test import APIClient
from EpicEvents.permissions import IsCommercial, IsAdministration, IsSupport
from EpicEvents.models import User


@pytest.mark.django_db
def test_IsCommercial_permission():

    # Arrange : Crée une instance de APIClient
    client = APIClient()
    user = User.objects.create(username='commercial_user', role='COMMERCIAL')
    
    # Utilise force_authenticate sur l'instance de APIClient
    client.force_authenticate(user=user)

    # Utilise une URL existante qui utilise la permission IsCommercial
    response = client.get('/api/clients/')
    permission = IsCommercial()

    # Act :Utilise response.wsgi_request pour obtenir la requête WSGI
    has_permission = permission.has_permission(response.wsgi_request, None)

    # Assert
    assert has_permission is True


@pytest.mark.django_db
def test_IsAdministration_permission():
    # Arrange
    client = APIClient()
    user = User.objects.create(username='admin_user', role='ADMINISTRATION')
    client.force_authenticate(user=user)

    # Utilise une URL existante qui utilise la permission IsAdministration
    response = client.get('/api/contrats/')
    permission = IsAdministration()

    # Act
    has_permission = permission.has_permission(response.wsgi_request, None)

    # Assert
    assert has_permission is True

 
@pytest.mark.django_db
def test_IsSupport_permission():
    # Arrange
    client = APIClient()
    user = User.objects.create(username='support_user', role='SUPPORT')
    client.force_authenticate(user=user)

    # Utilise une URL existante qui utilise la permission IsSupport
    response = client.get('/api/events/')
    permission = IsSupport()

    # Act
    has_permission = permission.has_permission(response.wsgi_request, None)

    # Assert
    assert has_permission is True
