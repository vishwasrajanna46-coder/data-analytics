import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Required Columns Check
    required_columns = ["Date", "Product", "Sales", "Revenue"]

    if all(col in df.columns for col in required_columns):

        # Convert Date
        df["Date"] = pd.to_datetime(df["Date"])

        # KPIs
        total_sales = df["Sales"].sum()
        total_revenue = df["Revenue"].sum()
        total_products = df["Product"].nunique()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Sales", f"{total_sales:,.0f}")
        col2.metric("Total Revenue", f"₹{total_revenue:,.2f}")
        col3.metric("Products", total_products)

        st.divider()

        # Date Filter
        start_date = df["Date"].min()
        end_date = df["Date"].max()

        date_range = st.date_input(
            "Select Date Range",
            [start_date, end_date]
        )

        if len(date_range) == 2:
            df = df[
                (df["Date"] >= pd.Timestamp(date_range[0]))
                & (df["Date"] <= pd.Timestamp(date_range[1]))
            ]

        # Revenue Trend
        revenue_trend = (
            df.groupby("Date")["Revenue"]
            .sum()
            .reset_index()
        )

        fig1 = px.line(
            revenue_trend,
            x="Date",
            y="Revenue",
            title="Revenue Trend"
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Top Products
        product_sales = (
            df.groupby("Product")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(by="Revenue", ascending=False)
        )

        fig2 = px.bar(
            product_sales,
            x="Product",
            y="Revenue",
            title="Top Performing Products"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Pie Chart
        fig3 = px.pie(
            product_sales,
            names="Product",
            values="Revenue",
            title="Revenue Share by Product"
        )

        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.error(
            "Dataset must contain columns: Date, Product, Sales, Revenue"
        )

else:
    st.info("Upload a CSV or Excel file to begin.")