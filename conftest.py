import pytest
from django.contrib.auth.models import User
from core.models import Categoria

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def categoria(db, user):
    return Categoria.objects.create(
        nome='Teste',
        tipo='receita',
        cor='#000000',
        usuario=user
    ) 