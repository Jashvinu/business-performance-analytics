import pandas as pd
import streamlit as st

from plots.accounts import ar_indicator, ap_indicator, profit_loss_chart, cashflow_chart, cashflows_pie, \
    expenses_by_category, expense_treemap
from plots.customer_report import cltv_by_month, rev_by_dash_segment, churn_by_dash_segment, sales_by_dash_segment, \
    conversion_and_purchase_rates, rev_by_loyalty_group, churn_wrt_loyalty, group_analysis
from plots.marketing import event_seq_funnel, event_seq_pie, channels_performance, aov_by_channels, channel_funnel
from plots.overview import clv_by_cac_chart, debt_and_equity, income_statement
from plots.sales_report import monthly_gross_rev, cost_breakdown_chart, sales_by_location, rev_by_products
from plots.demand_elasticity import (price_elasticity_overtime, elasticity_vs_base_price,
                                     shipping_vs_tax_ratio, price_and_qty_overtime, sales_volume_overtime)
from utils import current_and_previous_data, get_overview_kpis, get_conversion_rate, \
    get_aov, tax_amount, gross_profit_margin, get_discount_rate, shipping_amount, get_conv_rate, get_visitor_engagement, \
    format_currency_label
from constants import MONTHS


def overview(customers_sales_data, cash_flow_data):
    # -------------------------------- Filters ----------------------------------
    year = st.sidebar.selectbox(label="Year", options=sorted(set(customers_sales_data["Year"].values)))
    # ------------------------------- Data --------------------------------------
    current_data, previous_data = current_and_previous_data(data=customers_sales_data, y=year,
                                                            years=list(sorted(set(customers_sales_data["Year"].values))))
    # ------------------------------- KPIs --------------------------------------
    num_of_customers, clv, avg_lsp, avg_arpu, churning = get_overview_kpis(current_data, previous_data)
    kpi_row = st.columns(5)
    kpi_row[0].plotly_chart(num_of_customers, use_container_width=True)
    kpi_row[1].plotly_chart(clv, use_container_width=True)
    kpi_row[2].plotly_chart(avg_lsp, use_container_width=True)
    kpi_row[3].plotly_chart(avg_arpu, use_container_width=True)
    kpi_row[4].plotly_chart(churning, use_container_width=True)

    row_1 = st.columns(2)
    # Income Statement
    row_1[0].plotly_chart(income_statement(cash_flow_data), use_container_width=True)
    # Debt to Equity Ratio
    row_1[1].plotly_chart(debt_and_equity(cash_flow_data), use_container_width=True)
    # CLV:CAC chart
    df = customers_sales_data[customers_sales_data["Year"] == year]
    st.plotly_chart(clv_by_cac_chart(df), use_container_width=True)


def sales_insights(data):
    # ----------------------------------- Filters -------------------------------
    year = st.sidebar.selectbox(label="Year", options=sorted(set(data["Year"].values)))
    data = data[data["Year"] == year]
    # ----------------------------------- KPIs ----------------------------------
    kpis = st.columns(6)
    kpis[0].metric(label="Conversion Rate", value=f"{get_conversion_rate(data):.1f}%")
    kpis[1].metric(label="Average Order Value", value=f"{get_aov(data):.1f}")
    kpis[2].metric(label="Shipping Amount as %Revenue", value=f"{shipping_amount(data):.1f}%")
    kpis[3].metric(label="Tax Amount as  %Revenue", value=f"{tax_amount(data):.1f}%")
    kpis[4].metric(label="Gross Profit Margin", value=f"{gross_profit_margin(data):.1f}%")
    kpis[5].metric(label="Discount Rate", value=f"{get_discount_rate(data):.1f}%")
    # ------------------------------ Visuals ------------------------------------
    row_1 = st.columns(2)
    # Revenue/Gross Profit
    row_1[0].plotly_chart(monthly_gross_rev(data), use_container_width=True)
    # Cost Breakdown
    row_1[1].plotly_chart(cost_breakdown_chart(data), use_container_width=True)
    # Sales by Location
    row_1[0].plotly_chart(sales_by_location(data), use_container_width=True)
    # Product Performance
    row_1[1].plotly_chart(rev_by_products(data), use_container_width=True)


def customer_report(data):
    # ----------------------------------- Filters -------------------------------
    year = st.sidebar.selectbox(label="Year", options=sorted(set(data["Year"].values)))
    # month = st.sidebar.multiselect(label="Month", options=months,
    #                                placeholder="All")
    data = data[data["Year"] == year]
    data["Churn"] = data["P notAlive"].apply(lambda x: 1 if x > 0.5 else 0)
    # ---------------------------- Visuals ----------------------------
    row_1 = st.columns(2)
    # Churn & Revenue Analysis/Dash Segment
    row_1[0].plotly_chart(group_analysis(data, "Dash Segment"), use_container_width=True)
    # Churn & Revenue Analysis/Loyalty Groups
    row_1[1].plotly_chart(group_analysis(data, "Loyalty Group"), use_container_width=True)

    # Churn Analysis/Dash Segment
    # row_1[0].plotly_chart(churn_by_dash_segment(data), use_container_width=True)
    # # Dash Segment Analysis
    # row_1[1].plotly_chart(rev_by_dash_segment(data), use_container_width=True)
    # # Churn Analysis/Loyalty Groups
    # row_1[2].plotly_chart(churn_wrt_loyalty(data), use_container_width=True)
    # # Loyalty Group
    # row_1[3].plotly_chart(rev_by_loyalty_group(data), use_container_width=True)

    row_2 = st.columns(2)
    # Average CLTV by Month
    row_2[0].plotly_chart(cltv_by_month(data), use_container_width=True)
    # Sales by Loyalty Groups
    row_2[1].plotly_chart(sales_by_dash_segment(data), use_container_width=True)
    # Conversion Rate & Repeat Purchase Rate
    st.plotly_chart(conversion_and_purchase_rates(data), use_container_width=True)


def demand_elasticity(data):
    # --------------------------- Pre-processing -----------------------------
    data['Date'] = pd.to_datetime(data['Key'].str[:10])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data = data.sort_values(by="Date")

    data["Price Change"] = data["Price Ratio"].pct_change()
    data["Quantity Change"] = data["Units Sold"].pct_change()
    data["Price Elasticity"] = data["Quantity Change"] / data["Price Change"]

    product = st.sidebar.multiselect(label="Product", options=set(data["Product"].values))
    if not product:
        product = set(data["Product"].values)

    data = data[data["Product"].isin(product)]

    # --------------------------- Filters ------------------------------------
    year = st.sidebar.multiselect(label="Year", options=sorted(set(data["Year"].values)),
                                  placeholder="All")
    if not year:
        year = list(sorted(set(data["Year"].values)))

    filtered_data = data.copy()
    if year:
        filtered_data = data[data["Year"].isin(year)]

    # --------------------------- KPIs ---------------------------------------
    first_row = st.columns((2, 1))
    first_row[0].plotly_chart(elasticity_vs_base_price(filtered_data), use_container_width=True)
    first_row[1].plotly_chart(price_elasticity_overtime(filtered_data), use_container_width=True)

    second_row = st.columns(2)
    second_row[0].plotly_chart(shipping_vs_tax_ratio(filtered_data), use_container_width=True)
    second_row[1].plotly_chart(sales_volume_overtime(filtered_data), use_container_width=True)

    st.plotly_chart(price_and_qty_overtime(filtered_data), use_container_width=True)


def marketing_attribution(market_data, media_data):
    kpis_row = st.columns(5)
    conversion_rate = get_conv_rate(market_data)
    visitor_engagement = get_visitor_engagement(market_data)
    kpis_row[1].metric(label="Average Order Value", value=f"${market_data['AOV'].mean():.2f}")
    kpis_row[2].metric(label="Total Revenue", value=f"${market_data['AOV'].sum():.1f}")
    kpis_row[3].metric(label="Visitor's Engagement Rate", value=f"{visitor_engagement:.2f}")

    st.write("---")
    row_1 = st.columns(2)

    # Event Sequence Funnel
    row_1[1].plotly_chart(event_seq_funnel(market_data), use_container_width=True)
    # AOV w.r.t Event Sequence
    row_1[0].plotly_chart(event_seq_pie(market_data), use_container_width=True)
    # Spend and Conversion w.r.t Channels
    st.plotly_chart(channel_funnel(media_data, market_data), use_container_width=True)

    # Channels Performance
    row_2 = st.columns(2)
    row_2[0].plotly_chart(channels_performance(market_data), use_container_width=True)
    # AOV w.r.t Channels
    row_2[1].plotly_chart(aov_by_channels(market_data), use_container_width=True)


def accounts(data):
    year = st.sidebar.multiselect(label="Year", options=sorted(set(data["Year"].values)), placeholder="All")
    if not year:
        year = sorted(set(data["Year"].values))
    df = data[data['Year'].isin(year)]
    df = df.sort_values(by="Valuation Date")
    income_data = data[data["Year"].isin(year)]

    # KPIs
    kpi_row = st.columns(6)

    income_data['Gross Profit Margin'] = ((income_data['Rev'] - income_data['CGS']) / income_data['Rev']) * 100
    income_data['Operating Profit Margin'] = ((income_data['Income Before Tax'] - income_data['DepExp']
                                               - income_data['BankFees'] - income_data['Rent'] -
                                               income_data['Supplies'] - income_data['Utils'] -
                                               income_data['PayrollTax'] -
                                               income_data['OthExp']) / income_data['Income Before Tax']) * 100
    income_data['Net Profit Margin'] = ((income_data['Income Before Tax'] -
                                         income_data['IncomeTax']) / income_data['Income Before Tax']) * 100
    income_data['ROI'] = ((income_data['Profit or Loss']) / (income_data['WageExp'] + income_data['AdSpend'])) * 100
    income_data['Expense-to-Revenue Ratio'] = ((income_data['DepExp'] + income_data['BankFees'] +
                                                income_data['Rent'] + income_data['Supplies'] +
                                                income_data['Utils'] + income_data['PayrollTax'] +
                                                income_data['OthExp']) / income_data['Rev']) * 100
    income_data['ROA'] = ((income_data['Profit or Loss']) / income_data['Income Before Tax']) * 100

    gps = income_data['Gross Profit Margin'].mean()
    opm = income_data['Operating Profit Margin'].mean()
    npm = income_data['Net Profit Margin'].mean()
    roi = income_data['ROI'].mean()  # Return on Investment (ROI)
    etrr = income_data['Expense-to-Revenue Ratio'].mean()  # Expense-to-Revenue Ratio
    roa = income_data['ROA'].mean()  # Return on Assets (ROA)

    kpi_row[0].metric(label="Gross Profit Margin", value=f"{gps:.1f}%")
    kpi_row[1].metric(label="Operating Profit Margin", value=f"{opm:.1f}%")
    kpi_row[2].metric(label="Net Profit Margin", value=f"{npm:.1f}%")
    kpi_row[3].metric(label="ROI", value=f"{roi:.1f}%")
    kpi_row[4].metric(label="Expense/Revenue", value=f"{etrr:.1f}%")
    kpi_row[5].metric(label="ROA", value=f"{roa:.1f}%")

    top_row = st.columns((3, 2))
    # Expense Treemap
    top_row[0].plotly_chart(expense_treemap(income_data), use_container_width=True)
    # Expense Categorization
    top_row[1].plotly_chart(expenses_by_category(df), use_container_width=True)

    st.write("---")

    # Cash Flow
    beginning_cash = df['Cash'].iloc[0]
    cash_going_in = df[['Rev', 'ReturnAllow', 'New Stock Sold', 'Net Asset Acquisitions']].sum(axis=1).sum()
    cash_going_out = df[['WageExp', 'AdSpend', 'CGS', 'DepExp', 'Rent', 'Supplies', 'Utils',
                         'PayrollTax', 'OthExp', 'IncomeTax', 'NP', 'AP',
                         'New Stock Repurchase']].sum(axis=1).sum()
    profit_loss = df['Profit or Loss'].sum()
    ending_cash = beginning_cash + cash_going_in - cash_going_out
    cash_metric = st.columns(5)
    cash_metric[0].metric(label="Beginning Cash", value=f"{format_currency_label(beginning_cash)}")
    cash_metric[1].metric(label="Cash Going In", value=f"{format_currency_label(cash_going_in)}")
    cash_metric[2].metric(label="Cash Going Out", value=f"{format_currency_label(cash_going_out)}")
    cash_metric[3].metric(label="Profit/Loss", value=f"{format_currency_label(profit_loss)}")
    cash_metric[4].metric(label="Ending Cash", value=f"{format_currency_label(ending_cash)}")

    cashflow_row = st.columns((3, 2))
    monthly_cashflow = cashflow_chart(df)
    cashflow_breakdown = cashflows_pie(df)
    cashflow_row[0].plotly_chart(monthly_cashflow, use_container_width=True)
    cashflow_row[1].plotly_chart(cashflow_breakdown, use_container_width=True)

    # AR/AP
    mid_row_1, mid_row_2 = st.columns(2)
    accounts_receivable = ar_indicator(df)
    accounts_payable = ap_indicator(df)
    profit_loss = profit_loss_chart(df)
    with mid_row_1:

        ind_col = st.columns(2)
        ind_col[0].plotly_chart(ar_indicator(df), use_container_width=True)
        ind_col[1].plotly_chart(ap_indicator(df), use_container_width=True)
    mid_row_2.plotly_chart(profit_loss, use_container_width=True)

