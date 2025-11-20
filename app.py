import streamlit as st
import pandas as pd

# ---------- BASIC PAGE SETUP ----------
st.set_page_config(
    page_title="Civil Supplies AI Command Centre",
    layout="wide"
)

st.title("Civil Supplies AI Command Centre (PoC)")
st.markdown("### Simulated AI-driven Fiscal Intelligence for AP Civil Supplies")

st.markdown("---")

# ---------- SIDEBAR: GLOBAL INPUTS ----------
st.sidebar.header("Simulation Controls")

district = st.sidebar.selectbox(
    "Select District",
    ["All AP", "Srikakulam", "Vijayawada", "Visakhapatnam", "Tirupati"]
)

leakage_dev = st.sidebar.slider(
    "Avg Truck Route Deviation (%)", 0, 50, 8
)
ghost_pct = st.sidebar.slider(
    "Ghost Beneficiaries (%)", 0, 20, 4
)
fps_uptime = st.sidebar.slider(
    "FPS Uptime (%)", 60, 100, 92
)
dbt_anomalies = st.sidebar.slider(
    "Unusual DBT Transactions (per 10k)", 0, 500, 90
)
quality_level = st.sidebar.selectbox(
    "Grain Quality Status",
    ["Good", "Mixed", "Adulterated"]
)

st.sidebar.markdown("---")
st.sidebar.caption("All numbers are simulated for PoC demo")

# ---------- TOP KPI CARDS ----------
# We convert the raw slider values into simple "AI style" KPIs

leakage_index = round(leakage_dev * 1.5, 1)
ghost_loss = ghost_pct * 3   # in ₹ Crore
quality_score = 95 if quality_level == "Good" else (78 if quality_level == "Mixed" else 60)
fraud_risk = round(dbt_anomalies / 5, 1)
fiscal_savings = max(0, round(750 - (leakage_index + ghost_loss + (100-quality_score) + fraud_risk), 1))

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Leakage Index", leakage_index, f"{leakage_dev}% deviation")
col2.metric("Ghost Beneficiary Loss (₹ Cr)", ghost_loss, f"{ghost_pct}% ghost")
col3.metric("Quality Score", quality_score, quality_level)
col4.metric("DBT Fraud Risk Score", fraud_risk, f"{dbt_anomalies} alerts/10k")
col5.metric("Estimated Annual Savings (₹ Cr)", fiscal_savings, "Simulated")

st.markdown("---")

# ---------- TABS FOR DIFFERENT MODULES ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview Dashboard",
    "Leakage & Movement",
    "Ghost Beneficiaries",
    "Field Staff & FPS",
    "DBT Fraud
