from django.urls import path
from . import views

urlpatterns = [
    path('carteira/', views.portfolio_list, name='portfolio_list'),
    path('carteira/adicionar/', views.portfolio_add, name='portfolio_add'),
    path('carteira/<int:pk>/excluir/', views.portfolio_delete, name='portfolio_delete'),
]
