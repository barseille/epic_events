from rest_framework import serializers
from .models import User, Client, Contrat, Event


# Serializer pour le modèle User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # Valide le champ 'role' pour s'assurer qu'il est présent
    def validate_role(self, value):
        if not value:
            raise serializers.ValidationError("Le champ rôle est obligatoire.")
        return value


# Serializer pour le modèle Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


# Serializer pour le modèle Contrat
class ContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = '__all__'


# Serializer pour le modèle Event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
