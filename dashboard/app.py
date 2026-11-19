import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import sys
import os

# Allow importing src folder
sys.path.append(os.path.abspath("../src"))

from business_logic import (
    profit_recommendation,
    business_health_score,
    dynamic_health_score,
    scenario_health_score
)

from insights import generate_insights


# ======================
# PAGE SETTINGS
# ======================

st.set_page_config(page_title="Decision Intelligence Dashboard")

st.title("📊 Decision Intelligence AI Dashboard")


# ======================
# LOAD DATA + MODEL
# ======================

df = pd.read_csv("../data/superstore.csv", encoding="latin1")

model = pickle.load(open("../models/profit_model.pkl", "rb"))


# ======================
# BUSINESS OVERVIEW
# ======================

st.subheader("Business Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("Total Orders", df.shape[0])


# ======================
# SALES CHART
# ======================

st.subheader("Sales by Category")

category_sales = df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots()
category_sales.plot(kind="bar", ax=ax)

st.pyplot(fig)


# ======================
# AI PREDICTION
# ======================

st.subheader("🤖 AI Profit Prediction")

sales = st.number_input("Sales", value=200.0)
quantity = st.number_input("Quantity", step=1, value=2)
discount = st.slider("Discount", 0.0, 1.0, 0.1)

if st.button("Predict"):

    prediction = model.predict([[sales, quantity, discount]])[0]

    st.success(f"Predicted Profit: ${prediction:.2f}")

    # Recommendation
    recommendation = profit_recommendation(prediction)
    st.info(recommendation)

    # ⭐ Dynamic Health Score
    dynamic_score = dynamic_health_score(prediction)

    st.subheader("AI Business Health Score")
    st.progress(dynamic_score)
    st.write(f"Health Score: {dynamic_score}/100")

    st.subheader("Scenario Health Score (Based on Your Inputs)")

product_list = df["Product Name"].dropna().unique().tolist()

p1 = st.selectbox("Product 1", product_list, key="p1")
p2 = st.selectbox("Product 2", product_list, key="p2")
p3 = st.selectbox("Product 3", product_list, key="p3")

d1 = st.slider("Discount for Product 1", 0.0, 1.0, 0.1, key="d1")
d2 = st.slider("Discount for Product 2", 0.0, 1.0, 0.1, key="d2")
d3 = st.slider("Discount for Product 3", 0.0, 1.0, 0.1, key="d3")

def get_product_row(product_name):
    row = df[df["Product Name"] == product_name].iloc[0]
    return row

if st.button("Run Scenario"):
    chosen = [(p1, d1), (p2, d2), (p3, d3)]

    total_sales = 0
    total_pred_profit = 0

    results = []

    for name, disc in chosen:
        row = get_product_row(name)

        sales_val = float(row["Sales"])
        qty_val = int(row["Quantity"])

        pred_profit = model.predict([[sales_val, qty_val, disc]])[0]

        total_sales += sales_val
        total_pred_profit += pred_profit

        results.append({
            "Product Name": name,
            "Sales": sales_val,
            "Quantity": qty_val,
            "Discount (Scenario)": disc,
            "Predicted Profit": round(float(pred_profit), 2)
        })

    st.write("### Scenario Result Table")
    st.dataframe(pd.DataFrame(results))

    scenario_score = scenario_health_score(total_pred_profit, total_sales)

    st.write("### Scenario Health Score")
    st.progress(scenario_score)
    st.write(f"Scenario Health Score: **{scenario_score}/100**")

    st.write(f"Total Scenario Sales: **${total_sales:,.2f}**")
    st.write(f"Total Predicted Profit: **${total_pred_profit:,.2f}**")


# ======================
# AI INSIGHTS
# ======================

st.subheader("AI Business Insights")

insights = generate_insights(df)

for i in insights:
    st.write(i)


# ======================
# LOSS PRODUCTS
# ======================

st.subheader("Loss Making Products")

loss_df = df[df["Profit"] < 0].sort_values("Profit").head(10)

st.dataframe(loss_df[["Product Name", "Category", "Sales", "Profit"]])


# ======================
# OVERALL COMPANY HEALTH
# ======================

st.subheader("Overall Business Health")

overall_score = business_health_score(df)

st.progress(overall_score)
st.write(f"Overall Score: {overall_score}/100")

st.caption("AI predicts profit and recommends business decisions.")





