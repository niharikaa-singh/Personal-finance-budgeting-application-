from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict
import uvicorn

# Import your existing functions
from your_script import consolidate_data, analyze_student_finances

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the data
input_directory = "path/to/your/input/files"
output_file = "consolidated_student_financial_data.csv"
df = consolidate_data(input_directory, output_file)

class FinancialSummary(BaseModel):
    total_transactions: int
    date_range: Dict[str, str]
    total_income: float
    total_expenses: float
    net_savings: float
    top_expense_categories: Dict[str, float]
    expenses_by_academic_period: Dict[str, float]
    average_monthly_spending: float
    financial_aid_received: float
    tuition_fees_paid: float
    average_spending_by_day: Dict[str, float]
    highest_spending_day: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Financial Analysis API"}

@app.get("/summary", response_model=FinancialSummary)
async def get_summary():
    summary = analyze_student_finances(df)
    return summary

@app.get("/timeseries")
async def get_timeseries():
    timeseries_data = df.groupby('Date').agg({
        'Income': 'sum',
        'Expense': 'sum'
    }).reset_index().to_dict(orient='records')
    return timeseries_data

@app.get("/category_breakdown")
async def get_category_breakdown():
    category_data = df.groupby('Category')['Expense'].sum().sort_values(ascending=False).to_dict()
    return category_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
