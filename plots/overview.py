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


def clv_by_cac_chart(df):
    df["ratio"] = df["CLTV Monetary Value"] / df["Discount"]
    df['Month'] = df['Valuation Date'].dt.month
    df = df.groupby("Month")["ratio"].mean().reset_index()
    df['Month'] = df['Month'].apply(lambda x: MONTHS[x-1])
    fig = go.Figure(
        data=go.Bar(
            x=df["Month"], y=df["ratio"], marker=dict(color="#006d77"), text=round(df["ratio"], 2),
            hovertext="CLTV/CAC = " + " " + round(df["ratio"], 1).astype(str)
        )
    )
    fig.update_layout(
        title="Customer Lifetime Value/Cost per Acquired Customer Over Time",
        xaxis_title="Month",
        yaxis_title="CLTV:CAC",
    )
    fig = update_hover_layout(fig)
    return fig
