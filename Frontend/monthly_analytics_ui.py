import streamlit as st
import requests
import pandas as pd

api_url = "http://127.0.0.1:8000"

def monthly_analytics_tab():

    response = requests.get(f"{api_url}/analytics/monthly")

    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data)

        st.subheader("Monthly Expense")

        st.bar_chart(df.set_index("month")["total"])

        st.table(df)

    else:
        st.error("Unable to fetch data")