import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import update_hover_layout
from constants import MONTHS
import streamlit as st

colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]


def expense_treemap(data):
    expenses_cols = ["WageExp", "AdSpend", "ReturnAllow", "CGS", "BankFees", "DepExp",
                     "Rent", "Supplies", "Utils", "PayrollTax", "OthExp", "IncomeTax"]
    expense_data = data[expenses_cols + ["Valuation Date"]]
    melted_df = pd.melt(expense_data, id_vars=["Valuation Date"], var_name="Expense", value_name="Amount")
    melted_df = melted_df.groupby("Expense")["Amount"].sum().reset_index()
    melted_df = melted_df.sort_values(by="Amount")
    fig = px.treemap(melted_df, path=['Expense'], values='Amount', title="Expenses Overview",
                     color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3",
                                              "teal", "silver", "#f2cc8f", "#81b29a"])
    fig = update_hover_layout(fig)
    fig.update_layout(height=500)
    return fig


def expenses_by_category(df):
    operating_expense = df[["WageExp", "AdSpend", "BankFees", "DepExp", "Rent",
                            "Supplies", "Utils", "PayrollTax", "OthExp"]].sum(axis=1).sum()
    cogs = df["CGS"].sum()
    rev_allowances = df[["Rev", "ReturnAllow"]].sum(axis=1).sum()
    tax_expense = df["IncomeTax"].sum()
    data = pd.DataFrame({
        "Expense": ["Operating Expense", "CoGS", "Revenue & Allowance", "Tax Expense"],
        "Amount": [operating_expense, cogs, rev_allowances, tax_expense]
    })
    fig = go.Figure(
        go.Pie(
            labels=data["Expense"], values=data["Amount"],
            marker=dict(colors=colors)
        )
    )
    fig.update_yaxes(title="Expenses")
    fig.update_yaxes(title="Amount")
    fig.update_layout(title="Expense Breakdown")
    fig = update_hover_layout(fig)
    fig.update_layout(height=500)
    return fig


def cashflows_pie(df):
    cash_flow_columns = [
        'Cash', 'Cash for Payroll', 'Petty Cash', 'Marketable Securities',
        'AR', 'Inventory', 'Allow', 'Prepaid', 'FixAsset', 'AccumDep',
        'OtherAssets', 'AP', 'AL', 'TP', 'NP', 'WP', 'Stock', 'Retained Earnings',
        'Distributable Earnings', 'Net Earnings', 'Increase in TP', 'Increase in WP',
        'Decrease in AR', 'Depreciations', 'Increase in Inventory', 'Increase Marketable Securities',
        'Increase Allowance for Bad Debt', 'Increase Prepaid Expenses', 'Net Asset Acquisitions',
        'Net Asset Sale', 'Notes Payable', 'Decrease in Note Payable', 'New Stock Sold',
        'New Stock Repurchase'
    ]

    df['Total Cash Flow'] = df[cash_flow_columns].sum(axis=1)

    operating_cash_flow_columns = [
        'WageExp', 'AdSpend', 'Rev', 'ReturnAllow', 'CGS', 'BankFees', 'DepExp', 'Rent',
        'Supplies', 'Utils', 'PayrollTax', 'OthExp', 'Income Before Tax', 'IncomeTax',
        'Increase in TP', 'Increase in WP', 'Decrease in AR', 'Depreciations',
        'Increase in Inventory', 'Increase Allowance for Bad Debt', 'Increase Prepaid Expenses'
    ]

    df['Operating Cash Flow'] = df[operating_cash_flow_columns].sum(axis=1)

    investing_cash_flow_columns = [
        'FixAsset', 'Net Asset Acquisitions', 'Net Asset Sale', 'Marketable Securities',
        'Increase Marketable Securities'
    ]

    df['Investing Cash Flow'] = df[investing_cash_flow_columns].sum(axis=1)

    financing_cash_flow_columns = [
        'NP', 'Decrease in Note Payable', 'New Stock Sold', 'New Stock Repurchase'
    ]

    df['Financing Cash Flow'] = df[financing_cash_flow_columns].sum(axis=1)

    data = {
        'Category': ['Total Cash Flow', 'Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow'],
        'Amount': [df['Total Cash Flow'].sum(), df['Operating Cash Flow'].sum(),
                   df['Investing Cash Flow'].sum(), df['Financing Cash Flow'].sum()]
    }

    data = pd.DataFrame(data)
    fig = px.pie(data, names='Category', values='Amount', title='Cash Flow Breakdown',
                 color_discrete_sequence=colors[1:])
    fig = update_hover_layout(fig)
    return fig


def cashflow_chart(df):
    df["Cash Going In"] = df[['Rev', 'ReturnAllow', 'New Stock Sold', 'Net Asset Acquisitions']].sum(axis=1)
    df["Cash Going Out"] = df[
        ['WageExp', 'AdSpend', 'CGS', 'DepExp', 'Rent', 'Supplies', 'Utils', 'PayrollTax', 'OthExp', 'IncomeTax',
         'NP', 'AP', 'New Stock Repurchase']].sum(axis=1)

    monthly_cashflow = df.groupby("Month")['Cash', 'Cash Going In', 'Cash Going Out'].agg(
        {'Cash': 'last', 'Cash Going In': 'sum', 'Cash Going Out': 'sum'}
    )
    monthly_cashflow = monthly_cashflow.reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                                 'Sep', 'Oct', 'Nov', 'Dec']).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=monthly_cashflow["Month"], y=monthly_cashflow["Cash Going In"], name="Cash Going In",
               marker=dict(color=colors[0]))
    )
    fig.add_trace(
        go.Bar(x=monthly_cashflow["Month"], y=monthly_cashflow["Cash Going Out"], name="Cash Going Out",
               marker=dict(color=colors[1])), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=monthly_cashflow["Month"], y=monthly_cashflow["Cash"], name="Ending Cash On Hand",
                   mode="lines+markers", marker=dict(color=colors[2])), secondary_y=True
    )
    fig.update_yaxes(title="Month")
    fig.update_yaxes(title="Amount", secondary_y=False)
    fig.update_yaxes(title="Cash", secondary_y=True)
    fig.update_layout(title="Cash Flow")
    fig = update_hover_layout(fig)
    return fig



def create_indicator_plot(df, column, title, color):
    # Prepare the data
    monthly_data = df.groupby("Month")[column].sum()
    monthly_cashflow = monthly_data.reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                             'Sep', 'Oct', 'Nov', 'Dec']).reset_index()

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=monthly_cashflow["Month"], y=monthly_cashflow[column],
                   name=title, mode="lines", fill='tozeroy',
                   marker=dict(color=color))
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=monthly_cashflow[column].sum(),
            number={"prefix": "$"},
            title={"text": title, "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        )
    )
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    return fig


def ar_indicator(df):
    return create_indicator_plot(df, 'AR', 'Accounts Receivable', "#bde0fe")


def ap_indicator(df):
    df["AP"] = df["AP"].replace(',', '', regex=True).astype(float)
    return create_indicator_plot(df, 'AP', 'Accounts Payable', "#ffadad")


def profit_loss_chart(df):
    monthly_data = df.groupby("Month")['Profit or Loss'].sum()
    monthly_cashflow = monthly_data.reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                             'Sep', 'Oct', 'Nov', 'Dec']).reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=monthly_cashflow["Month"], y=monthly_cashflow["Profit or Loss"], name="Profit/Loss",
               marker=dict(color=colors[0]))
    )
    fig.update_yaxes(title="Month")
    fig.update_yaxes(title="Amount")
    fig.update_layout(title="Profit Loss Analysis")
    fig = update_hover_layout(fig)
    return fig
