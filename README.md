# Business Performance Analytics

## Overview
The **Business Performance Analytics** project is designed to get insights into business performance, specifically for an eBay seller store. This provides an interactive dashboard for analyzing sales data, customer behavior, marketing effectiveness, and financial metrics. By leveraging this tool, business owners can make informed decisions to optimize operations, increase revenue, and enhance customer satisfaction.

## Features
- **High-Level Overview**: A summary of key business metrics, financial performance, and trends.
- **Sales Insights**: Shows detailed sales performance analysis, including revenue trends, product performance, and cost breakdowns.
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

## Screenshots

![overview-tab](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/1.png)
![sales-report](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/2.png)
![customer-report](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/3.png)
![demand](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/4.png)
![market](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/5.png)
![accounts](https://github.com/noorulhudaajmal/business-performance-analytics/blob/main/images/6.png)

---
