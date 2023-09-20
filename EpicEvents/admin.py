from django.contrib import admin
from .models import User, Client, Contrat, Event  # Importe tous les modèles

# Enregistre les modèles pour qu'ils apparaissent dans l'admin
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Contrat)
admin.site.register(Event)
