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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview Dashboard",
    "Leakage & Movement",
    "Ghost Beneficiaries",
    "Field Staff & FPS",
    "DBT Fraud Analytics"
])

# ---------- TAB 1: OVERVIEW ----------
with tab1:
    st.subheader(f"State Overview - {district}")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("#### Trend of Risk Scores (Simulated)")
        # Create fake trend data
        trend_df = pd.DataFrame({
            "Month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            "Leakage Index": [40, 38, 35, leakage_index + 2, leakage_index, max(leakage_index - 3, 10)],
            "Fraud Risk": [30, 28, 25, fraud_risk + 3, fraud_risk, max(fraud_risk - 4, 5)]
        }).set_index("Month")

        st.line_chart(trend_df)

    with col_b:
        st.markdown("#### Quick Health Snapshot")
        st.progress(fps_uptime / 100.0)
        st.write(f"FPS Uptime: **{fps_uptime}%**")

        if leakage_index > 50:
            st.error("High Leakage Risk Detected in Supply Chain")
        elif leakage_index > 30:
            st.warning("Moderate Leakage Risk – Needs Monitoring")
        else:
            st.success("Leakage Under Control")

        if fraud_risk > 60:
            st.error("DBT Fraud Risk is CRITICAL")
        elif fraud_risk > 30:
            st.warning("DBT Fraud Risk is ELEVATED")
        else:
            st.success("DBT Fraud Risk is NORMAL")

    st.markdown("#### AI Alert Feed (Simulated)")
    st.write("- 🚨 **Truck diversion suspected** on Route VJA-123 (off-route by 12 km).")
    st.write("- ⚠️ **5,432 ghost cards** flagged in last monthly Aadhaar sync.")
    st.write("- 🚨 **DBT burst pattern** detected in Tirupati cluster (₹1.2 Cr risk).")
    st.write("- ✅ **Quality checks cleared** for latest FCI shipment to Visakhapatnam.")

# ---------- TAB 2: LEAKAGE & MOVEMENT ----------
with tab2:
    st.subheader("AI Module: Supply Chain Leakage Anomaly Detection")

    st.markdown("""
    This view shows how AI watches **truck routes, stock movement, and FPS withdrawals** to detect leakage.
    """)

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("##### Route Deviation vs Alert Level")
        route_df = pd.DataFrame({
            "Route Deviation (%)": [0, 5, 10, 15, 20, leakage_dev],
            "Alert Score": [0, 10, 30, 50, 70, leakage_index]
        })
        st.bar_chart(route_df, x="Route Deviation (%)", y="Alert Score")

    with col_l2:
        st.markdown("##### Sample Route Alert")
        st.write(f"**District:** {district}")
        st.write("**Route ID:** MD-204")
        st.write(f"**Deviation Detected:** {leakage_dev}%")
        st.write(f"**AI Leakage Index:** {leakage_index}")
        if leakage_index > 50:
            st.error("Action Recommended: Immediately contact Enforcement Cell and freeze FPS withdrawals on this route.")
        else:
            st.info("Action: Monitor this route and schedule surprise inspection.")

# ---------- TAB 3: GHOST BENEFICIARIES ----------
with tab3:
    st.subheader("AI Module: Ghost Beneficiary Cleanup")

    st.markdown("""
    This view simulates how AI combines **AePDS, Aadhaar, & ePoS** to identify duplicate or inactive ration cards.
    """)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("##### Ghost % vs Fiscal Loss")
        ghost_df = pd.DataFrame({
            "Ghost %": list(range(0, 21, 5)) + [ghost_pct],
            "Loss (₹ Cr)": [x * 3 for x in range(0, 21, 5)] + [ghost_loss]
        })
        st.area_chart(ghost_df, x="Ghost %", y="Loss (₹ Cr)")

    with col_g2:
        st.markdown("##### Current Cleanup Simulation")
        st.write(f"Estimated Ghost Beneficiaries: **{ghost_pct}%** of cards")
        st.write(f"Estimated Annual Loss: **₹{ghost_loss} Cr**")
        st.success(f"If AI removes 70% of ghost cards, **you save ~₹{round(ghost_loss * 0.7, 1)} Cr/year**.")

        st.markdown("###### How AI flags ghost cards (explained simply):")
        st.write("1. Looks for cards with **no usage for many months**.")
        st.write("2. Compares **names, addresses, Aadhaar IDs** for duplicates.")
        st.write("3. Flags **suspicious patterns** (same Aadhaar used in 2 districts).")

# ---------- TAB 4: FIELD STAFF & FPS ----------
with tab4:
    st.subheader("AI Module: Field Staff Tracking & FPS Monitoring")

    st.markdown("""
    This view shows how inspector visits, FPS uptime, and surprise checks impact **overall PDS health**.
    """)

    visits_completed = int(fps_uptime / 5)
    visits_planned = 25

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("##### Inspector Visit Compliance")
        st.metric("Visits Completed", f"{visits_completed}", f"out of {visits_planned}")
        st.metric("Compliance Rate", f"{int((visits_completed/visits_planned)*100)}%")

        if fps_uptime < 80:
            st.warning("Low FPS uptime – AI recommends targeted inspections in bottom 10% FPS.")
        else:
            st.success("Good FPS uptime – maintain current inspection rhythm.")

    with col_f2:
        st.markdown("##### Simple Visit Log (Demo)")
        inspector_name = st.text_input("Inspector Name", "Ravi Kumar")
        fps_code = st.text_input("FPS Code", "FPS-1039")
        issue_flag = st.selectbox("Any Issue Observed?", ["No Issue", "Stock Mismatch", "Device Offline", "Suspected Diversion"])

        if st.button("Submit Visit Log (Simulated)"):
            st.success(f"Visit recorded for {fps_code} by {inspector_name}. Issue: {issue_flag}")

# ---------- TAB 5: DBT FRAUD ANALYTICS ----------
with tab5:
    st.subheader("AI Module: DBT Fraud Analytics")

    st.markdown("""
    This view simulates how AI watches **DBT transactions** to flag unusual patterns.
    """)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown("##### DBT Anomalies vs Risk Score")
        fraud_df = pd.DataFrame({
            "Anomalies per 10k txns": [0, 50, 100, 200, 300, dbt_anomalies],
            "Risk Score": [0, 20, 40, 60, 80, fraud_risk]
        })
        st.line_chart(fraud_df, x="Anomalies per 10k txns", y="Risk Score")

    with col_d2:
        st.markdown("##### Sample Fraud Case (Simulated)")
        st.write("**Scheme:** Rice Subsidy DBT")
        st.write("**Beneficiary ID:** BEN-98234")
        st.write("**Pattern:** Multiple withdrawals in 3 districts within 24 hours")
        st.write(f"**Anomaly Level:** {fraud_risk}/100")

        if fraud_risk > 60:
            st.error("System Action: AUTO-FREEZE payment & alert State Audit team.")
        elif fraud_risk > 30:
            st.warning("System Action: Mark for manual review within 48 hours.")
        else:
            st.info("System Action: Log only, no immediate intervention.")
