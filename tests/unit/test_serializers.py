import pytest
from EpicEvents.serializers import UserSerializer
from EpicEvents.models import User


@pytest.mark.django_db
def test_valid_user_serializer():
    # Arrange
    user = User.objects.create(username='test_user', role='COMMERCIAL')
    serializer = UserSerializer(instance=user)

    # Act
    serialized_data = serializer.data

    # Assert
    assert serialized_data['username'] == 'test_user'
    assert serialized_data['role'] == 'COMMERCIAL'


@pytest.mark.django_db
def test_invalid_user_serializer_missing_role():
    # Arrange
    invalid_data = {
        'username': 'test_user',
    }
    serializer = UserSerializer(data=invalid_data)

    # Act
    is_valid = serializer.is_valid()

    # Assert
    assert not is_valid
    assert 'role' in serializer.errors
