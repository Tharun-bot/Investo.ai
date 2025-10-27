from rest_framework import serializers
from .models import Stock, StockData, Signal, Portfolio, Position

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'

class SignalSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source='stock.symbol', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    
    class Meta:
        model = Signal
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source='stock.symbol', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    profit_loss = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Position
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
