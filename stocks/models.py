from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='data')
    date = models.DateTimeField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['stock', 'date']
        ordering = ['-date']

class Signal(models.Model):
    SIGNAL_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('HOLD', 'Hold'),
    ]
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='signals')
    signal_type = models.CharField(max_length=4, choices=SIGNAL_CHOICES)
    confidence = models.FloatField()
    price_at_signal = models.DecimalField(max_digits=10, decimal_places=2)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason = models.TextField()
    technical_score = models.FloatField(default=0)
    fundamental_score = models.FloatField(default=0)
    ml_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='positions')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_value(self):
        return self.quantity * self.current_price

    @property
    def profit_loss(self):
        return (self.current_price - self.average_price) * self.quantity
