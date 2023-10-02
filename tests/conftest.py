import pytest
from EpicEvents.models import User 

@pytest.fixture
def commercial_user(db):
    return User.objects.create(username="commercial", role="COMMERCIAL", email="commercial@example.com")

@pytest.fixture
def admin_user(db):
    return User.objects.create(username="admin", role="ADMINISTRATION", email="admin@example.com")

@pytest.fixture
def support_user(db):
    return User.objects.create(username="support", role="SUPPORT", email="support@example.com")
