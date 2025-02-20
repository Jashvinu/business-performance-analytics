import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from constants import MONTHS
from utils import update_hover_layout


colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]


def income_statement(df):
    expense_columns = ['WageExp', 'AdSpend', 'BankFees', 'DepExp', 'Rent', 'Supplies', 'Utils',
                       'PayrollTax', 'OthExp']
    revenue_columns = ['Rev', 'ReturnAllow']

    df["Total Expense"] = df[expense_columns].sum(axis=1)
    df['Revenue'] = df[revenue_columns].sum(axis=1)

    fin_data = df.groupby("Year")['Total Expense', 'Profit or Loss', 'Revenue', 'CGS'].sum().reset_index()
    COLORS = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["Total Expense"], name="Total Expense",
               marker=dict(color=COLORS[0]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["CGS"], name="CoGS",
               marker=dict(color=COLORS[1]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["Revenue"], name="Revenue",
               marker=dict(color=COLORS[2]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["Profit or Loss"], name="Net Profit",
               marker=dict(color=COLORS[3]))
    )
    fig.update_layout(barmode="group", title="Income Statement", xaxis_title="Year",
                      yaxis_title="Amount", height=450)
    fig = update_hover_layout(fig)
    fig.update_xaxes(type='category')

    return fig


def debt_and_equity(df):
    debt_columns = ["AP", "AL", "TP", "WP", "NP", "Increase in TP", "Increase in WP"]
    shared_equity_columns = ["Stock", "Retained Earnings", "Distributable Earnings"]

    df['Total Debt'] = df[debt_columns].sum(axis=1)
    df['Shareholders Equity'] = df[shared_equity_columns].sum(axis=1)
    df['Debt to Equity Ratio'] = df['Total Debt'] / df['Shareholders Equity']

    fin_data = df.groupby("Year")['Total Debt', 'Shareholders Equity', 'Debt to Equity Ratio'].sum().reset_index()

    COLORS = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["Total Debt"], name="Total Debt",
               marker=dict(color=COLORS[0])), secondary_y=False
    )
    fig.add_trace(
        go.Bar(x=fin_data["Year"], y=fin_data["Shareholders Equity"], name="Shareholder's Equity",
               marker=dict(color=COLORS[1])), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=fin_data["Year"], y=fin_data["Debt to Equity Ratio"], name="Debt to Equity Ratio",
                   mode="markers+lines", marker=dict(color=COLORS[2])), secondary_y=True
    )
    fig.update_layout(barmode="group", title="Income Statement", xaxis_title="Year",
                      yaxis_title="Amount", height=450)

    fig.update_layout(
        title="Debt and Equity",
        xaxis_title="Year", height=450
    )
    fig = update_hover_layout(fig)
    fig.update_xaxes(type='category')
    fig.update_yaxes(title_text="Amount", secondary_y=False)
    fig.update_yaxes(title_text="Debt-to-Equity Ratio", secondary_y=True)

    return fig


import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Define months constant
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def clv_by_cac_chart(df):
    """
    Create a bar chart showing the ratio of Customer Lifetime Value to Customer Acquisition Cost.
    
    Args:
        df (pd.DataFrame): DataFrame containing 'CLTV Monetary Value', 'Discount', and 'Valuation Date' columns
    
    Returns:
        plotly.graph_objects.Figure: Bar chart of CLV/CAC ratio
    """
    try:
        # Create a copy to avoid modifying original dataframe
        df_copy = df.copy()
        
        # Validate required columns
        required_columns = ['CLTV Monetary Value', 'Discount', 'Valuation Date']
        if not all(col in df_copy.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df_copy.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Calculate ratio and handle division by zero
        df_copy["ratio"] = df_copy["CLTV Monetary Value"].div(
            df_copy["Discount"].replace(0, np.nan)
        )
        
        # Extract month and convert to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df_copy['Valuation Date']):
            df_copy['Valuation Date'] = pd.to_datetime(df_copy['Valuation Date'])
        
        df_copy['Month'] = df_copy['Valuation Date'].dt.month
        
        # Group by month and calculate mean ratio
        monthly_ratios = (df_copy.groupby("Month")["ratio"]
                         .mean()
                         .round(2)
                         .reset_index())
        
        # Convert month numbers to month names
        monthly_ratios['Month'] = monthly_ratios['Month'].apply(lambda x: MONTHS[x-1])
        
        # Sort by month order
        monthly_ratios['Month_Num'] = monthly_ratios['Month'].apply(lambda x: MONTHS.index(x))
        monthly_ratios = monthly_ratios.sort_values('Month_Num')
        
        # Create the visualization
        fig = go.Figure(
            data=go.Bar(
                x=monthly_ratios["Month"],
                y=monthly_ratios["ratio"],
                marker=dict(
                    color="#006d77",
                    pattern_shape="/"  # Add pattern for better visibility
                ),
                text=monthly_ratios["ratio"].round(2),
                textposition='auto',
                hovertemplate="Month: %{x}<br>" +
                             "CLTV/CAC: %{y:.2f}<br>" +
                             "<extra></extra>"
            )
        )
        
        # Update layout
        fig.update_layout(
            title={
                'text': "Customer Lifetime Value to Acquisition Cost Ratio",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Month",
            yaxis_title="CLTV:CAC Ratio",
            showlegend=False,
            hovermode='x unified',
            template='plotly_white',
            height=500,
            margin=dict(l=50, r=20, t=70, b=50),
            yaxis=dict(
                tickformat=".2f",
                gridcolor='lightgray'
            )
        )
        
        # Add reference line at ratio = 1
        fig.add_hline(
            y=1, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Break-even ratio (1:1)",
            annotation_position="bottom right"
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating CLV/CAC chart: {str(e)}")
        # Return a figure with error message
        return go.Figure().add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )