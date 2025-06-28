from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('receita', 'Receita'), ('despesa', 'Despesa')])
    cor = models.CharField(max_length=7, default='#000000')  # Código hexadecimal da cor

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('receita', 'Receita'), ('despesa', 'Despesa')])
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-data_criacao']

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.valor} - {self.data}"

    def save(self, *args, **kwargs):
        # Garante que o tipo da transação corresponda ao tipo da categoria
        if self.tipo != self.categoria.tipo:
            self.tipo = self.categoria.tipo
        super().save(*args, **kwargs)
