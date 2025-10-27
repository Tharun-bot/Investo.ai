"""
Example ML model for stock prediction - similar to your PyTorch implementation
This demonstrates the type of model that could power the AI signals
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def generate_mock_data(n_samples=1000):
    """Generate mock financial data for demonstration"""
    np.random.seed(42)
    
    # Features: price ratios, technical indicators, volume metrics
    data = {
        'pe_ratio': np.random.normal(25, 10, n_samples),
        'pb_ratio': np.random.normal(3, 1.5, n_samples),
        'rsi': np.random.uniform(0, 100, n_samples),
        'macd': np.random.normal(0, 2, n_samples),
        'volume_ratio': np.random.normal(1, 0.5, n_samples),
        'price_momentum': np.random.normal(0, 0.1, n_samples),
        'earnings_growth': np.random.normal(0.08, 0.15, n_samples),
        'revenue_growth': np.random.normal(0.05, 0.12, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (0: SELL, 1: HOLD, 2: BUY)
    # Simple rule-based target for demonstration
    conditions = [
        (df['pe_ratio'] < 15) & (df['rsi'] < 30) & (df['earnings_growth'] > 0.1),  # BUY
        (df['pe_ratio'] > 35) | (df['rsi'] > 70),  # SELL
    ]
    choices = [2, 0]  # BUY, SELL
    df['signal'] = np.select(conditions, choices, default=1)  # Default HOLD
    
    return df

def train_signal_model():
    """Train a model to predict buy/sell/hold signals"""
    print("Generating training data...")
    df = generate_mock_data(1000)
    
    # Prepare features and target
    feature_columns = ['pe_ratio', 'pb_ratio', 'rsi', 'macd', 'volume_ratio', 
                      'price_momentum', 'earnings_growth', 'revenue_growth']
    X = df[feature_columns]
    y = df['signal']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['SELL', 'HOLD', 'BUY']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    return model, scaler

def predict_signal(model, scaler, stock_data):
    """Predict signal for a given stock"""
    # Example stock data
    features = np.array([[
        stock_data.get('pe_ratio', 25),
        stock_data.get('pb_ratio', 3),
        stock_data.get('rsi', 50),
        stock_data.get('macd', 0),
        stock_data.get('volume_ratio', 1),
        stock_data.get('price_momentum', 0),
        stock_data.get('earnings_growth', 0.08),
        stock_data.get('revenue_growth', 0.05)
    ]])
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    confidence = model.predict_proba(features_scaled)[0].max()
    
    signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
    
    return {
        'signal': signal_map[prediction],
        'confidence': confidence * 100
    }

if __name__ == "__main__":
    # Train the model
    model, scaler = train_signal_model()
    
    # Example prediction
    example_stock = {
        'pe_ratio': 22,
        'pb_ratio': 2.5,
        'rsi': 45,
        'macd': 1.2,
        'volume_ratio': 1.1,
        'price_momentum': 0.05,
        'earnings_growth': 0.12,
        'revenue_growth': 0.08
    }
    
    result = predict_signal(model, scaler, example_stock)
    print(f"\nPrediction for example stock:")
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']:.1f}%")
