import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import update_hover_layout
from constants import MONTHS

colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]


def price_elasticity_overtime(data):
    data = data.groupby(["Year", "Product"])["Price Elasticity"].mean().reset_index()
    fig = go.Figure()
    ind = 0
    for prod in data['Product'].unique():
        prod_data = data[data["Product"] == prod]
        fig.add_trace(
            go.Bar(
                y=prod_data["Year"],
                x=prod_data["Price Elasticity"],
                name=f"{prod}",
                marker=dict(color=colors[ind]),
                orientation="h", hovertext="dP/dQ = " + round(prod_data["Price Elasticity"], 2).astype(str)
            )
        )
        ind += 1
    fig.update_yaxes(type='category')
    fig.update_layout(
        title="Average Price Elasticity By Year",
        xaxis_title="Price Elasticity",
        yaxis_title="Year",
    )
    fig = update_hover_layout(fig)
    return fig


def elasticity_vs_base_price(data):
    fig = px.scatter(
        data,
        x="Base Price",
        y="Price Elasticity",
        color="Product",
        size="Units Sold",
        animation_frame="Year",
        title="Price Elasticity vs. Base Price"
    )
    fig.update_yaxes(type="log")
    fig = update_hover_layout(fig)
    return fig


def shipping_vs_tax_ratio(data):
    fig = px.scatter(
        data,
        x="Shipping and Tax Ratio",
        y="Base Price",
        color="Units Sold",
        size="Units Sold",
        title="Impact of Shipping Ratio on Base Price and Units Sold",
        color_continuous_scale='viridis'
    )
    fig = update_hover_layout(fig)
    return fig


def sales_volume_overtime(data):
    data = data.groupby(["Year", "Product"])["Units Sold"].sum().reset_index()
    data = data.sort_values(by="Year", ascending=True)
    data['Price Sensitivity'] = (data['Units Sold'] - data['Units Sold'].shift(1)) / data['Units Sold'].shift(1) * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    ind = 0
    for product in data["Product"].unique():
        product_data = data[data["Product"] == product]
        fig.add_trace(
            go.Bar(
                x=product_data["Year"],
                y=product_data["Units Sold"],
                name=product,
                marker=dict(color=colors[ind])
            ),
            secondary_y=False
        )
        ind += 1

    price_sen_data = data.groupby("Year")["Price Sensitivity"].mean().reset_index()
    fig.add_trace(
        go.Scatter(
            x=price_sen_data["Year"],
            y=price_sen_data["Price Sensitivity"],
            name="Price Sensitivity",   
            mode="markers+lines",
            marker=dict(color=colors[ind])
        ),
        secondary_y=True
    )

    fig.update_xaxes(type='category')
    fig.update_layout(
        title="Sales Volume Over Years by Product",
        xaxis_title="Year",
        yaxis_title="Sales Volume",
        barmode='group'
    )
    fig = update_hover_layout(fig)
    return fig


def price_and_qty_overtime(data):
    data = data.groupby(["Month", "Year"]).agg(
        {"Base Price": "mean",
         "Units Sold": "sum"}
    ).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    ind = 0
    for year in data["Year"].unique():
        year_df = data[data["Year"] == year]
        year_df.sort_values(by="Month", inplace=True)
        year_df["Month"] = year_df["Month"].apply(lambda x: MONTHS[x - 1])
        fig.add_trace(
            go.Bar(x=year_df["Month"], y=year_df["Base Price"], marker=dict(color=colors[ind]),
                   name=f'Avg. Base Price ({year})'), secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=year_df["Month"], y=year_df["Units Sold"], line=dict(color=colors[ind + 5]),
                       marker=dict(color=colors[ind + 5]), mode="markers+lines", name=f'#Units ({year})'),
            secondary_y=True
        )
        ind += 1
    fig.update_layout(
        title="Base Price & Qty Sold Over Time",
        xaxis_title="Month",
        # yaxis_title="Qty",
        # show_legend = False
    )
    fig = update_hover_layout(fig)
    return fig
