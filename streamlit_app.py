# ---------------- FIX IMPORT PATH ---------------- #
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ---------------- LIBRARIES ---------------- #
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from src.analysis import *

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
.metric-card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #
df = load_data()
df = preprocess_data(df)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🔍 Filters")

person = st.sidebar.selectbox(
    "Select Person",
    ["All"] + list(df['person'].unique())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + list(df['month'].unique())
)

budget = st.sidebar.slider("Monthly Budget", 10000, 100000, 30000)

# ---------------- FILTER DATA ---------------- #
filtered_df = df.copy()

if person != "All":
    filtered_df = filtered_df[filtered_df['person'] == person]

if month != "All":
    filtered_df = filtered_df[filtered_df['month'] == month]

# ---------------- TITLE ---------------- #
st.title("💸 Expense Tracker Dashboard")

# ---------------- KPI CARDS ---------------- #
total_spend, transactions, avg_txn, avg_daily, top_cat = compute_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

def card(title, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col1:
    card("💰 Total Spend", f"₹{total_spend:,.0f}")

with col2:
    card("📊 Avg Daily", f"₹{avg_daily:,.0f}")

with col3:
    card("🧾 Transactions", transactions)

with col4:
    card("💳 Avg Transaction", f"₹{avg_txn:,.0f}")

with col5:
    card("🏆 Top Category", top_cat)

st.markdown("---")

# ---------------- ROW 1 ---------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📅 Monthly Spending")
    monthly = monthly_spending(filtered_df)
    fig1 = px.bar(
        monthly,
        x='month',
        y='amount',
        color='amount',
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("## 💳 Payment Methods")
    payment = payment_distribution(filtered_df)
    fig2 = px.pie(
        payment,
        names='payment_mode',
        values='amount',
        hole=0.5,
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- ROW 2 ---------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📈 Daily Trend")
    rolling = rolling_spending(filtered_df)
    fig3 = px.line(
        rolling,
        x='date',
        y=['amount', 'rolling_avg'],
        template='plotly_dark'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("## ⚠️ Overspending")
    overspend = overspending_detection(filtered_df, budget)
    fig4 = px.bar(
        overspend,
        x='month',
        y='amount',
        color='overspend',
        template='plotly_dark'
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------------- HEATMAP ---------------- #
st.markdown("## 🔥 Category vs Month Heatmap")

heatmap = heatmap_data(filtered_df)

fig5, ax = plt.subplots()
sns.heatmap(heatmap, cmap="rocket", linewidths=0.5, ax=ax)
st.pyplot(fig5)

# ---------------- SAVINGS ---------------- #
st.markdown("## 💰 Savings Rate")

savings = savings_rate(filtered_df)

fig6 = px.line(
    savings,
    x='month',
    y='savings_rate',
    template='plotly_dark'
)
st.plotly_chart(fig6, use_container_width=True)

# ---------------- PERSON SPENDING ---------------- #
st.markdown("## 👥 Person-wise Spending")

person_df = person_spending(filtered_df)

fig7 = px.bar(
    person_df,
    x='person',
    y='amount',
    color='amount',
    template='plotly_dark'
)
st.plotly_chart(fig7, use_container_width=True)

# ---------------- TOP TRANSACTIONS ---------------- #
st.markdown("## 🧾 Top Transactions")

top_txn = top_transactions(filtered_df)
st.dataframe(top_txn)

# ---------------- INSIGHTS ---------------- #
st.markdown("## 🧠 Key Insights")

insights = generate_insights(filtered_df)

for ins in insights:
    st.markdown(
        f"""
        <div class="metric-card">
            {ins}
        </div>
        """,
        unsafe_allow_html=True
    )