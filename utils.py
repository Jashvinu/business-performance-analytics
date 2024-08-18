import os
import pandas as pd
import plotly.graph_objects as go
from plots.kpis import get_num_of_customers, get_clv, average_life_span, average_arpu, churn_rate
from constants import MONTHS

      
def preprocess_data(data_list: list) -> list:
    """
    Preprocesses the data by formatting date column
    to contain values of datetime data-type
    :param data_list: the list of dataframes with date column
    :return: list of dataframes with formatted date columns
    """
    for df in data_list:
        for col in df.columns:
            if 'key' in col.lower():
                try:
                    df['Date'] = df[col].apply(lambda x: x.split("_")[0])
                    df['Date'] = pd.to_datetime(df['Date'])
                    df['Year'] = df['Date'].dt.year
                    df['Month'] = df['Date'].dt.month_name().str[:3]
                except IndexError:
                    continue
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col])
                df['Year'] = df[col].dt.year
                df['Month'] = df[col].dt.month_name().str[:3]
    return data_list


def format_currency_label(value: float) -> str:
    """
    Format a numerical value into a string representing
    the value with appropriate currency suffixes
    :param value: The numerical value to be formatted.
    :return: The formatted string with appropriate suffix and two decimal places.
    """
    if value >= 1e9:  # Billion
        return f'{value / 1e9:.2f} bn'
    elif value >= 1e6:  # Million
        return f'{value / 1e6:.2f} M'
    elif value >= 1e3:  # Thousand
        return f'{value / 1e3:.2f} K'
    else:
        return f'{value:.2f}'


def update_hover_layout(fig: go.Figure) -> go.Figure:
    """
    Updates the hover-layout of the plotly graph object figure
    :param fig: the plotly graph object fig
    :return: Figure with updated layout
    """
    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
            font_family="Rockwell"
        ),
        height=400
    )
    return fig


def get_previous_month(month):
    current = MONTHS.index(month)
    previous = MONTHS[current - 1]
    if previous == "Dec":
        return 0
    else:
        return previous


def current_and_previous_data(data, y, years):
    p_y = years.index(y) - 1
    current_data = data[data["Year"] == y]
    if p_y < 0:
        previous_data = current_data.copy()
    else:
        previous_data = data[(data["Year"] == years[p_y])]
    return current_data, previous_data


def get_overview_kpis(current_data, previous_data):
    num_of_customers = get_num_of_customers(current_data, previous_data)
    clv = get_clv(current_data, previous_data)
    avg_lsp = average_life_span(current_data, previous_data)
    avg_arpu = average_arpu(current_data, previous_data)
    churning = churn_rate(current_data, previous_data)

    return num_of_customers, clv, avg_lsp, avg_arpu, churning


def get_conversion_rate(data: pd.DataFrame):
    """
    Calculates the conversion rate.

    :param data: DataFrame containing column 'Customer ID'.
    :return: Conversion rate as a percentage.
    """
    try:
        # Total number of rows or records
        number_of_conversions = len(data)
        # Number of unique customer IDs
        number_of_visitors = data['Customer ID'].nunique()
        # Calculating conversion rate
        conversion_rate = (number_of_visitors / number_of_conversions) * 100
        return conversion_rate
    except ZeroDivisionError:
        return 0


def get_aov(data: pd.DataFrame):
    """
    Calculates the Average Order Value (AOV).

    :param data: DataFrame containing column 'Total Revenue'.
    :return: Average Order Value.
    """
    try:
        aov = data['Total Revenue'].sum() / len(data)
        return aov
    except ZeroDivisionError:
        return 0


def get_rev_by_customer(data: pd.DataFrame):
    """
    Calculates the average revenue per customer.

    :param data: DataFrame containing columns 'Customer ID' and 'Total Revenue'.
    :return: Average revenue per customer.
    """
    try:
        revenue_by_customer = data.groupby('Customer ID')['Total Revenue'].sum().mean()
        return revenue_by_customer
    except ZeroDivisionError:
        return 0


def shipping_amount(data: pd.DataFrame):
    """
    Calculates the shipping amount as a percentage of total revenue.

    :param data: DataFrame containing columns 'Shipping Amount' and 'Total Revenue'.
    :return: Shipping amount percentage.
    """
    try:
        shipping_percentage = (data['Shipping Amount'].sum() / data['Total Revenue'].sum()) * 100
        return shipping_percentage
    except ZeroDivisionError:
        return 0


def tax_amount(data: pd.DataFrame):
    """
    Calculates the tax amount as a percentage of total revenue.

    :param data: DataFrame containing columns 'Tax' and 'Total Revenue'.
    :return: Tax amount percentage.
    """
    try:
        tax_percentage = (data['Tax'].sum() / data['Total Revenue'].sum()) * 100
        return tax_percentage
    except ZeroDivisionError:
        return 0


def gross_profit_margin(data: pd.DataFrame):
    """
    Calculates the gross profit margin.

    :param data: DataFrame containing columns 'Gross Profit' and 'Total Revenue'.
    :return: Gross profit margin percentage.
    """
    try:
        margin = (data['Gross Profit'].sum() / data['Total Revenue'].sum()) * 100
        return margin
    except ZeroDivisionError:
        return 0


def get_discount_rate(data: pd.DataFrame):
    """
    Calculates the discount rate as a percentage of total revenue.

    :param data: DataFrame containing columns 'Discount' and 'Total Revenue'.
    :return: Discount rate percentage.
    """
    try:
        discount_rate = (data['Discount'].sum() / data['Total Revenue'].sum()) * 100
        return discount_rate
    except ZeroDivisionError:
        return 0

def get_total_revenue(data):
    data["Total Revenue"] = data["Units Sold"] * data["Price Ratio"]
    return data["Total Revenue"].sum()


def get_sales_volume(data):
    return data["Units Sold"].sum()


def get_conv_rate(df):
    total_visitors = len(df)  # Total number of visitors
    converted_visitors = df[df['Is Target'] == 1]  # Visitors who converted
    conversion_rate = (len(converted_visitors) / total_visitors) * 100
    return conversion_rate


def get_visitor_engagement(df):
    average_event_count = df['Event Sequence'].mean()
    return average_event_count






def get_attribution_indicators(df, column, name, value, prefix):
    df["Event DateTime"] = pd.to_datetime(df["Event DateTime"])
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={"prefix": prefix},
            title={"text": name, "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=df["Event DateTime"],
        y=df[column],
        mode="lines",
        # fill='tozeroy',
        name=name,
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig.update_layout(height=250)
    fig = update_hover_layout(fig)
    return fig


def get_products_data(directory="./data", prefix="demand_forecast_output_ABC_Cereal_Bars"):
    dfs = []
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith(".csv"):
            product_name = filename.replace(prefix, "").replace(".csv", "").strip()
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            df["Product"] = product_name
            dfs.append(df)
    products_data = pd.concat(dfs, ignore_index=True)
    return products_data
