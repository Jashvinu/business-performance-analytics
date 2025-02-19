import pandas as pd
import plotly.graph_objects as go
from utils import update_hover_layout
from constants import MONTHS


def monthly_gross_rev(filtered_data):
    filtered_data['Month'] = filtered_data['Valuation Date'].dt.month
    revenue_data = filtered_data.groupby("Month")["Total Revenue_y", "Gross Profit"].sum().reset_index()
    revenue_data["Month"] = revenue_data["Month"].apply(lambda x: MONTHS[x-1])
    revenue_data.sort_values(by="Month", inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=revenue_data["Month"], y=revenue_data["Total Revenue_y"], mode="lines+markers+text",
        marker=dict(color="#e76f51"), line=dict(color="#e76f51"), textposition="top center", name="Revenue"))
    fig.add_trace(go.Scatter(
        x=revenue_data["Month"], y=revenue_data["Gross Profit"], mode="lines+markers",
        marker=dict(color="#264653"), line=dict(color="#264653"), textposition="top center", name="Profit Margin"))
    fig.update_layout(title="Revenue/G.Profit Over Time", xaxis_title="Month", yaxis_title="Amount", height=400)
    fig = update_hover_layout(fig)
    return fig


def cost_breakdown_chart(filtered_data):
    filtered_data['Month'] = filtered_data['Valuation Date'].dt.month
    costs_data = filtered_data.groupby("Month")["Shipping Amount", "Tax", "Discount"].sum().reset_index()
    costs_data["Month"] = costs_data["Month"].apply(lambda x: MONTHS[x-1])
    costs_data.sort_values(by="Month", inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=costs_data["Month"], y=costs_data["Shipping Amount"], name="Shipping",
                         marker=dict(color="#264653")))
    fig.add_trace(go.Bar(x=costs_data["Month"], y=costs_data["Tax"], name="Tax", marker=dict(color="#2a9d8f")))
    fig.add_trace(go.Bar(x=costs_data["Month"], y=costs_data["Discount"], name="Discount",
                         marker=dict(color="#e9c46a")))
    fig.update_layout(title="Cost Breakdown", barmode="stack", legend_title="Costs", xaxis_title="Month",
                      yaxis_title="Cost Amount", height=400)
    fig = update_hover_layout(fig)
    return fig


def sales_by_location(filtered_data):
    loc_data = filtered_data.groupby("Conversion Country")["Total Revenue_y", "Gross Profit"].sum().reset_index()
    loc_data = loc_data.sort_values(by="Total Revenue_y", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=loc_data["Conversion Country"], y=loc_data["Total Revenue_y"], name="Revenue",
        text=round(loc_data["Total Revenue_y"], 1), marker=dict(color="#287271"),
    ))
    fig.add_trace(go.Bar(
        x=loc_data["Conversion Country"], y=loc_data["Gross Profit"], name="Gross Profit",
        text=round(loc_data["Gross Profit"], 1), marker=dict(color="#babb74"),
    ))
    fig.update_layout(title="Sales by Location", barmode="group", legend_title="Sales",
                      xaxis_title="Country", yaxis_title="Total Revenue_y")
    fig = update_hover_layout(fig)
    return fig


def rev_by_products(filtered_data):
    product_performance = filtered_data.groupby('Product Item Name')['Total Revenue_y'].sum().reset_index()
    product_performance = product_performance.sort_values(by="Total Revenue_y", ascending=False)
    product_performance["Product Item Name"] = product_performance["Product Item Name"].str[16:]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=product_performance["Product Item Name"],
        y=product_performance["Total Revenue_y"],
        marker=dict(color="#55b1a5"),
    ))
    fig.update_layout(
        title="Product Performance", xaxis_title="Product Name", yaxis_title="Total Revenue_y",
        xaxis_tickangle=-45,
    )
    fig = update_hover_layout(fig)
    return fig

