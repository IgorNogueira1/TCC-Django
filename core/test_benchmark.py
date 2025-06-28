import pytest
from decimal import Decimal
from core.models import Categoria, Transacao
from django.db import models

@pytest.mark.django_db
class TestBenchmark:
    def test_criar_categorias_padrao_benchmark(self, benchmark, user):
        def criar_categorias():
            # Categorias de receita
            Categoria.objects.create(
                nome='Salário',
                tipo='receita',
                cor='#10B981',
                usuario=user
            )
            Categoria.objects.create(
                nome='Investimentos',
                tipo='receita',
                cor='#3B82F6',
                usuario=user
            )
            Categoria.objects.create(
                nome='Outros',
                tipo='receita',
                cor='#6366F1',
                usuario=user
            )

            # Categorias de despesa
            Categoria.objects.create(
                nome='Alimentação',
                tipo='despesa',
                cor='#EF4444',
                usuario=user
            )
            Categoria.objects.create(
                nome='Transporte',
                tipo='despesa',
                cor='#F59E0B',
                usuario=user
            )
            Categoria.objects.create(
                nome='Moradia',
                tipo='despesa',
                cor='#EC4899',
                usuario=user
            )
            Categoria.objects.create(
                nome='Saúde',
                tipo='despesa',
                cor='#8B5CF6',
                usuario=user
            )
            Categoria.objects.create(
                nome='Educação',
                tipo='despesa',
                cor='#14B8A6',
                usuario=user
            )
            Categoria.objects.create(
                nome='Lazer',
                tipo='despesa',
                cor='#F97316',
                usuario=user
            )
            Categoria.objects.create(
                nome='Outros',
                tipo='despesa',
                cor='#6B7280',
                usuario=user
            )

        benchmark(criar_categorias)

    def test_calcular_saldo_benchmark(self, benchmark, user, categoria):
        # Criar algumas transações
        for i in range(100):
            Transacao.objects.create(
                data='2024-03-20',
                tipo='receita' if i % 2 == 0 else 'despesa',
                valor=Decimal('100.00'),
                categoria=categoria,
                usuario=user
            )

        def calcular_saldo():
            receitas = Transacao.objects.filter(
                usuario=user,
                tipo='receita'
            ).aggregate(total=models.Sum('valor'))['total'] or Decimal('0.00')

            despesas = Transacao.objects.filter(
                usuario=user,
                tipo='despesa'
            ).aggregate(total=models.Sum('valor'))['total'] or Decimal('0.00')

            return receitas - despesas

        result = benchmark(calcular_saldo)
        assert result == Decimal('0.00')  # 50 receitas - 50 despesas 