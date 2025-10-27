from django.contrib import admin
from .models import Stock, StockData, Signal, Portfolio, Position

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'sector', 'created_at']
    search_fields = ['symbol', 'name']
    list_filter = ['sector', 'created_at']

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ['stock', 'signal_type', 'confidence', 'price_at_signal', 'created_at']
    list_filter = ['signal_type', 'created_at', 'is_active']
    search_fields = ['stock__symbol', 'stock__name']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_value', 'cash_balance', 'updated_at']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'stock', 'quantity', 'average_price', 'current_price']
