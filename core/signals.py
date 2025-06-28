from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Categoria

@receiver(post_save, sender=User)
def criar_categorias_padrao(sender, instance, created, **kwargs):
    if created:
        # Categorias de receita
        Categoria.objects.create(
            nome='Salário',
            tipo='receita',
            cor='#10B981',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Investimentos',
            tipo='receita',
            cor='#3B82F6',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Outros',
            tipo='receita',
            cor='#6366F1',
            usuario=instance
        )

        # Categorias de despesa
        Categoria.objects.create(
            nome='Alimentação',
            tipo='despesa',
            cor='#EF4444',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Transporte',
            tipo='despesa',
            cor='#F59E0B',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Moradia',
            tipo='despesa',
            cor='#EC4899',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Saúde',
            tipo='despesa',
            cor='#8B5CF6',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Educação',
            tipo='despesa',
            cor='#14B8A6',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Lazer',
            tipo='despesa',
            cor='#F97316',
            usuario=instance
        )
        Categoria.objects.create(
            nome='Outros',
            tipo='despesa',
            cor='#6B7280',
            usuario=instance
        ) 