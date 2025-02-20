import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from constants import MONTHS

# Color palette for consistency
COLORS = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]

def prepare_data(data):
    """Prepare data for demand elasticity analysis"""
    # Make a copy to avoid SettingWithCopyWarning
    df = data.copy()
    
    # Check if we have a date column or need to create one
    if 'Date' not in df.columns:
        # Print available columns for debugging
        print("Available columns:", df.columns.tolist())
        
        # Try different date column possibilities
        if 'Created Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Created Date'])
        elif 'Transaction_Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Transaction_Date'])
        elif 'Order Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Order Date'])
        else:
            # If no date column found, create a dummy date for testing
            print("Warning: No date column found, using index as date")
            df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    
    # Extract year and month
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    return df

def price_elasticity_overtime(data):
    """Calculate and visualize price elasticity over time"""
    try:
        df = prepare_data(data)
        
        # Group and calculate mean elasticity
        yearly_elasticity = df.groupby(["Year", "Product"])["Price Elasticity"].mean().reset_index()
        
        fig = go.Figure()
        
        # Create bars for each product
        for idx, prod in enumerate(yearly_elasticity['Product'].unique()):
            prod_data = yearly_elasticity[yearly_elasticity["Product"] == prod]
            
            fig.add_trace(
                go.Bar(
                    y=prod_data["Year"].astype(str),
                    x=prod_data["Price Elasticity"],
                    name=prod,
                    marker=dict(color=COLORS[idx % len(COLORS)]),
                    orientation="h",
                    hovertemplate="Year: %{y}<br>" +
                                "Elasticity: %{x:.2f}<br>" +
                                "<extra></extra>"
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Average Price Elasticity By Year",
            xaxis_title="Price Elasticity",
            yaxis_title="Year",
            showlegend=True,
            barmode='group',
            height=600,
            yaxis={'categoryorder': 'category ascending'},
            hovermode='closest'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in price_elasticity_overtime: {str(e)}")
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )

def elasticity_vs_base_price(data):
    """Create scatter plot of elasticity vs base price"""
    try:
        df = prepare_data(data)
        
        fig = px.scatter(
            df,
            x="Base Price",
            y="Price Elasticity",
            color="Product",
            size="Units Sold",
            animation_frame="Year",
            title="Price Elasticity vs. Base Price",
            hover_data=["Product", "Base Price", "Price Elasticity", "Units Sold"]
        )
        
        fig.update_yaxes(type="log")
        fig.update_layout(
            height=600,
            hovermode='closest'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in elasticity_vs_base_price: {str(e)}")
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )

def sales_volume_overtime(data):
    """Analyze sales volume trends over time"""
    try:
        df = prepare_data(data)
        
        # Calculate yearly sales by product
        yearly_sales = df.groupby(["Year", "Product"])["Units Sold"].sum().reset_index()
        yearly_sales = yearly_sales.sort_values(by="Year", ascending=True)
        
        # Calculate price sensitivity
        yearly_sales['Price Sensitivity'] = (
            yearly_sales.groupby("Product")['Units Sold']
            .pct_change() * 100
        )
        
        # Create subplot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add bars for each product
        for idx, product in enumerate(yearly_sales["Product"].unique()):
            product_data = yearly_sales[yearly_sales["Product"] == product]
            
            fig.add_trace(
                go.Bar(
                    x=product_data["Year"].astype(str),
                    y=product_data["Units Sold"],
                    name=product,
                    marker=dict(color=COLORS[idx % len(COLORS)])
                ),
                secondary_y=False
            )
        
        # Add price sensitivity line
        sensitivity_data = yearly_sales.groupby("Year")["Price Sensitivity"].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=sensitivity_data["Year"].astype(str),
                y=sensitivity_data["Price Sensitivity"],
                name="Price Sensitivity",
                mode="markers+lines",
                marker=dict(color=COLORS[-1])
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title="Sales Volume and Price Sensitivity Over Time",
            xaxis_title="Year",
            yaxis_title="Sales Volume",
            yaxis2_title="Price Sensitivity (%)",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in sales_volume_overtime: {str(e)}")
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )

def price_and_qty_overtime(data):
    """Analyze price and quantity relationships over time"""
    try:
        df = prepare_data(data)
        
        # Monthly aggregation
        monthly_data = df.groupby(["Month", "Year"]).agg({
            "Base Price": "mean",
            "Units Sold": "sum"
        }).reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces for each year
        for idx, year in enumerate(sorted(monthly_data["Year"].unique())):
            year_data = monthly_data[monthly_data["Year"] == year].copy()
            year_data.sort_values(by="Month", inplace=True)
            year_data["Month"] = year_data["Month"].apply(lambda x: MONTHS[x - 1])
            
            # Add base price bars
            fig.add_trace(
                go.Bar(
                    x=year_data["Month"],
                    y=year_data["Base Price"],
                    name=f'Avg. Base Price ({year})',
                    marker=dict(color=COLORS[idx % len(COLORS)])
                ),
                secondary_y=False
            )
            
            # Add units sold line
            fig.add_trace(
                go.Scatter(
                    x=year_data["Month"],
                    y=year_data["Units Sold"],
                    name=f'Units Sold ({year})',
                    mode="markers+lines",
                    line=dict(color=COLORS[(idx + 5) % len(COLORS)])
                ),
                secondary_y=True
            )
        
        # Update layout
        fig.update_layout(
            title="Base Price & Quantity Sold Over Time",
            xaxis_title="Month",
            yaxis_title="Base Price",
            yaxis2_title="Units Sold",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in price_and_qty_overtime: {str(e)}")
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )

def shipping_vs_tax_ratio(data):
    """Analyze the relationship between shipping/tax ratio and other metrics"""
    try:
        df = prepare_data(data)
        
        # Calculate shipping and tax ratio if not present
        if 'Shipping and Tax Ratio' not in df.columns and 'Shipping' in df.columns and 'Tax' in df.columns:
            df['Shipping and Tax Ratio'] = (df['Shipping'] + df['Tax']) / df['Base Price']
        
        # Create scatter plot
        fig = px.scatter(
            df,
            x="Shipping and Tax Ratio",
            y="Base Price",
            color="Units Sold",
            size="Units Sold",
            title="Impact of Shipping & Tax Ratio on Base Price and Units Sold",
            color_continuous_scale='viridis',
            hover_data=['Product', 'Date']
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest',
            xaxis_title="Shipping & Tax Ratio",
            yaxis_title="Base Price",
            coloraxis_colorbar_title="Units Sold"
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in shipping_vs_tax_ratio: {str(e)}")
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )