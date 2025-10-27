import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class StockPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'rsi', 'macd', 'bb_position', 'volume_ratio', 
            'price_momentum', 'volatility', 'pe_ratio', 'pb_ratio'
        ]
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        model_path = 'ml_models/trained_model.pkl'
        scaler_path = 'ml_models/scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        else:
            self._train_model()
    
    def _train_model(self):
        """Train a new model with synthetic data"""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        
        # Create features
        data = {
            'rsi': np.random.uniform(0, 100, n_samples),
            'macd': np.random.normal(0, 2, n_samples),
            'bb_position': np.random.uniform(0, 1, n_samples),
            'volume_ratio': np.random.normal(1, 0.5, n_samples),
            'price_momentum': np.random.normal(0, 0.1, n_samples),
            'volatility': np.random.uniform(0.1, 0.5, n_samples),
            'pe_ratio': np.random.normal(25, 10, n_samples),
            'pb_ratio': np.random.normal(3, 1.5, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create target variable (0: SELL, 1: HOLD, 2: BUY)
        conditions = [
            (df['rsi'] < 30) & (df['price_momentum'] > 0.05) & (df['pe_ratio'] < 20),  # BUY
            (df['rsi'] > 70) | (df['pe_ratio'] > 35) | (df['price_momentum'] < -0.05),  # SELL
        ]
        choices = [2, 0]  # BUY, SELL
        df['target'] = np.select(conditions, choices, default=1)  # Default HOLD
        
        # Prepare data
        X = df[self.feature_names]
        y = df['target']
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs('ml_models', exist_ok=True)
        joblib.dump(self.model, 'ml_models/trained_model.pkl')
        joblib.dump(self.scaler, 'ml_models/scaler.pkl')
    
    def _calculate_technical_indicators(self, hist_data):
        """Calculate technical indicators from historical data"""
        try:
            df = hist_data.copy()
            
            if len(df) < 14:
                # Not enough data for proper indicators
                return {
                    'rsi': 50,
                    'macd': 0,
                    'bb_position': 0.5,
                    'volume_ratio': 1,
                    'price_momentum': 0,
                    'volatility': 0.2
                }
            
            # RSI with error handling
            try:
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=min(14, len(df)-1)).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df)-1)).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                rsi_value = rsi.iloc[-1] if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50
            except:
                rsi_value = 50
            
            # MACD with error handling
            try:
                exp1 = df['Close'].ewm(span=min(12, len(df)//2)).mean()
                exp2 = df['Close'].ewm(span=min(26, len(df)//2)).mean()
                macd = exp1 - exp2
                macd_value = macd.iloc[-1] if not macd.empty and not pd.isna(macd.iloc[-1]) else 0
            except:
                macd_value = 0
            
            # Bollinger Bands with error handling
            try:
                window = min(20, len(df)//2)
                bb_middle = df['Close'].rolling(window=window).mean()
                bb_std = df['Close'].rolling(window=window).std()
                bb_upper = bb_middle + (bb_std * 2)
                bb_lower = bb_middle - (bb_std * 2)
                bb_position = (df['Close'] - bb_lower) / (bb_upper - bb_lower)
                bb_pos_value = bb_position.iloc[-1] if not bb_position.empty and not pd.isna(bb_position.iloc[-1]) else 0.5
            except:
                bb_pos_value = 0.5
            
            # Volume ratio with error handling
            try:
                window = min(20, len(df)//2)
                volume_ma = df['Volume'].rolling(window=window).mean()
                volume_ratio = df['Volume'] / volume_ma
                vol_ratio_value = volume_ratio.iloc[-1] if not volume_ratio.empty and not pd.isna(volume_ratio.iloc[-1]) else 1
            except:
                vol_ratio_value = 1
            
            # Price momentum with error handling
            try:
                momentum_period = min(5, len(df)//4)
                price_momentum = df['Close'].pct_change(periods=momentum_period)
                momentum_value = price_momentum.iloc[-1] if not price_momentum.empty and not pd.isna(price_momentum.iloc[-1]) else 0
            except:
                momentum_value = 0
            
            # Volatility with error handling
            try:
                window = min(20, len(df)//2)
                volatility = df['Close'].pct_change().rolling(window=window).std()
                vol_value = volatility.iloc[-1] if not volatility.empty and not pd.isna(volatility.iloc[-1]) else 0.2
            except:
                vol_value = 0.2
            
            return {
                'rsi': float(rsi_value),
                'macd': float(macd_value),
                'bb_position': float(bb_pos_value),
                'volume_ratio': float(vol_ratio_value),
                'price_momentum': float(momentum_value),
                'volatility': float(vol_value)
            }
            
        except Exception as e:
            # Return default values if everything fails
            return {
                'rsi': 50,
                'macd': 0,
                'bb_position': 0.5,
                'volume_ratio': 1,
                'price_momentum': 0,
                'volatility': 0.2
            }
    
    def generate_signal(self, hist_data, stock_info):
        """Generate trading signal for a stock"""
        try:
            # Validate input data
            if hist_data.empty:
                raise ValueError("No historical data provided")
            
            if len(hist_data) < 20:
                # Not enough data for proper analysis
                current_price = float(hist_data['Close'].iloc[-1])
                return {
                    'signal': 'HOLD',
                    'confidence': 50.0,
                    'current_price': round(current_price, 2),
                    'target_price': round(current_price, 2),
                    'reason': 'Insufficient historical data for reliable analysis',
                    'technical_score': 50.0,
                    'fundamental_score': 50.0,
                    'ml_score': 50.0
                }
            
            # Calculate technical indicators
            tech_indicators = self._calculate_technical_indicators(hist_data)
            
            # Get fundamental data with better error handling
            pe_ratio = stock_info.get('trailingPE')
            pb_ratio = stock_info.get('priceToBook')
            
            # Handle None or invalid values
            if pe_ratio is None or pe_ratio <= 0 or pe_ratio > 1000:
                pe_ratio = 25  # Use market average as default
            if pb_ratio is None or pb_ratio <= 0 or pb_ratio > 50:
                pb_ratio = 3   # Use market average as default
            
            # Prepare features with better validation
            features = [
                tech_indicators.get('rsi', 50),
                tech_indicators.get('macd', 0),
                tech_indicators.get('bb_position', 0.5),
                tech_indicators.get('volume_ratio', 1),
                tech_indicators.get('price_momentum', 0),
                tech_indicators.get('volatility', 0.2),
                pe_ratio,
                pb_ratio
            ]
            
            # Handle NaN values and ensure all features are numeric
            cleaned_features = []
            for i, feature in enumerate(features):
                if pd.isna(feature) or feature is None or not isinstance(feature, (int, float)):
                    # Use default values for each feature
                    defaults = [50, 0, 0.5, 1, 0, 0.2, 25, 3]
                    cleaned_features.append(defaults[i])
                else:
                    cleaned_features.append(float(feature))
            
            # Make prediction
            try:
                features_scaled = self.scaler.transform([cleaned_features])
                prediction = self.model.predict(features_scaled)[0]
                confidence = self.model.predict_proba(features_scaled)[0].max() * 100
            except Exception as e:
                # Fallback if ML prediction fails
                prediction = 1  # HOLD
                confidence = 50.0
            
            # Map prediction to signal
            signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
            signal = signal_map[prediction]
            
            # Calculate scores
            technical_score = self._calculate_technical_score(tech_indicators)
            fundamental_score = self._calculate_fundamental_score(pe_ratio, pb_ratio)
            ml_score = confidence
            
            # Generate reason
            reason = self._generate_reason(signal, tech_indicators, pe_ratio, pb_ratio)
            
            # Calculate target price
            current_price = float(hist_data['Close'].iloc[-1])
            target_price = self._calculate_target_price(signal, current_price, tech_indicators)
            
            return {
                'signal': signal,
                'confidence': round(confidence, 1),
                'current_price': round(current_price, 2),
                'target_price': round(target_price, 2) if target_price else round(current_price, 2),
                'reason': reason,
                'technical_score': round(technical_score, 1),
                'fundamental_score': round(fundamental_score, 1),
                'ml_score': round(ml_score, 1)
            }
            
        except Exception as e:
            # Ultimate fallback response
            try:
                current_price = float(hist_data['Close'].iloc[-1])
            except:
                current_price = 100.0  # Default fallback price
                
            return {
                'signal': 'HOLD',
                'confidence': 50.0,
                'current_price': round(current_price, 2),
                'target_price': round(current_price, 2),
                'reason': f'Analysis error: {str(e)[:100]}...',
                'technical_score': 50.0,
                'fundamental_score': 50.0,
                'ml_score': 50.0
            }
    
    def _calculate_technical_score(self, indicators):
        """Calculate technical analysis score"""
        score = 50  # Neutral
        
        # RSI scoring
        if indicators['rsi'] < 30:
            score += 20  # Oversold - bullish
        elif indicators['rsi'] > 70:
            score -= 20  # Overbought - bearish
        
        # MACD scoring
        if indicators['macd'] > 0:
            score += 10
        else:
            score -= 10
        
        # Bollinger Bands scoring
        if indicators['bb_position'] < 0.2:
            score += 15  # Near lower band - bullish
        elif indicators['bb_position'] > 0.8:
            score -= 15  # Near upper band - bearish
        
        # Price momentum scoring
        if indicators['price_momentum'] > 0.02:
            score += 15
        elif indicators['price_momentum'] < -0.02:
            score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_fundamental_score(self, pe_ratio, pb_ratio):
        """Calculate fundamental analysis score"""
        score = 50  # Neutral
        
        # P/E ratio scoring
        if pe_ratio and pe_ratio > 0:
            if pe_ratio < 15:
                score += 20  # Undervalued
            elif pe_ratio > 30:
                score -= 20  # Overvalued
        
        # P/B ratio scoring
        if pb_ratio and pb_ratio > 0:
            if pb_ratio < 1.5:
                score += 15  # Undervalued
            elif pb_ratio > 4:
                score -= 15  # Overvalued
        
        return max(0, min(100, score))
    
    def _generate_reason(self, signal, indicators, pe_ratio, pb_ratio):
        """Generate human-readable reason for the signal"""
        reasons = []
        
        if signal == 'BUY':
            if indicators['rsi'] < 35:
                reasons.append("oversold conditions")
            if indicators['price_momentum'] > 0.02:
                reasons.append("strong price momentum")
            if pe_ratio and pe_ratio < 20:
                reasons.append("attractive valuation")
            if not reasons:
                reasons.append("positive technical and fundamental factors")
        
        elif signal == 'SELL':
            if indicators['rsi'] > 65:
                reasons.append("overbought conditions")
            if indicators['price_momentum'] < -0.02:
                reasons.append("negative price momentum")
            if pe_ratio and pe_ratio > 30:
                reasons.append("high valuation concerns")
            if not reasons:
                reasons.append("negative technical and fundamental factors")
        
        else:  # HOLD
            reasons.append("mixed signals suggest waiting for clearer direction")
        
        return "Signal based on " + ", ".join(reasons)
    
    def _calculate_target_price(self, signal, current_price, indicators):
        """Calculate target price based on signal"""
        if signal == 'BUY':
            # Target 5-10% above current price
            multiplier = 1.05 + (indicators['price_momentum'] * 10) if indicators['price_momentum'] > 0 else 1.05
            return current_price * min(multiplier, 1.10)
        elif signal == 'SELL':
            # Target 5-10% below current price
            multiplier = 0.95 + (indicators['price_momentum'] * 10) if indicators['price_momentum'] < 0 else 0.95
            return current_price * max(multiplier, 0.90)
        else:
            return current_price
