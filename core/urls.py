from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('perfil/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs para Transações
    path('transacoes/', views.transacao_list, name='transacao_list'),
    path('transacoes/nova/', views.transacao_create, name='transacao_create'),
    path('transacoes/<int:pk>/editar/', views.transacao_edit, name='transacao_edit'),
    path('transacoes/<int:pk>/excluir/', views.transacao_delete, name='transacao_delete'),
    
    # URLs para Categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),

    # URLs para Carteiras de Investimento
    path('carteiras/', views.carteira_list, name='carteira_list'),
    path('carteiras/nova/', views.carteira_create, name='carteira_create'),
    path('carteiras/<int:pk>/', views.carteira_detail, name='carteira_detail'),
    path('carteiras/<int:pk>/editar/', views.carteira_edit, name='carteira_edit'),
    path('carteiras/<int:pk>/excluir/', views.carteira_delete, name='carteira_delete'),
    path('carteiras/<int:carteira_pk>/investimentos/novo/', views.investimento_add, name='investimento_add'),
    path('carteiras/<int:carteira_pk>/investimentos/<int:pk>/excluir/', views.investimento_delete, name='investimento_delete'),
    
    #teste
    path('dashboard/exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('dashboard/exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
] 