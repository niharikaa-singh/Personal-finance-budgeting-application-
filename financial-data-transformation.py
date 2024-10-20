import pandas as pd
import numpy as np
from datetime import datetime
import os
import glob

def load_bank_data(file_path):
    df = pd.read_csv(file_path)
    df['Source'] = 'Bank'
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].astype(float)
    return df[['Date', 'Description', 'Amount', 'Source']]

def load_google_pay_data(file_path):
    df = pd.read_csv(file_path)
    df['Source'] = 'Google Pay'
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].astype(float)
    return df[['Date', 'Description', 'Amount', 'Source']]

def load_paytm_data(file_path):
    df = pd.read_csv(file_path)
    df['Source'] = 'Paytm'
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].astype(float)
    return df[['Date', 'Description', 'Amount', 'Source']]

def categorize_transaction(description):
    description = description.lower()
    if any(keyword in description for keyword in ['grocery', 'supermarket', 'food', 'snacks']):
        return 'Food & Groceries'
    elif any(keyword in description for keyword in ['restaurant', 'cafe', 'dining', 'takeout', 'delivery']):
        return 'Eating Out'
    elif any(keyword in description for keyword in ['electricity', 'water', 'gas', 'internet', 'phone', 'wifi']):
        return 'Utilities'
    elif any(keyword in description for keyword in ['uber', 'lyft', 'taxi', 'metro', 'bus', 'train', 'subway']):
        return 'Transportation'
    elif any(keyword in description for keyword in ['scholarship', 'grant', 'loan', 'financial aid', 'stipend']):
        return 'Financial Aid'
    elif any(keyword in description for keyword in ['salary', 'paycheck', 'deposit', 'part-time', 'internship']):
        return 'Income'
    elif any(keyword in description for keyword in ['rent', 'dorm', 'housing']):
        return 'Housing'
    elif any(keyword in description for keyword in ['movie', 'theatre', 'concert', 'entertainment', 'spotify', 'netflix']):
        return 'Entertainment'
    elif any(keyword in description for keyword in ['doctor', 'hospital', 'pharmacy', 'health center']):
        return 'Healthcare'
    elif any(keyword in description for keyword in ['textbook', 'course materials', 'school supplies', 'library']):
        return 'Education Supplies'
    elif any(keyword in description for keyword in ['tuition', 'fees', 'lab fee']):
        return 'Tuition & Fees'
    elif any(keyword in description for keyword in ['club', 'society', 'membership', 'gym']):
        return 'Campus Activities'
    else:
        return 'Other'

def clean_description(description):
    # Remove common prefixes/suffixes and standardize descriptions
    cleaned = description.lower()
    cleaned = cleaned.replace('transaction - ', '').replace('payment to ', '').replace('payment from ', '')
    return cleaned.strip()

def transform_data(df):
    # Clean and transform the data
    df['Description'] = df['Description'].apply(clean_description)
    df['Category'] = df['Description'].apply(categorize_transaction)
    df['Month'] = df['Date'].dt.to_period('M')
    df['Year'] = df['Date'].dt.year
    df['DayOfWeek'] = df['Date'].dt.day_name()
    
    # Separate income and expenses
    df['Income'] = np.where(df['Amount'] > 0, df['Amount'], 0)
    df['Expense'] = np.where(df['Amount'] < 0, -df['Amount'], 0)
    
    # Add academic period (assuming Fall semester starts in August, Spring in January)
    df['AcademicPeriod'] = df['Date'].dt.to_period('Q-AUG').astype(str).replace({
        'Q1': 'Fall', 'Q2': 'Fall', 'Q3': 'Spring', 'Q4': 'Summer'
    })
    
    return df

def consolidate_data(input_directory, output_file):
    # Load data from all sources
    bank_files = glob.glob(os.path.join(input_directory, '*bank*.csv'))
    google_pay_files = glob.glob(os.path.join(input_directory, '*google_pay*.csv'))
    paytm_files = glob.glob(os.path.join(input_directory, '*paytm*.csv'))
    
    dfs = []
    for file in bank_files:
        dfs.append(load_bank_data(file))
    for file in google_pay_files:
        dfs.append(load_google_pay_data(file))
    for file in paytm_files:
        dfs.append(load_paytm_data(file))
    
    # Concatenate all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Transform the combined data
    transformed_df = transform_data(combined_df)
    
    # Sort by date
    transformed_df = transformed_df.sort_values('Date')
    
    # Save to CSV
    transformed_df.to_csv(output_file, index=False)
    print(f"Consolidated data saved to {output_file}")
    
    return transformed_df

def analyze_student_finances(df):
    print("\nCollege Student Financial Analysis:")
    print(f"Total Transactions: {len(df)}")
    print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"\nTotal Income: ${df['Income'].sum():.2f}")
    print(f"Total Expenses: ${df['Expense'].sum():.2f}")
    print(f"Net Savings: ${(df['Income'].sum() - df['Expense'].sum()):.2f}")
    
    print("\nTop 5 Expense Categories:")
    print(df.groupby('Category')['Expense'].sum().sort_values(ascending=False).head())
    
    print("\nExpenses by Academic Period:")
    print(df.groupby('AcademicPeriod')['Expense'].sum().sort_values(ascending=False))
    
    print("\nAverage Monthly Spending:")
    print(df.groupby('Month')['Expense'].mean().mean())
    
    print("\nFinancial Aid Received:")
    print(df[df['Category'] == 'Financial Aid']['Income'].sum())
    
    print("\nTuition & Fees Paid:")
    print(df[df['Category'] == 'Tuition & Fees']['Expense'].sum())
    
    weekday_spending = df.groupby('DayOfWeek')['Expense'].mean().sort_values(ascending=False)
    print("\nAverage Spending by Day of Week:")
    print(weekday_spending)
    
    highest_spending_day = weekday_spending.index[0]
    print(f"\nHighest average spending on: {highest_spending_day}")

if __name__ == "__main__":
    input_directory = "path/to/your/input/files"
    output_file = "consolidated_student_financial_data.csv"
    consolidated_data = consolidate_data(input_directory, output_file)
    
    analyze_student_finances(consolidated_data)
