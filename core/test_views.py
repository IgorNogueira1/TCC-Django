import pytest
from django.urls import reverse
from decimal import Decimal
from core.models import Transacao

@pytest.mark.django_db
class TestViews:
    def test_dashboard_view(self, client, user, categoria):
        client.force_login(user)
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200
        assert 'Saldo Atual' in response.content.decode()

    def test_transacao_list_view(self, client, user, categoria):
        client.force_login(user)
        response = client.get(reverse('transacao_list'))
        assert response.status_code == 200
        assert 'Transações' in response.content.decode()

    def test_transacao_create_view(self, client, user, categoria):
        client.force_login(user)
        response = client.post(reverse('transacao_create'), {
            'data': '2024-03-20',
            'tipo': 'receita',
            'valor': '100.00',
            'categoria': categoria.id,
            'observacoes': 'Teste'
        })
        assert response.status_code == 302
        assert Transacao.objects.filter(usuario=user).exists()

    def test_transacao_update_view(self, client, user, categoria):
        client.force_login(user)
        transacao = Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=categoria,
            usuario=user
        )
        response = client.post(
            reverse('transacao_update', args=[transacao.id]),
            {
                'data': '2024-03-21',
                'tipo': 'receita',
                'valor': '200.00',
                'categoria': categoria.id,
                'observacoes': 'Teste atualizado'
            }
        )
        assert response.status_code == 302
        transacao.refresh_from_db()
        assert transacao.valor == Decimal('200.00')

    def test_transacao_delete_view(self, client, user, categoria):
        client.force_login(user)
        transacao = Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=categoria,
            usuario=user
        )
        response = client.post(reverse('transacao_delete', args=[transacao.id]))
        assert response.status_code == 302
        assert not Transacao.objects.filter(id=transacao.id).exists()

    def test_categoria_list_view(self, client, user):
        client.force_login(user)
        response = client.get(reverse('categoria_list'))
        assert response.status_code == 200
        assert 'Categorias' in response.content.decode()

    def test_categoria_create_view(self, client, user):
        client.force_login(user)
        response = client.post(reverse('categoria_create'), {
            'nome': 'Nova Categoria',
            'tipo': 'receita',
            'cor': '#FFFFFF'
        })
        assert response.status_code == 302
        assert user.categoria_set.filter(nome='Nova Categoria').exists()

    def test_categoria_update_view(self, client, user, categoria):
        client.force_login(user)
        response = client.post(
            reverse('categoria_update', args=[categoria.id]),
            {
                'nome': 'Categoria Atualizada',
                'tipo': 'receita',
                'cor': '#FFFFFF'
            }
        )
        assert response.status_code == 302
        categoria.refresh_from_db()
        assert categoria.nome == 'Categoria Atualizada'

    def test_categoria_delete_view(self, client, user, categoria):
        client.force_login(user)
        response = client.post(reverse('categoria_delete', args=[categoria.id]))
        assert response.status_code == 302
        assert not user.categoria_set.filter(id=categoria.id).exists() 