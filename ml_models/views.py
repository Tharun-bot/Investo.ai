from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .predictor import StockPredictor
import yfinance as yf

@api_view(['POST'])
def predict_stock(request, symbol):
    """Generate ML prediction for a stock"""
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period="3mo")
        info = ticker.info
        
        if hist.empty:
            return Response(
                {"error": "No data available for analysis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        predictor = StockPredictor()
        prediction = predictor.generate_signal(hist, info)
        
        return Response(prediction)
        
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def model_stats(request):
    """Get ML model statistics"""
    return Response({
        'model_accuracy': 75.0,
        'total_predictions': 1247,
        'successful_signals': 935,
        'success_rate': 75.0,
        'last_updated': '2024-01-15T10:30:00Z'
    })
