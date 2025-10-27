import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock, StockData, Signal
from .serializers import StockSerializer, SignalSerializer
from ml_models.predictor import StockPredictor
from django.db import models

@api_view(['GET'])
def get_stock_data(request, symbol):
    """Get real-time stock data using yfinance"""
    try:
        # Validate symbol
        if not symbol or symbol.upper() == 'UNDEFINED':
            return Response(
                {"error": "Invalid stock symbol provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        symbol = symbol.upper().strip()
        
        # Fetch data from yfinance
        ticker = yf.Ticker(symbol)
        
        # Try to get basic info first
        try:
            info = ticker.info
            if not info or 'symbol' not in info:
                return Response(
                    {"error": f"Stock symbol '{symbol}' not found or may be delisted"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"Unable to fetch information for '{symbol}'. Symbol may be invalid or delisted."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Try to get historical data
        try:
            hist = ticker.history(period="1d", interval="1m")
            if hist.empty:
                # Try with a longer period
                hist = ticker.history(period="5d")
                if hist.empty:
                    return Response(
                        {"error": f"No price data available for '{symbol}'. Symbol may be delisted or invalid."}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
        except Exception as e:
            return Response(
                {"error": f"Unable to fetch price data for '{symbol}': {str(e)}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create stock in database
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={
                'name': info.get('longName', symbol),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', '')
            }
        )
        
        # Current price data
        current_price = float(hist['Close'].iloc[-1])
        previous_close = info.get('previousClose', current_price)
        if previous_close is None or previous_close == 0:
            previous_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0
        
        # Get latest signal
        latest_signal = Signal.objects.filter(stock=stock, is_active=True).first()
        
        # Prepare chart data (limit to last 50 points for performance)
        chart_data = []
        hist_limited = hist.tail(50)
        for index, row in hist_limited.iterrows():
            chart_data.append({
                'time': index.strftime('%H:%M') if hasattr(index, 'strftime') else str(index)[-5:],
                'price': round(float(row['Close']), 2),
                'volume': int(row['Volume']) if not pd.isna(row['Volume']) else 0
            })
        
        response_data = {
            'symbol': stock.symbol,
            'name': stock.name,
            'price': round(current_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': info.get('volume', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', None),
            'pb_ratio': info.get('priceToBook', None),
            'dividend_yield': info.get('dividendYield', None),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', None),
            'signal': SignalSerializer(latest_signal).data if latest_signal else None,
            'chart_data': chart_data
        }
        
        return Response(response_data)
        
    except Exception as e:
        error_message = str(e)
        if "404" in error_message or "delisted" in error_message.lower():
            return Response(
                {"error": f"Stock symbol '{symbol}' not found or may be delisted"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                {"error": f"An error occurred while fetching data: {error_message}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def generate_signal(request, symbol):
    """Generate AI signal for a stock"""
    try:
        # Validate symbol
        if not symbol or symbol.upper() == 'UNDEFINED':
            return Response(
                {"error": "Invalid stock symbol provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        symbol = symbol.upper().strip()
        
        # Get or create stock
        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            # Try to create stock if it doesn't exist
            ticker = yf.Ticker(symbol)
            try:
                info = ticker.info
                if not info or 'symbol' not in info:
                    return Response(
                        {"error": f"Stock symbol '{symbol}' not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                stock = Stock.objects.create(
                    symbol=symbol,
                    name=info.get('longName', symbol),
                    sector=info.get('sector', ''),
                    industry=info.get('industry', '')
                )
            except Exception as e:
                return Response(
                    {"error": f"Unable to find or create stock '{symbol}': {str(e)}"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Fetch recent data for analysis
        ticker = yf.Ticker(symbol)
        try:
            hist = ticker.history(period="3mo")
            info = ticker.info
            
            if hist.empty:
                return Response(
                    {"error": f"Insufficient historical data for '{symbol}' to generate signal"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": f"Unable to fetch data for analysis: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize predictor and generate signal
        predictor = StockPredictor()
        signal_data = predictor.generate_signal(hist, info)
        
        # Deactivate old signals for this stock
        Signal.objects.filter(stock=stock, is_active=True).update(is_active=False)
        
        # Create new signal in database
        signal = Signal.objects.create(
            stock=stock,
            signal_type=signal_data['signal'],
            confidence=signal_data['confidence'],
            price_at_signal=Decimal(str(signal_data['current_price'])),
            target_price=Decimal(str(signal_data['target_price'])) if signal_data['target_price'] else None,
            reason=signal_data['reason'],
            technical_score=signal_data['technical_score'],
            fundamental_score=signal_data['fundamental_score'],
            ml_score=signal_data['ml_score']
        )
        
        return Response(SignalSerializer(signal).data)
        
    except Exception as e:
        return Response(
            {"error": f"Error generating signal: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_recent_signals(request):
    """Get recent signals across all stocks"""
    signals = Signal.objects.filter(is_active=True)[:20]
    return Response(SignalSerializer(signals, many=True).data)

@api_view(['GET'])
def search_stocks(request):
    """Search for stocks by symbol or name"""
    query = request.GET.get('q', '')
    if not query:
        return Response([])
    
    # Search in database first
    stocks = Stock.objects.filter(
        models.Q(symbol__icontains=query) | 
        models.Q(name__icontains=query)
    )[:10]
    
    return Response(StockSerializer(stocks, many=True).data)

@api_view(['GET'])
def market_overview(request):
    """Get market overview data"""
    market_symbols = ['^GSPC', '^IXIC', '^DJI', '^VIX']
    market_data = []
    
    for symbol in market_symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current
                change = current - previous
                change_percent = (change / previous) * 100 if previous else 0
                
                name_map = {
                    '^GSPC': 'S&P 500',
                    '^IXIC': 'NASDAQ',
                    '^DJI': 'DOW',
                    '^VIX': 'VIX'
                }
                
                market_data.append({
                    'name': name_map.get(symbol, symbol),
                    'value': round(current, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'positive': change >= 0
                })
        except:
            continue
    
    return Response(market_data)
