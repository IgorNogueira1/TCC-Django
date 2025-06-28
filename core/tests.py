from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Transacao
from decimal import Decimal

class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Criar uma categoria de teste
        self.categoria = Categoria.objects.create(
            nome='Teste',
            tipo='receita',
            cor='#000000',
            usuario=self.user
        )

    def test_criar_transacao(self):
        response = self.client.post(reverse('transacao_create'), {
            'data': '2024-03-20',
            'tipo': 'receita',
            'valor': '100.00',
            'categoria': self.categoria.id,
            'observacoes': 'Teste'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transacao.objects.filter(usuario=self.user).exists())

    def test_editar_transacao(self):
        transacao = Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=self.categoria,
            usuario=self.user
        )
        response = self.client.post(
            reverse('transacao_update', args=[transacao.id]),
            {
                'data': '2024-03-21',
                'tipo': 'receita',
                'valor': '200.00',
                'categoria': self.categoria.id,
                'observacoes': 'Teste atualizado'
            }
        )
        self.assertEqual(response.status_code, 302)
        transacao.refresh_from_db()
        self.assertEqual(transacao.valor, Decimal('200.00'))

    def test_excluir_transacao(self):
        transacao = Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=self.categoria,
            usuario=self.user
        )
        response = self.client.post(reverse('transacao_delete', args=[transacao.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transacao.objects.filter(id=transacao.id).exists())

    def test_criar_categoria(self):
        response = self.client.post(reverse('categoria_create'), {
            'nome': 'Nova Categoria',
            'tipo': 'receita',
            'cor': '#FFFFFF'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nome='Nova Categoria').exists())

    def test_editar_categoria(self):
        response = self.client.post(
            reverse('categoria_update', args=[self.categoria.id]),
            {
                'nome': 'Categoria Atualizada',
                'tipo': 'receita',
                'cor': '#FFFFFF'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nome, 'Categoria Atualizada')

    def test_excluir_categoria(self):
        response = self.client.post(reverse('categoria_delete', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())

    def test_dashboard(self):
        # Criar algumas transações
        Transacao.objects.create(
            data='2024-03-20',
            tipo='receita',
            valor=Decimal('100.00'),
            categoria=self.categoria,
            usuario=self.user
        )
        Transacao.objects.create(
            data='2024-03-20',
            tipo='despesa',
            valor=Decimal('50.00'),
            categoria=self.categoria,
            usuario=self.user
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'R$ 100,00')
        self.assertContains(response, 'R$ 50,00')
        self.assertContains(response, 'R$ 50,00')  # Saldo
