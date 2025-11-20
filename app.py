import streamlit as st

st.title("Civil Supplies AI PoC Dashboard")

leakage = st.slider("Truck Route Deviation (%)", 0, 100, 5)
ghost = st.slider("Ghost Beneficiaries (%)", 0, 30, 3)
quality = st.selectbox("Grain Quality", ["Good", "Adulterated"])
fps_uptime = st.slider("FPS Uptime (%)", 50, 100, 90)
dbt = st.slider("Unusual DBT Transactions", 0, 500, 50)

st.subheader("Simulated Insights")

st.write(f"Leakage Index Score: {leakage * 1.8}")
st.write(f"Ghost Beneficiary Loss Estimate: ₹{ghost * 3} Crore")
st.write("Quality Score: 95" if quality == "Good" else "Quality Score: 62")
st.write(f"FPS Health Score: {fps_uptime}")
st.write(f"DBT Fraud Risk Score: {dbt / 5}")
