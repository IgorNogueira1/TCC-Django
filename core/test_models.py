import pytest
from decimal import Decimal
from core.models import Categoria, Transacao
from django.db import models

@pytest.mark.django_db
class TestModels:
    def test_criar_categoria(self, user):
        categoria = Categoria.objects.create(
            nome='Teste',
            tipo='receita',
            cor='#000000',
            usuario=user
        )
        assert categoria.nome == 'Teste'
        assert categoria.tipo == 'receita'
        assert categoria.cor == '#000000'
        assert categoria.usuario == user

    def test_criar_transacao(self, user, categoria):
        transacao = Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=categoria,
            usuario=user,
            observacoes='Teste'
        )
        assert transacao.data.strftime('%Y-%m-%d') == '2024-03-20'
        assert transacao.tipo == 'receita'
        assert transacao.valor == Decimal('100.00')
        assert transacao.categoria == categoria
        assert transacao.usuario == user
        assert transacao.observacoes == 'Teste'

    def test_calcular_saldo(self, user, categoria):
        # Criar receitas
        Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=categoria,
            usuario=user
        )
        Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('50.00'),
            categoria=categoria,
            usuario=user
        )

        # Criar despesas
        Transacao.objects.create(
            data='2024-03-20',
            tipo='despesa',
            valor=Decimal('30.00'),
            categoria=categoria,
            usuario=user
        )
        Transacao.objects.create(
            data='2024-03-20',
            tipo='despesa',
            valor=Decimal('20.00'),
            categoria=categoria,
            usuario=user
        )

        # Calcular saldo
        receitas = Transacao.objects.filter(
            usuario=user,
            tipo='receita'
        ).aggregate(total=models.Sum('valor'))['total'] or Decimal('0.00')

        despesas = Transacao.objects.filter(
            usuario=user,
            tipo='despesa'
        ).aggregate(total=models.Sum('valor'))['total'] or Decimal('0.00')

        saldo = receitas - despesas

        assert saldo == Decimal('100.00') 