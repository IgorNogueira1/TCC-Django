import pytest
from django.contrib.auth.models import User
from core.models import Categoria

@pytest.mark.django_db
class TestSignals:
    def test_criar_categorias_padrao(self):
        # Criar um novo usuário
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Verificar se as categorias padrão foram criadas
        categorias = Categoria.objects.filter(usuario=user)
        assert categorias.count() == 10  # 3 receitas + 7 despesas

        # Verificar categorias de receita
        receitas = categorias.filter(tipo='receita')
        assert receitas.count() == 3
        assert receitas.filter(nome='Salário').exists()
        assert receitas.filter(nome='Investimentos').exists()
        assert receitas.filter(nome='Outros').exists()

        # Verificar categorias de despesa
        despesas = categorias.filter(tipo='despesa')
        assert despesas.count() == 7
        assert despesas.filter(nome='Alimentação').exists()
        assert despesas.filter(nome='Transporte').exists()
        assert despesas.filter(nome='Moradia').exists()
        assert despesas.filter(nome='Saúde').exists()
        assert despesas.filter(nome='Educação').exists()
        assert despesas.filter(nome='Lazer').exists()
        assert despesas.filter(nome='Outros').exists()

    def test_nao_criar_categorias_padrao_para_usuario_existente(self, user):
        # Verificar que não foram criadas novas categorias
        categorias_antes = Categoria.objects.filter(usuario=user).count()
        
        # Atualizar o usuário
        user.first_name = 'Test'
        user.save()

        # Verificar que o número de categorias não mudou
        categorias_depois = Categoria.objects.filter(usuario=user).count()
        assert categorias_antes == categorias_depois 