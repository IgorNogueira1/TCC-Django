from django.contrib import admin
from .models import Transacao, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario')
    list_filter = ('tipo', 'usuario')
    search_fields = ('nome',)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipo', 'valor', 'categoria', 'usuario')
    list_filter = ('tipo', 'categoria', 'usuario', 'data')
    search_fields = ('observacoes',)
    date_hierarchy = 'data'
