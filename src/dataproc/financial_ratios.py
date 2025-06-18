"""Module for processing financial ratios for data analysis"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

class FinancialRatiosProcessor:
    def __init__(self, data_dir : str):
        self.data_dir = Path(data_dir)
        self.ratios_df = None
    
    def load_data(self) -> None:
        """Load all financial data from the directory"""
        print(f'Loading data from : {self.data_dir.absolute()}')
        print(f"Directory Exists : {self.data_dir.exists()}")

        all_data = []
        file_count = 0

        for file_path in self.data_dir.glob("*_10Y_QUARTERLY.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        all_data.extend(data)
                        file_count+=1
                    else:
                        print(f"Invalid Data")
            except Exception as e:
                print(f"Error : {e}")
        
        print(f"Processed {file_count} files")
        print(f"Total records : {len(all_data)}")

        if not all_data:
            raise ValueError("No data loaded")
        
        self.ratios_df = pd.DataFrame(all_data)
        print(f"Before applying datetime function : {self.ratios_df['date'][:5]}")
        print(f"After applying datetime function : {pd.to_datetime(self.ratios_df['date'][:5]).dt.tz_localize(None)}")
        self.ratios_df['date'] = pd.to_datetime(self.ratios_df['date']).dt.tz_localize(None)
        self.ratios_df.sort_values(['symbol', 'date'], inplace=True)

    def get_key_ratios(self) -> pd.DataFrame:
        """Extract key financial ratios for analysis"""
        if  self.load_data() is None:
            self.load_data()
        key_ratios = [
            # Profitability
            'grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin',
            'returnOnAssets', 'returnOnEquity',
            
            # Valuation
            'priceEarningsRatio', 'priceToBookRatio', 'priceToSalesRatio',
            'enterpriseValueMultiple',
            
            # Financial Health
            'currentRatio', 'debtEquityRatio', 'interestCoverage',
            'cashFlowToDebtRatio',
            
            # Growth & Efficiency
            'assetTurnover', 'inventoryTurnover', 'receivablesTurnover'
        ]

        return self.ratios_df[['symbol', 'date'] + key_ratios]
    
    def check_data_consistency(self) -> pd.DataFrame:
        """Checks for data consistency"""
        df = self.get_key_ratios()
        issues = []
        # Check for zeros in ratios where they don't make sense
        zero_check_ratios = [
            'grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin',
            'returnOnAssets', 'returnOnEquity', 'currentRatio'
        ]

        for ratio in zero_check_ratios:
            if(ratio in df.columns):
                zero_mask = df[ratio] == 0
                if zero_mask.any():
                    issues.extend(df[zero_mask].index.to_list())
        
        #check for missing values
        missing_mask = df.isnull().any(axis=1)
        if missing_mask.any():
            issues.extend(df[missing_mask].index.to_list())
        
        # Check for extreme outliers
        outlier_ratios = {
            'priceEarningsRatio': (0, 100),
            'priceToBookRatio': (0, 50),
            'priceToSalesRatio': (0, 50),
            'enterpriseValueMultiple': (0, 100)
        }

        for ratio, (min_value, max_value) in outlier_ratios.items():
            if ratio in df.columns:
                outlier_mask = (df[ratio] < min_value) | (df[ratio] > max_value)
                if(outlier_mask.any()):
                    issues.extend(df[outlier_mask].index.to_list())
        
              # Create issues DataFrame
        issues_df = pd.DataFrame({
            'symbol': df.loc[issues, 'symbol'],
            'date': df.loc[issues, 'date'],
            'issue_type': 'data_consistency'
        })
        
        return issues_df.head()



fr = FinancialRatiosProcessor(data_dir='data/FMP')
#fr.load_data()
#fr.get_key_ratios()
print(fr.check_data_consistency())