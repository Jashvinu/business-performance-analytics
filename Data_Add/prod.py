import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_income_sheet(start_date='2022-01-01', end_date='2024-02-01'):
    """Generate Income DataSheet"""
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    base_revenue = 1000000  # Starting monthly revenue
    growth_rate = 0.15      # Annual growth rate
    
    data = []
    for date in dates:
        # Calculate growth and seasonal factors
        years_passed = (date - pd.to_datetime(start_date)).days / 365
        growth_factor = (1 + growth_rate) ** years_passed
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
        
        # Base revenue with growth and seasonality
        revenue = base_revenue * growth_factor * seasonal_factor * (1 + 0.1 * np.random.randn())
        
        # Calculate expenses as percentages of revenue
        expenses = {
            'WageExp': revenue * np.random.normal(0.25, 0.02),
            'AdSpend': revenue * np.random.normal(0.10, 0.02),
            'BankFees': revenue * np.random.normal(0.02, 0.005),
            'DepExp': revenue * np.random.normal(0.05, 0.01),
            'Rent': revenue * np.random.normal(0.08, 0.01),
            'Supplies': revenue * np.random.normal(0.03, 0.01),
            'Utils': revenue * np.random.normal(0.02, 0.005),
            'PayrollTax': revenue * np.random.normal(0.075, 0.005),
            'OthExp': revenue * np.random.normal(0.05, 0.01),
            'ReturnAllow': revenue * np.random.normal(0.03, 0.01),
            'CGS': revenue * np.random.normal(0.4, 0.03),
        }
        
        # Calculate profit/loss
        total_expenses = sum(expenses.values())
        profit_or_loss = revenue - total_expenses
        
        data.append({
            'Valuation Date': date,
            'Year': date.year,
            'Month': date.month,
            'Rev': revenue,
            'Profit or Loss': profit_or_loss,
            **expenses
        })
    
    return pd.DataFrame(data)

def generate_balance_sheet(start_date='2022-01-01', end_date='2024-02-01'):
    """Generate Balance Sheet"""
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    base_value = 1000000  # Base value for calculations
    
    data = []
    for date in dates:
        years_passed = (date - pd.to_datetime(start_date)).days / 365
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
        
        # Calculate debt components
        debt_components = {
            'AP': base_value * 0.3 * (1 + years_passed * 0.1) * (1 + 0.1 * np.random.randn()),
            'AL': base_value * 0.2 * (1 + years_passed * 0.05) * seasonal_factor,
            'TP': base_value * 0.15 * (1 + years_passed * 0.08),
            'WP': base_value * 0.25 * (1 + years_passed * 0.07) * seasonal_factor,
            'NP': base_value * (1 - years_passed * 0.1),  # Decreasing over time
        }
        
        # Calculate equity components
        equity_components = {
            'Stock': base_value * 2 * (1 + years_passed * 0.15),
            'Retained Earnings': base_value * (1 + years_passed * 0.2) * seasonal_factor,
            'Distributable Earnings': base_value * 0.1 * seasonal_factor
        }
        
        data.append({
            'Valuation Date': date,
            'Year': date.year,
            'Month': date.month,
            **debt_components,
            **equity_components,
            'Increase in TP': debt_components['TP'] * 0.1,
            'Increase in WP': debt_components['WP'] * 0.1
        })
    
    return pd.DataFrame(data)

def generate_customers_report(start_date='2022-01-01', end_date='2024-02-01', num_customers=1000):
    """Generate Customers Report"""
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    customer_ids = [f'CUST_{i:04d}' for i in range(num_customers)]
    
    data = []
    for date in dates:
        for customer_id in np.random.choice(customer_ids, size=int(len(customer_ids)*0.8)):  # 80% active each month
            # Calculate CLTV and related metrics
            base_value = np.random.lognormal(6, 1)  # Base CLTV
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
            
            data.append({
                'Valuation Date': date,
                'Year': date.year,
                'Month': date.month,
                'Customer ID': customer_id,
                'CLTV Monetary Value': base_value * seasonal_factor,
                'Discount': base_value * 0.1 * np.random.uniform(0.8, 1.2)  # Discount as proxy for CAC
            })
    
    return pd.DataFrame(data)

def generate_all_sheets():
    """Generate all required sheets and save to CSV"""
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("Generating Income DataSheet...")
    income_df = generate_income_sheet()
    income_df.to_csv('data/income_datasheet.csv', index=False)
    
    print("Generating Balance Sheet...")
    balance_df = generate_balance_sheet()
    balance_df.to_csv('data/balance_sheet.csv', index=False)
    
    print("Generating Customers Report...")
    customers_df = generate_customers_report()
    customers_df.to_csv('data/customers_report.csv', index=False)
    
    print("All sheets have been generated and saved to the 'data' directory!")
    
    return {
        'income_sheet': income_df,
        'balance_sheet': balance_df,
        'customers_report': customers_df
    }

if __name__ == "__main__":
    dfs = generate_all_sheets()
    
    # Display sample data from each sheet
    for sheet_name, df in dfs.items():
        print(f"\nSample data from {sheet_name}:")
        print(df.head())
        print("\nColumns:", df.columns.tolist())