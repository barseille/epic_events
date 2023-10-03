import pytest
from rest_framework.test import APIClient
from EpicEvents.models import User, Client, Contrat, Event
from django.urls import reverse
import datetime


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_user(api_client, commercial_user):
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(reverse('user-list'), {
        'username': 'test_user',
        'email': 'test@gmail.com',
        'password': 'testpassword',
        'role': 'COMMERCIAL'
    })
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_client(api_client, commercial_user):
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(reverse('client-list'), {
        'name': 'Client Test',
        'email': 'client@gmail.com',
        'phone': '1234567890',
        'company_name': 'Test Company',
        'commercial_contact': commercial_user.id
    })
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_contrat(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    client_obj = Client.objects.create(
        name='Client Test',
        email='client@gmail.com',
        commercial_contact=admin_user
    )
    response = api_client.post(reverse('contrat-list'), {
        'client': client_obj.id,
        'status': 'EN_COURS',
        'start_date': '2023-10-01',
        'end_date': '2023-10-02',
        'price': 1000,
        'payment_received': 'OUI',
        'is_signed': True,
        'contrat_author': admin_user.id
    })
    print(response.data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_event(api_client, commercial_user):
    api_client.force_authenticate(user=commercial_user)
    
    # Créer un client et un contrat signé
    client_obj = Client.objects.create(
        name='Client Test',
        email='client@gmail.com',
        commercial_contact=commercial_user
    )
    contrat_obj = Contrat.objects.create(
        client=client_obj,
        status='EN_COURS',
        start_date='2023-10-01',
        end_date='2023-10-02',
        price=1000,
        payment_received='OUI',
        is_signed=True,
        contrat_author=commercial_user
    )
    
    # Tenter de créer un événement
    response = api_client.post(reverse('event-list'), {
        'contrat': contrat_obj.id,
        'start_date': '2023-10-03',
        'end_date': '2023-10-04',
        'attendees': 10,
        'notes': 'Some notes'
    })
    
    assert response.status_code == 201
    assert Event.objects.count() == 1
    event = Event.objects.first()
    assert event.contrat.id == contrat_obj.id
    assert event.start_date == datetime.date(2023, 10, 3)
    assert event.end_date == datetime.date(2023, 10, 4)
    assert event.attendees == 10
    assert event.notes == 'Some notes'
