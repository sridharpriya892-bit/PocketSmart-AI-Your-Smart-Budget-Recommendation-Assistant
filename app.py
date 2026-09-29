import os
import streamlit as st
import pandas as pd
from google import genai

# Page Config
st.set_page_config(page_title="Pocket Smart AI", page_icon="💰", layout="centered")

st.title("💰 Pocket Smart AI")
st.subheader("Your AI-Powered Personal Finance Assistant")

# Sidebar - API Key Configuration
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to enable AI analysis.")

# User Inputs
st.header("1. Financial Details")
income = st.number_input("Monthly Income (₹)", min_value=0.0, value=50000.0, step=1000.0)

st.subheader("Monthly Expenses")
rent = st.number_input("Rent / Housing", min_value=0.0, value=15000.0)
food = st.number_input("Food & Groceries", min_value=0.0, value=8000.0)
bills = st.number_input("Utilities & Bills", min_value=0.0, value=3000.0)
other = st.number_input("Other Expenses", min_value=0.0, value=5000.0)

total_expenses = rent + food + bills + other
net_savings = income - total_expenses

# Summary Metrics
st.header("2. Budget Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expenses:,.2f}")
col3.metric("Net Savings", f"₹{net_savings:,.2f}")

# Expense Breakdown Chart
expense_data = pd.DataFrame({
    'Category': ['Rent', 'Food', 'Bills', 'Other'],
    'Amount': [rent, food, bills, other]
})
st.bar_chart(expense_data.set_index('Category'))

# AI Insights Generation
st.header("3. Smart AI Insights")
if st.button("Generate AI Advisory"):
    if not api_key:
        st.error("Please provide a valid Gemini API Key in the sidebar.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            Act as a personal financial expert. Analyze the following budget details:
            - Monthly Income: ₹{income}
            - Rent: ₹{rent}
            - Food: ₹{food}
            - Utilities: ₹{bills}
            - Other Expenses: ₹{other}
            - Total Expenses: ₹{total_expenses}
            - Net Savings: ₹{net_savings}

            Provide a concise, 3-step action plan to improve savings and optimize budget allocation.
            """
            
            with st.spinner("Analyzing your finances..."):
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt
                )
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error calling AI service: {e}")