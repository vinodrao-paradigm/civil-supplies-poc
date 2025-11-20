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
    "DBT Fraud Analytics",
    "AI Chatbot"
])

# ---------- TAB 1: OVERVIEW ----------
with tab1:
    st.subheader(f"State Overview - {district}")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("#### Trend of Risk Scores (Simulated)")
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
            st.error("Action Recommended: Immediately contact Enforcement Cell and freeze FPS withdrawals.")
        else:
            st.info("Action: Monitor this route and schedule surprise inspection.")

# ---------- TAB 3: GHOST BENEFICIARIES ----------
with tab3:
    st.subheader("AI Module: Ghost Beneficiary Cleanup")

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
        st.write(f"Ghost Cards: **{ghost_pct}%**")
        st.write(f"Estimated Loss: **₹{ghost_loss} Cr**")
        st.success(f"AI Cleanup Savings (~70%): **₹{round(ghost_loss * 0.7, 1)} Cr/year**")

# ---------- TAB 4: FIELD STAFF & FPS ----------
with tab4:
    st.subheader("AI Module: Field Staff Tracking & FPS Monitoring")

    visits_completed = int(fps_uptime / 5)
    visits_planned = 25

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("##### Inspector Visit Compliance")
        st.metric("Visits Completed", f"{visits_completed}", f"out of {visits_planned}")
        st.metric("Compliance Rate", f"{int((visits_completed/visits_planned)*100)}%")

    with col_f2:
        st.markdown("##### Simple Visit Log (Demo)")
        inspector_name = st.text_input("Inspector Name", "Ravi Kumar")
        fps_code = st.text_input("FPS Code", "FPS-1039")
        issue_flag = st.selectbox("Any Issue Observed?", ["No Issue", "Stock Mismatch", "Device Offline", "Suspected Diversion"])

        if st.button("Submit Visit Log (Simulated)"):
            st.success(f"Visit recorded for {fps_code}. Issue: {issue_flag}")

# ---------- TAB 5: DBT FRAUD ANALYTICS ----------
with tab5:
    st.subheader("AI Module: DBT Fraud Analytics")

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown("##### DBT Anomalies vs Risk Score")
        fraud_df = pd.DataFrame({
            "Anomalies per 10k txns": [0, 50, 100, 200, 300, dbt_anomalies],
            "Risk Score": [0, 20, 40, 60, 80, fraud_risk]
        })
        st.line_chart(fraud_df, x="Anomalies per 10k txns", y="Risk Score")

    with col_d2:
        st.markdown("##### Sample Fraud Case")
        st.write("**Scheme:** Rice Subsidy DBT")
        st.write("**Beneficiary ID:** BEN-98234")
        st.write("**Pattern:** Multiple withdrawals in 3 districts within 24 hours")
        st.write(f"**Risk Score:** {fraud_risk}")

        if fraud_risk > 60:
            st.error("Action: AUTO-FREEZE payment & alert Audit Dept.")
        elif fraud_risk > 30:
            st.warning("Action: Send for manual review.")
        else:
            st.info("Action: Log only, no intervention.")
# ---------- TAB 6: SIMPLE DEMO CHATBOT ----------
with tab6:
    st.subheader("AI Assistant (Demo)")

    st.markdown("""
    Ask questions about the Civil Supplies AI Command Centre, PDS leakages, DBT fraud detection, or how this PoC works.
    This is a **simulated** chatbot with carefully prepared answers for the demo.
    """)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show previous messages
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)

    user_input = st.chat_input("Ask something about the Civil Supplies AI system...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        query = user_input.lower()

        # --- TOPIC-BASED CANNED ANSWERS ---

        if "what is this" in query or "what does this system do" in query or "explain this system" in query:
            answer = (
                "This system is a Proof of Concept for an AI-enabled Civil Supplies Command Centre. "
                "It shows how data from AePDS, ePoS, DBT, FPS inspections and quality checks can be combined into one dashboard, "
                "so that leakages, ghost beneficiaries, and fraud can be detected early and acted on."
            )

        elif "minister" in query or "ias" in query or "secretary" in query:
            answer = (
                "For the Minister and senior IAS officers, this dashboard gives a top-down view: key KPIs like leakage index, "
                "ghost beneficiary loss, DBT fraud risk, FPS uptime and estimated savings. "
                "They can quickly see which districts are healthy, which are at risk, and what actions the system recommends."
            )

        elif "leakage" in query or "diversion" in query or "truck" in query or "route" in query:
            answer = (
                "Leakage is detected by monitoring truck GPS routes, stock movement and FPS withdrawals. "
                "If a truck goes off its normal route or the stock issued at FPS does not match what was dispatched, "
                "the AI raises a leakage alert with a risk score for that route or FPS."
            )

        elif "ghost" in query or "beneficiary" in query or "duplicate" in query:
            answer = (
                "Ghost beneficiaries are identified using Aadhaar deduplication, inactivity checks and cross-district pattern analysis. "
                "The system looks for cards that are not used for many months, cards linked to the same Aadhaar or address, "
                "and suspicious claims across multiple locations."
            )

        elif "dbt" in query or "fraud" in query or "payment" in query or "transaction" in query:
            answer = (
                "DBT fraud is detected by analysing transaction patterns. The system flags unusual withdrawal bursts, "
                "multiple withdrawals from different locations for the same beneficiary, and amounts that do not match typical behaviour. "
                "High-risk cases can be auto-frozen or sent for audit."
            )

        elif "quality" in query or "grain" in query or "fcI" in query or "warehouse" in query:
            answer = (
                'Grain quality is monitored using image-based inspection and simple IoT inputs from warehouses. '
                "If colour, texture or moisture levels look abnormal, AI can flag a batch for manual inspection before it reaches beneficiaries."
            )

        elif "savings" in query or "money" in query or "roi" in query or "benefit" in query:
            answer = (
                "The PoC demonstrates how AI can reduce losses from leakage, ghost cards, and fraud. "
                "By acting on these alerts, the department can save a significant portion of recurring losses each year, "
                "while improving reliability and trust in the PDS system."
            )

        elif "data" in query or "source" in query or "where does data come" in query:
            answer = (
                "In the real system, the data would come from AePDS, ePoS devices, DBT payment systems, GPS trackers and warehouse systems. "
                "In this PoC, all numbers are simulated to show the behaviour and experience without using any real government data."
            )

        elif "implementation" in query or "how will this be implemented" in query or "next steps" in query:
            answer = (
                "This PoC is the first step. Once approved, the next phases would include: connecting to real data sources via APIs, "
                "fine-tuning AI models on Andhra Pradesh data, and rolling out the dashboards for pilot districts before statewide scaling."
            )

        elif "dashboard" in query or "screen" in query or "tab" in query:
            answer = (
                "The dashboard is organised into tabs: an overview for leadership, and separate views for leakage, ghost beneficiaries, "
                "field staff/FPS monitoring and DBT fraud analytics. Each tab shows KPIs, trends, and example alerts to demonstrate how AI supports decisions."
            )

        else:
            # More helpful default answer
            answer = (
                "This PoC chatbot is using prepared answers, not a live AI model. "
                "I couldn't match your exact question to a topic, but in simple terms: this system is designed to "
                "reduce leakage, clean up beneficiary data, detect DBT fraud and improve FPS performance using AI-driven analytics. "
                "You can try asking about leakage, ghost beneficiaries, DBT fraud, grain quality, data sources or how this helps the Minister."
            )

        st.session_state.chat_history.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.write(answer)

