import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
from utils import preprocess_data

from views import *

# ------------------------------ Page Configuration------------------------------
st.set_page_config(page_title="CFO-Dashboard", page_icon="📊", layout="wide")
# ----------------------------------- Page Styling ------------------------------

with open("css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid=stHeader] {
        display:none;
    }
    [data-testid=block-container] {
        padding-top: 0px;
    }
    [data-testid=stSidebarUserContent]{
      margin-top: -40px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("./assets/logo.png")
    st.write("# ")

# ----------------------------------- Data Loading ------------------------------
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
balance_data = conn.read(
    worksheet="balance_sheet",
)
income_data = conn.read(
    worksheet="income_data",
)
cash_data = conn.read(
    worksheet="cash_flow"
)
customers_data = conn.read(
    worksheet="customers_report"
)
sales_data = conn.read(
    worksheet="sales_report"
)
products_data = conn.read(
    worksheet="products_data"
)
market_data = conn.read(
    worksheet="market_data"
)
media_data = conn.read(
    worksheet="media_data"
)

# --------------------------- Data Pre-processing -------------------------------

customers_sales_data = pd.merge(customers_data, sales_data, on='Customer_ID')
(balance_data, income_data, cash_data, customers_sales_data,
 market_data, media_data) = preprocess_data([balance_data, income_data, cash_data,
                                             customers_sales_data, market_data, media_data])
temp_df = pd.merge(income_data, balance_data, on=["Valuation Date", "Year", "Month"])
cash_flow_data = pd.merge(temp_df, cash_data, on=["Valuation Date", "Year", "Month"])

# ----------------------------------- Menu --------------------------------------
menu = option_menu(menu_title=None, menu_icon=None, orientation="horizontal",
                   options=["Overview", "Sales Insights", "Customer's Report",
                            "Demand Elasticity", "Marketing Attribution", "Accounts"])

match menu:
    case "Overview":
        overview(customers_sales_data, cash_flow_data)
    case "Sales Insights":
        sales_insights(customers_sales_data)
    case "Customer's Report":
        customer_report(customers_sales_data)
    case "Demand Elasticity":
        demand_elasticity(products_data)
    case "Marketing Attribution":
        marketing_attribution(market_data, media_data)
    case "Accounts":
        accounts(cash_flow_data)
