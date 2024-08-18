import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import update_hover_layout
from constants import MONTHS


def churn_wrt_loyalty(data):
    loyalty_churn = data.groupby("Loyalty Group")["Churn"].sum().reset_index()
    loyalty_churn = loyalty_churn.sort_values(by="Churn")
    fig = go.Figure(
        go.Bar(
            x=loyalty_churn["Loyalty Group"], y=loyalty_churn["Churn"], name="Churned Customers",
            marker=dict(color="#81b29a")
        )
    )
    fig = update_hover_layout(fig)
    return fig


def churn_by_dash_segment(data):
    fig = px.pie(data_frame=data, names="Dash Segment", values="Churn", labels="value+percent",
                 title="Customer Churn w.r.t Dash Segment", hole=0.3,
                 color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3",
                                          "teal", "silver", "#f2cc8f", "#81b29a"])
    fig = update_hover_layout(fig)
    return fig


def sales_by_dash_segment(data):
    data["Month"] = data["Month"].apply(lambda x:MONTHS[x-1])
    revenue_by_loyalty_and_month = data.groupby(["Dash Segment", "Month"])['CLTV Monetary Value'].sum().unstack()
    revenue_by_loyalty_and_month = revenue_by_loyalty_and_month.transpose()
    fig = go.Figure()
    colors = ["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3"]
    x = 0
    for i in revenue_by_loyalty_and_month.columns:
        fig.add_trace(go.Bar(
            x=revenue_by_loyalty_and_month.index,
            y=revenue_by_loyalty_and_month[i],
            name=i,
            marker=dict(color=colors[x])
        ))
        x += 1
    fig = update_hover_layout(fig)
    fig.update_xaxes(categoryorder='array', categoryarray=MONTHS)
    fig.update_layout(title="Sales w.r.t Dash Segment")
    return fig


def rev_by_dash_segment(data):
    revenue_by_dash_segment = data.groupby('Dash Segment')['Total Revenue'].sum().reset_index()
    fig = px.pie(
        revenue_by_dash_segment,
        names=revenue_by_dash_segment["Dash Segment"],
        values=revenue_by_dash_segment["Total Revenue"],
        title="Revenue Contribution by Dash Segment",
        hole=0.3, color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3"]
    )
    fig = update_hover_layout(fig)
    return fig


def group_analysis(data, group):
    # Revenue by Group
    revenue_by_dash_segment = data.groupby(group)['Total Revenue'].sum().reset_index()
    revenue_pie = go.Pie(
        labels=revenue_by_dash_segment[group],
        values=revenue_by_dash_segment["Total Revenue"],
        # title="Revenue",
        hole=0.3,
        marker=dict(colors=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3", "#eddea4", "#f2bf8b"])
    )

    # Customer Churn by Group
    churn_pie = go.Pie(
        labels=data[group],
        values=data["Churn"],
        # title="Churn",
        hole=0.3,
        marker=dict(colors=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3", "#eddea4", "#f2bf8b"])
    )

    # Subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=("Revenue", "Churn"))

    # Adding traces to the subplot
    fig.add_trace(revenue_pie, 1, 1)
    fig.add_trace(churn_pie, 1, 2)

    fig.update_layout(
        title_text=f"{group} Breakdown",
        showlegend=True,
    )

    return fig


def rev_by_loyalty_group(data):
    revenue_by_loyalty = data.groupby('Loyalty Group')['Total Revenue'].sum().reset_index().rename(
        {"Total Revenue": "Contribution"}, axis=1
    )
    fig = px.pie(
        revenue_by_loyalty,
        names=revenue_by_loyalty["Loyalty Group"],
        values=revenue_by_loyalty["Contribution"],
        labels="percent+label",
        hole=0.3, color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3"]
    )
    fig.update_layout(
        title="Revenue Contribution by Loyalty Groups",
    )
    fig = update_hover_layout(fig)
    return fig


def cltv_by_month(data):
    data["Month"] = data["Valuation Date"].dt.month
    avg_cltv_by_month = data.groupby('Month')['CLTV Monetary Value'].mean().reset_index()
    avg_cltv_by_month["Month"] = avg_cltv_by_month["Month"].apply(lambda x: MONTHS[x - 1])
    fig = go.Figure(
        go.Bar(
            x=avg_cltv_by_month["Month"],
            y=avg_cltv_by_month["CLTV Monetary Value"],
            marker=dict(color="#2a9d8f"),
            text=round(avg_cltv_by_month["CLTV Monetary Value"], 2),
            hovertext="Avg. CLTV=" + round(avg_cltv_by_month["CLTV Monetary Value"], 2).astype(str),
        )
    )
    fig.update_layout(
        title="Average CLTV by Month", xaxis_title="Month", yaxis_title="Average CLTV",
    )
    fig = update_hover_layout(fig)
    return fig


def conversion_and_purchase_rates(data):
    data["Month"] = data["Valuation Date"].dt.month
    con_rate = data.groupby('Month')['Customer ID'].nunique().reset_index()
    conversion = data['Month'].value_counts().reset_index()
    conversion.rename(columns={"index": "Month", "Month": "num_conversion"}, inplace=True)
    con_rate = pd.merge(con_rate, conversion, on="Month")
    con_rate["conversion_rate"] = (con_rate["Customer ID"] / con_rate["num_conversion"]) * 100
    con_rate.sort_values(by="Month", inplace=True)
    con_rate["Month"] = con_rate["Month"].apply(lambda x: MONTHS[x - 1])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=con_rate['Month'],
        y=con_rate['conversion_rate'],
        name='Conversion Rate', marker=dict(color="#006d77"),
        text=con_rate['conversion_rate'].apply(lambda rate: f"{round(rate, 2)}%"),
    ))

    purchase_counts = data.groupby(['Customer ID', 'Month']).size().reset_index(name='purchase_count')
    purchase_counts = purchase_counts[purchase_counts['purchase_count'] > 1]

    total_customers = purchase_counts.groupby('Month')['Customer ID'].nunique().reset_index()
    purchase_counts = purchase_counts.groupby("Month")["purchase_count"].sum().reset_index()
    repeat_purchase = pd.merge(purchase_counts, total_customers, on="Month")
    repeat_purchase["repeat_purchase_rate"] = (repeat_purchase["Customer ID"] / repeat_purchase[
        "purchase_count"]) * 100
    repeat_purchase.sort_values(by="Month", inplace=True)
    repeat_purchase["Month"] = repeat_purchase["Month"].apply(lambda x:MONTHS[x-1])

    fig.add_trace(go.Bar(
        x=repeat_purchase["Month"],
        y=repeat_purchase["repeat_purchase_rate"],
        text=repeat_purchase['repeat_purchase_rate'].apply(lambda rate: f"{round(rate, 2)}%"),
        textposition='auto', marker=dict(color="#52b69a"),
        name="Repeat Purchase Rate"
    ))
    fig.update_layout(
        title="Conversion & Repeat Purchase Rate by Month",
        xaxis_title="Month",
        yaxis_title="Rate (%)",
    )
    fig = update_hover_layout(fig)
    return fig
