# Personal-finance-budgeting-application-

# Financial Data ETL Pipeline and Web Application

This project involves the development of an ETL (Extract, Transform, Load) pipeline for consolidating financial data from multiple sources. The pipeline cleans, standardizes, and categorizes transactions, transforming raw data into structured, analysis-ready information. Additionally, the project includes a web application built using Streamlit, with interactive data visualizations created using Matplotlib and Seaborn, and a FastAPI backend to handle API requests.

## Features

### 1. **ETL Pipeline**
- **Extract**: Pulls data from multiple financial sources such as bank statements, Google Pay, and Paytm transactions.
- **Transform**:
  - Cleans and standardizes the data (e.g., formats dates, handles missing values, and normalizes currency formats).
  - Categorizes transactions into pre-defined categories like "Rent," "Groceries," and "Miscellaneous."
- **Load**: Outputs the cleaned and categorized data into a structured format, ready for analysis.

### 2. **Data Visualization Features**
- **Budget Adherence Tracking**: Visualizes whether the user is staying within their set monthly budget.
- **Category-wise Expense Breakdown**: Provides visual insights into how expenses are distributed across different categories.
- **Financial Goal Progress**: Shows progress towards financial goals (e.g., savings or investment targets) over time.

### 3. **Web Application**
- **Frontend**: Developed using **Streamlit** to create an interactive and user-friendly interface.
- **Backend**: Integrated with **FastAPI** to handle API requests and serve processed data.
- **Data Visualizations**: Interactive plots and charts created using **Matplotlib** and **Seaborn** for visualizing financial data.

