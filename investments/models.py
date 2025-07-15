from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    STOCK = 'stock'
    FII = 'fii'
    ASSET_TYPES = [
        (STOCK, 'Ação'),
        (FII, 'Fundo Imobiliário'),
    ]

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, unique=True)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class PortfolioItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'asset')

    def __str__(self):
        return f"{self.asset.symbol} ({self.quantity})"
