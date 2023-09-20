from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Liste des rôles utilisateur disponibles.
USER_ROLES = [
    ('COMMERCIAL', 'Commercial'),
    ('ADMINISTRATION', 'Administration'),
    ('SUPPORT', 'Support'),
]

CONTRAT_STATUTS = [
    ('EN_COURS', 'En cours'),
    ('TERMINE', 'Terminé'),
    ('ANNULE', 'Annulé'),
]

PAYMENT_STATUS = [
    ('OUI', 'Oui'),
    ('NON', 'Non'),
]

class User(AbstractUser):
    role = models.CharField(max_length=15, choices=USER_ROLES, null=False, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    last_update_date = models.DateTimeField(auto_now=True)
    commercial_contact = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)


class Contrat(models.Model):
    client = models.ForeignKey(Client, related_name='contrats', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=CONTRAT_STATUTS)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()
    payment_received = models.CharField(max_length=3, choices=PAYMENT_STATUS)
    is_signed = models.BooleanField(default=False, verbose_name="Signed")

class Event(models.Model):
    contrat = models.ForeignKey(Contrat, related_name='events', on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    attendees = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
