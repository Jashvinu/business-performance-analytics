# Business Performance Analytics

## Overview
The **Business Performance Analytics** project is designed to deliver insights into business performance, specifically tailored for an eBay seller store. This dashboard provides an interactive platform for analyzing sales data, customer behavior, marketing effectiveness, and financial metrics. By leveraging this tool, business owners can make informed decisions to optimize operations, increase revenue, and enhance customer satisfaction.

## Features
- **High-Level Overview**: Summary of key business metrics, financial performance, and trends.
- **Sales Insights**: Detailed analysis of sales performance, including revenue trends, product performance, and cost breakdowns.
- **Customer Behavior**: Insights into customer segmentation, lifetime value, acquisition costs, and conversion rates.
- **Demand Elasticity**: Analysis of price elasticity and its impact on product demand and pricing strategies.
- **Marketing Attribution**: Evaluation of marketing channels, conversion rates, and customer journey analysis.
- **Financial Reporting**: Detailed financial insights, including cash flow analysis, expense categorization, and profit/loss tracking.

## Project Scope
This project includes the development of a user-friendly dashboard that integrates data from an eBay seller store. The goal is to provide actionable insights into different aspects of the business, supporting strategic planning and decision-making.

## Objectives
- To create an interactive dashboard that utilizes business data for real-time analysis.
- To provide in-depth insights into sales, customer behavior, and financial metrics.
- To support informed decision-making through data-driven visualizations.

## Project Environment
| **Component**           | **Technology**         |
|-------------------------|------------------------|
| **Programming Language** | Python                 |
| **Data Visualization**  | Plotly                 |
| **Web Framework**       | Streamlit              |
| **Data Management**     | Pandas, Streamlit GSheet, Google Sheets |
| **Version Control**     | Git                    |

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/noorulhudaajmal/business-performance-analytics.git
   ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Link your Google Sheets data:
   - Before running the application, you need to connect the streamlit app to your Google Sheets data where the eBay seller store data is stored.
   - Create and open the .streamlit/secrets.toml file in the root directory of the project.
   - Add your Google Sheets API credentials and spreadsheet URL [Guidelines](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet).
   - Ensure your Google Sheets contains the following worksheets with the respective data:
       - Balance Sheet
       - Income DataSheet
       - Cash Flow
       - Customers Report
       - Sales Report
       - Market Data
       - Media Data
       - Products Data

5. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage
Once the application is running, user can explore various sections of the dashboard to gain insights into different aspects of the business.

---
