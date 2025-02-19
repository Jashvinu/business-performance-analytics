import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class CFODashboardDataGenerator:
    def __init__(self, start_date='2022-01-01', end_date='2024-02-01', num_customers=1000):
        """Initialize the data generator with date range and base parameters"""
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.dates = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        self.num_customers = num_customers
        self.customer_ids = [f'CUST_{i:04d}' for i in range(num_customers)]
        
        # Product data
        self.products = [f'eBay Item Name {i+1}' for i in range(20)]
        self.product_base_prices = {prod: np.random.uniform(50, 500) for prod in self.products}
        
        # Geographic data
        self.countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'IT', 'ES']
        self.country_weights = [0.4, 0.2, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05]
        
        # Marketing channels
        self.channels = ['Facebook', 'Google', 'Email', 'Direct', 'Organic', 'Referral']
        
        # Create output directory
        if not os.path.exists('data'):
            os.makedirs('data')

    def generate_customer_data(self):
        """Generate customer profile data"""
        data = []
        loyalty_groups = ['Bronze', 'Silver', 'Gold', 'Platinum']
        dash_segments = ['New', 'Regular', 'Loyal', 'VIP', 'At Risk']
        
        for customer_id in self.customer_ids:
            join_date = np.random.choice(self.dates)
            months_active = (self.end_date - join_date).days / 30
            
            # Calculate customer metrics
            lifetime_value = np.random.lognormal(6, 1)  # Base CLTV
            total_revenue = lifetime_value * np.random.uniform(0.8, 1.2)
            churn_prob = min(0.1 + (months_active / 24) * 0.3, 0.95)
            
            data.append({
                'Customer ID': customer_id,
                'Join Date': join_date,
                'Loyalty Group': np.random.choice(loyalty_groups, p=[0.4, 0.3, 0.2, 0.1]),
                'Dash Segment': np.random.choice(dash_segments, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
                'CLTV Monetary Value': lifetime_value,
                'Total Revenue': total_revenue,
                'Churn': 1 if np.random.random() < churn_prob else 0,
                'P notAlive': churn_prob
            })
        
        return pd.DataFrame(data)

    def generate_sales_data(self):
        """Generate detailed sales transaction data"""
        data = []
        
        for date in self.dates:
            # More sales on weekends
            daily_sales = int(np.random.normal(50, 10) * (1.5 if date.weekday() >= 5 else 1))
            
            for _ in range(daily_sales):
                customer_id = np.random.choice(self.customer_ids)
                product = np.random.choice(self.products)
                country = np.random.choice(self.countries, p=self.country_weights)
                
                # Calculate prices and costs
                base_price = self.product_base_prices[product]
                quantity = np.random.randint(1, 5)
                
                # Apply seasonal and promotional effects
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
                discount_rate = np.random.choice([0, 0.1, 0.2], p=[0.7, 0.2, 0.1])
                
                # Calculate components
                unit_price = base_price * seasonal_factor * (1 - discount_rate)
                shipping_rate = {'US': 0.05, 'UK': 0.06, 'CA': 0.07, 'AU': 0.09,
                               'DE': 0.08, 'FR': 0.08, 'IT': 0.08, 'ES': 0.08}[country]
                tax_rate = {'US': 0.08, 'UK': 0.20, 'CA': 0.13, 'AU': 0.10,
                           'DE': 0.19, 'FR': 0.20, 'IT': 0.22, 'ES': 0.21}[country]
                
                shipping_amount = unit_price * shipping_rate * quantity
                tax = unit_price * tax_rate * quantity
                discount = unit_price * discount_rate * quantity
                total_amount = (unit_price * quantity) + shipping_amount + tax
                gross_profit = total_amount * 0.3
                
                data.append({
                    'Valuation Date': date,
                    'Customer ID': customer_id,
                    'Product Item Name': product,
                    'Conversion Country': country,
                    'Units Sold': quantity,
                    'Unit Price': unit_price,
                    'Shipping Amount': shipping_amount,
                    'Tax': tax,
                    'Discount': discount,
                    'Total Revenue': total_amount,
                    'Gross Profit': gross_profit
                })
        
        return pd.DataFrame(data)

    def generate_marketing_data(self):
        """Generate marketing campaign and attribution data"""
        # Event data
        event_data = []
        media_data = []
        
        for date in self.dates:
            # Generate daily events
            num_events = int(np.random.normal(100, 20))
            
            for _ in range(num_events):
                channel = np.random.choice(self.channels, p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.1])
                
                # Event sequence (higher probability for early stages)
                event_seq = np.random.choice(range(1, 8), p=[0.4, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02])
                
                # Conversion more likely in later sequences
                is_target = 1 if (event_seq > 4 and np.random.random() < 0.7) else 0
                
                # Calculate AOV based on channel and sequence
                base_aov = {'Facebook': 75, 'Google': 85, 'Email': 95,
                           'Direct': 100, 'Organic': 80, 'Referral': 90}[channel]
                aov = base_aov * (1 + 0.1 * event_seq) * np.random.uniform(0.8, 1.2)
                
                event_data.append({
                    'Event DateTime': date,
                    'Channel': channel,
                    'Event Sequence': event_seq,
                    'AOV': aov,
                    'Is Target': is_target
                })
            
            # Generate daily media spend
            for channel in self.channels:
                base_spend = {'Facebook': 1000, 'Google': 1200, 'Email': 500,
                             'Direct': 300, 'Organic': 200, 'Referral': 400}[channel]
                
                daily_spend = base_spend * np.random.uniform(0.8, 1.2)
                
                media_data.append({
                    'Date': date,
                    'Channel': channel,
                    'Media Spend': daily_spend
                })
        
        return pd.DataFrame(event_data), pd.DataFrame(media_data)

    def generate_financial_data(self):
        """Generate financial statements data"""
        monthly_dates = pd.date_range(start=self.start_date, end=self.end_date, freq='M')
        
        data = []
        base_revenue = 1000000  # Starting monthly revenue
        growth_rate = 0.15  # Annual growth rate
        
        for date in monthly_dates:
            # Generate base revenue with growth and seasonality
            year_factor = (1 + growth_rate) ** ((date - self.start_date).days / 365)
            season_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
            revenue = base_revenue * year_factor * season_factor
            
            # Generate expenses as percentages of revenue
            expenses = {
                'WageExp': revenue * np.random.normal(0.25, 0.02),
                'AdSpend': revenue * np.random.normal(0.10, 0.03),
                'ReturnAllow': revenue * np.random.normal(0.03, 0.01),
                'CGS': revenue * np.random.normal(0.40, 0.03),
                'BankFees': revenue * np.random.normal(0.01, 0.002),
                'DepExp': revenue * np.random.normal(0.05, 0.01),
                'Rent': revenue * np.random.normal(0.08, 0.01),
                'Supplies': revenue * np.random.normal(0.03, 0.01),
                'Utils': revenue * np.random.normal(0.02, 0.005),
                'PayrollTax': revenue * np.random.normal(0.075, 0.005),
                'OthExp': revenue * np.random.normal(0.05, 0.02)
            }
            
            # Calculate totals and profit
            total_expenses = sum(expenses.values())
            profit = revenue - total_expenses
            
            # Generate balance sheet items
            balance_sheet = {
                'Cash': profit + np.random.normal(500000, 50000),
                'AR': revenue * 0.2,
                'Inventory': expenses['CGS'] * 1.5,
                'FixAsset': 2000000 - (date - self.start_date).days * 1000,  # Depreciation
                'AP': expenses['CGS'] * 0.3,
                'Stock': 1000000
            }
            
            data.append({
                'Valuation Date': date,
                'Year': date.year,
                'Month': date.month,
                'Rev': revenue,
                **expenses,
                **balance_sheet,
                'Profit or Loss': profit
            })
        
        return pd.DataFrame(data)

    def generate_all_data(self):
        """Generate all datasets and save to CSV"""
        print("Generating customer data...")
        customers_data = self.generate_customer_data()
        customers_data.to_csv('data/customers_report.csv', index=False)
        
        print("Generating sales data...")
        sales_data = self.generate_sales_data()
        sales_data.to_csv('data/sales_report.csv', index=False)
        
        print("Generating marketing data...")
        event_data, media_data = self.generate_marketing_data()
        event_data.to_csv('data/market_data.csv', index=False)
        media_data.to_csv('data/media_data.csv', index=False)
        
        print("Generating financial data...")
        financial_data = self.generate_financial_data()
        
        # Split financial data into different statements
        financial_data.to_csv('data/income_data.csv', index=False)
        financial_data.to_csv('data/balance_sheet.csv', index=False)
        financial_data.to_csv('data/cash_flow.csv', index=False)
        
        print("Data generation complete! Files saved in the 'data' directory.")
        
        return {
            'customers': customers_data,
            'sales': sales_data,
            'events': event_data,
            'media': media_data,
            'financial': financial_data
        }

if __name__ == "__main__":
    # Create data generator instance
    generator = CFODashboardDataGenerator()
    
    # Generate all data
    data = generator.generate_all_data()