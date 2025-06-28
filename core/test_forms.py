import pytest
from decimal import Decimal
from core.forms import TransacaoForm, CategoriaForm
from core.models import Categoria

@pytest.mark.django_db
class TestForms:
    def test_transacao_form_valido(self, user, categoria):
        form_data = {
            'data': '2024-03-20',
            'tipo': 'receita',
            'valor': '100.00',
            'categoria': categoria.id,
            'observacoes': 'Teste'
        }
        form = TransacaoForm(data=form_data, user=user)
        assert form.is_valid()

    def test_transacao_form_invalido(self, user, categoria):
        form_data = {
            'data': '2024-03-20',
            'tipo': 'receita',
            'valor': '-100.00',  # Valor negativo
            'categoria': categoria.id,
            'observacoes': 'Teste'
        }
        form = TransacaoForm(data=form_data, user=user)
        assert not form.is_valid()
        assert 'valor' in form.errors

    def test_categoria_form_valido(self, user):
        form_data = {
            'nome': 'Nova Categoria',
            'tipo': 'receita',
            'cor': '#FFFFFF'
        }
        form = CategoriaForm(data=form_data, user=user)
        assert form.is_valid()

    def test_categoria_form_invalido(self, user):
        form_data = {
            'nome': '',  # Nome vazio
            'tipo': 'receita',
            'cor': '#FFFFFF'
        }
        form = CategoriaForm(data=form_data, user=user)
        assert not form.is_valid()
        assert 'nome' in form.errors

    def test_categoria_form_tipo_invalido(self, user):
        form_data = {
            'nome': 'Nova Categoria',
            'tipo': 'invalido',  # Tipo inválido
            'cor': '#FFFFFF'
        }
        form = CategoriaForm(data=form_data, user=user)
        assert not form.is_valid()
        assert 'tipo' in form.errors

    def test_categoria_form_cor_invalida(self, user):
        form_data = {
            'nome': 'Nova Categoria',
            'tipo': 'receita',
            'cor': 'invalido'  # Cor inválida
        }
        form = CategoriaForm(data=form_data, user=user)
        assert not form.is_valid()
        assert 'cor' in form.errors 