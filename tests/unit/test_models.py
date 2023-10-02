import pytest
from EpicEvents.models import User, Client, Contrat, Event


@pytest.mark.django_db
def test_create_user():
    """
    Teste la création d'un utilisateur.
    """
    # Arrange
    username = "testuser"
    role = "COMMERCIAL"
    email = "test@example.com"

    # Act
    user = User.objects.create(username=username, role=role, email=email)

    # Assert
    assert user.username == username
    assert user.role == role
    assert user.email == email

  
@pytest.mark.django_db
def test_create_client():
    """
    Teste la création d'un client.
    """
    # Arrange
    username = "commercial"
    role = "COMMERCIAL"
    email = "commercial@example.com"
    client_name = "client"
    client_email = "client@example.com"

    # Act
    user = User.objects.create(username=username, role=role, email=email)
    client = Client.objects.create(name=client_name, email=client_email, commercial_contact=user)

    # Assert
    assert client.name == client_name
    assert client.email == client_email
    assert client.commercial_contact == user


@pytest.mark.django_db
def test_create_contrat():
    """
    Teste la création d'un contrat.
    """
    # Arrange : On prépare les données nécessaires pour le test
    commercial_user = User.objects.create(username="commercial", role="COMMERCIAL", email="commercial@example.com")
    client = Client.objects.create(name="client", email="client@example.com", commercial_contact=commercial_user)

    # Act : On effectue l'action à tester
    contrat = Contrat.objects.create(
        client=client,
        status="EN_COURS",
        start_date="2023-01-01",
        end_date="2023-12-31",
        price=1000,
        payment_received="OUI",
        is_signed=True,
        contrat_author=commercial_user
    )

    # Assert : On vérifie que le résultat est celui attendu
    assert contrat.client == client
    assert contrat.status == "EN_COURS"
    assert contrat.start_date == "2023-01-01"
    assert contrat.end_date == "2023-12-31"
    assert contrat.price == 1000
    assert contrat.payment_received == "OUI"
    assert contrat.is_signed == True
    
    
@pytest.mark.django_db
def test_create_event():
    """
    Teste la création d'un événement.
    """
    # Arrange
    commercial_user = User.objects.create(username="commercial", role="COMMERCIAL", email="commercial@example.com")
    client = Client.objects.create(name="client", email="client@example.com", commercial_contact=commercial_user)  
    contrat = Contrat.objects.create(
        client=client,  
        status="EN_COURS",
        start_date="2023-01-01",
        end_date="2023-12-31",
        price=1000,
        payment_received="OUI",
        is_signed=True,
        contrat_author=commercial_user 
    )
    start_date = "2023-10-03"
    end_date = "2023-10-04"
    attendees = 50
    notes = "test de création d'un événement"

    # Act
    event = Event.objects.create(
        contrat=contrat,
        start_date=start_date,
        end_date=end_date,
        attendees=attendees,
        notes=notes
    )

    # Assert
    assert event.contrat == contrat
    assert event.start_date == start_date
    assert event.end_date == end_date
    assert event.attendees == attendees
    assert event.notes == notes
