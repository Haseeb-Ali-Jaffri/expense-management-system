from datetime import datetime
import streamlit as st
import requests

api_url = "http://127.0.0.1:8000"

def add_update_tab():
    entered_date = st.date_input("Enter Date: ",datetime(2024,8,1),label_visibility= "collapsed")
    date_key = entered_date.strftime("%Y%m%d")
    response = requests.get(f"{api_url}/expenses/{entered_date}")
    if response.status_code == 200:
        expenses = response.json()
    else:
        expenses = []
        st.write("Failed to retrieve expenses data")
    categories = ["Rent", "Food", "Shopping", "Other", "Entertainment", "Other"]
    updated_expenses=[]
    with st.form(key = "expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")
        num_rows = len(expenses) + 5
        for i in range(num_rows):
            if i <(len(expenses)):
                amount = expenses[i]['amount']
                category = expenses[i]['category']
                notes = expenses[i]['notes']
            else:
                amount = 0.0
                category = "Rent"
                notes = ""
            col1, col2,col3 = st.columns(3)
            with col1:
                amount_ip = st.number_input(label="Amount",min_value=0.0,value=amount,step=1.0, key = f"{date_key}_amount{i}",label_visibility="collapsed")
            with col2:
                category_ip = st.selectbox(label = "Category", options=categories, index=categories.index(category), key =f"{date_key}_category{i}", label_visibility="collapsed")
            with col3:
                notes_ip = st.text_input(label= "Notes", value= notes, key = f"{date_key}_notes{i}" ,label_visibility= "collapsed")
            updated_expenses.append({"amount":amount_ip, "category":category_ip, "notes":notes_ip})
        submit_button = st.form_submit_button(label = "Submit")
        if submit_button:
            filtered_expenses = [expense for expense in updated_expenses if expense["amount"]>0]
            post_response = requests.post(f"{api_url}/expenses/{entered_date}",json=filtered_expenses)
            if post_response.status_code == 200:
                st.success("Expense successfully updated")
            else:
                st.error("Failed to update expense")