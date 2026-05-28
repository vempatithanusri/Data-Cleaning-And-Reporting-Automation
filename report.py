# Data Cleaning & Reporting Automation
# Automated Data Cleaning Dashboard using Streamlit

# Install Required Libraries
# pip install pandas numpy streamlit plotly openpyxl

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Streamlit Page Setup
st.set_page_config(page_title="Data Cleaning Automation", layout="wide")

# Title
st.title("🧹 Data Cleaning & Reporting Automation")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read Dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Original Dataset")
    st.dataframe(df)

    # Dataset Information
    st.subheader("📌 Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Missing Values Before Cleaning
    st.subheader("❌ Missing Values Before Cleaning")
    missing_before = df.isnull().sum()
    st.dataframe(missing_before)

    # Remove Duplicates
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Fill Missing Values
    for col in df.select_dtypes(include=np.number).columns:
        df[col].fillna(df[col].mean(), inplace=True)

    for col in df.select_dtypes(include='object').columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # Standardize Column Names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Missing Values After Cleaning
    st.subheader("✅ Missing Values After Cleaning")
    missing_after = df.isnull().sum()
    st.dataframe(missing_after)

    # Cleaned Dataset
    st.subheader("🧼 Cleaned Dataset")
    st.dataframe(df)

    # Summary Report
    st.subheader("📊 Automated Summary Report")

    summary = df.describe(include='all')
    st.dataframe(summary)

    # Visualization
    st.subheader("📈 Visual Summary")

    numeric_columns = df.select_dtypes(include=np.number).columns

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=selected_column,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # KPI Metrics
    st.subheader("📌 Cleaning Report")

    col4, col5 = st.columns(2)

    col4.metric("Duplicates Removed", duplicates)
    col5.metric("Remaining Missing Values", df.isnull().sum().sum())

    # Download Cleaned Data
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download Cleaned Dataset",
        data=csv,
        file_name='cleaned_dataset.csv',
        mime='text/csv'
    )

else:
    st.info("Please upload a CSV or Excel file.")
