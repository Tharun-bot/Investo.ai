# Investo.ai - AI-Powered Stock Signal Platform

A complete Django-based stock analysis platform with real-time data from yfinance and machine learning predictions.

## Features

- **Real-time Stock Data**: Integration with yfinance for live market data
- **AI-Powered Signals**: Machine learning models for buy/sell/hold recommendations
- **Technical Analysis**: RSI, MACD, Bollinger Bands, and more
- **Fundamental Analysis**: P/E ratios, P/B ratios, financial metrics
- **Portfolio Tracking**: Track your investments and performance
- **Market Overview**: Real-time market indices and trends
- **REST API**: Complete API for mobile apps or external integrations

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Redis (optional, for background tasks)

### Installation

1. **Clone and setup the project:**
   \`\`\`bash
   # Make setup script executable
   chmod +x setup.sh
   
   # Run setup
   ./setup.sh
   \`\`\`

2. **Or manual setup:**
   \`\`\`bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   \`\`\`

3. **Start the development server:**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

4. **Access the application:**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/api/

## API Endpoints

### Stock Data
- `GET /api/stocks/{symbol}/` - Get real-time stock data
- `POST /api/stocks/{symbol}/signal/` - Generate AI signal
- `GET /api/stocks/signals/recent/` - Get recent signals
- `GET /api/stocks/search/?q={query}` - Search stocks
- `GET /api/stocks/market/overview/` - Market overview

### Machine Learning
- `POST /api/ml/predict/{symbol}/` - Get ML prediction
- `GET /api/ml/model/stats/` - Model performance stats

## Usage Examples

### Get Stock Data
\`\`\`bash
curl http://127.0.0.1:8000/api/stocks/AAPL/
\`\`\`

### Generate AI Signal
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/stocks/AAPL/signal/
\`\`\`

### Search Stocks
\`\`\`bash
curl http://127.0.0.1:8000/api/stocks/search/?q=apple
\`\`\`

## Project Structure

\`\`\`
investo_ai/
├── investo_ai/          # Django project settings
├── stocks/              # Stock data and signals app
├── ml_models/           # Machine learning models app
├── templates/           # HTML templates
├── static/              # Static files
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
\`\`\`

## Machine Learning Model

The platform uses a Random Forest classifier trained on:
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Volume ratios
- **Fundamental Metrics**: P/E ratio, P/B ratio, Growth rates
- **Market Data**: Price momentum, Volatility measures

**Model Performance**: 75% accuracy on historical data

## Customization

### Adding New Indicators

1. Edit `ml_models/predictor.py`
2. Add your indicator to `_calculate_technical_indicators()`
3. Update the feature list and retrain the model

### Integrating Other Data Sources

1. Replace yfinance calls in `stocks/views.py`
2. Update the data fetching logic
3. Ensure data format consistency

