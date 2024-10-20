import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Student Financial Analysis", layout="wide")
st.title("Student Financial Analysis Dashboard")

# Fetch summary data
summary = requests.get(f"{API_URL}/summary").json()

# Display summary statistics
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${summary['total_income']:.2f}")
col2.metric("Total Expenses", f"${summary['total_expenses']:.2f}")
col3.metric("Net Savings", f"${summary['net_savings']:.2f}")

st.subheader("Financial Overview")
st.write(f"Total Transactions: {summary['total_transactions']}")
st.write(f"Date Range: {summary['date_range']['min']} to {summary['date_range']['max']}")

# Fetch time series data
timeseries_data = requests.get(f"{API_URL}/timeseries").json()
df_timeseries = pd.DataFrame(timeseries_data)
df_timeseries['Date'] = pd.to_datetime(df_timeseries['Date'])

# Time series plot
st.subheader("Income and Expenses Over Time")
fig_timeseries = px.line(df_timeseries, x='Date', y=['Income', 'Expense'],
                         title='Income and Expenses Over Time')
st.plotly_chart(fig_timeseries, use_container_width=True)

# Fetch category breakdown data
category_data = requests.get(f"{API_URL}/category_breakdown").json()

# Category breakdown plot
st.subheader("Expense Categories")
fig_categories = px.pie(values=list(category_data.values()), names=list(category_data.keys()),
                        title='Expense Categories')
st.plotly_chart(fig_categories, use_container_width=True)

# Display top expense categories
st.subheader("Top 5 Expense Categories")
top_expenses = pd.DataFrame(list(summary['top_expense_categories'].items()),
                            columns=['Category', 'Amount'])
top_expenses = top_expenses.sort_values('Amount', ascending=False).head()
fig_top_expenses = px.bar(top_expenses, x='Category', y='Amount',
                          title='Top 5 Expense Categories')
st.plotly_chart(fig_top_expenses, use_container_width=True)

# Display expenses by academic period
st.subheader("Expenses by Academic Period")
academic_expenses = pd.DataFrame(list(summary['expenses_by_academic_period'].items()),
                                 columns=['Period', 'Amount'])
fig_academic = px.bar(academic_expenses, x='Period', y='Amount',
                      title='Expenses by Academic Period')
st.plotly_chart(fig_academic, use_container_width=True)

# Display average spending by day of week
st.subheader("Average Spending by Day of Week")
day_spending = pd.DataFrame(list(summary['average_spending_by_day'].items()),
                            columns=['Day', 'Amount'])
day_spending = day_spending.sort_values('Amount', ascending=False)
fig_day_spending = px.bar(day_spending, x='Day', y='Amount',
                          title='Average Spending by Day of Week')
st.plotly_chart(fig_day_spending, use_container_width=True)

# Additional metrics
st.subheader("Additional Financial Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Monthly Spending", f"${summary['average_monthly_spending']:.2f}")
col2.metric("Financial Aid Received", f"${summary['financial_aid_received']:.2f}")
col3.metric("Tuition & Fees Paid", f"${summary['tuition_fees_paid']:.2f}")

st.write(f"Highest average spending on: {summary['highest_spending_day']}")
