import streamlit as st
import pandas as pd
import os
from pathlib import Path

# =========================
# BASIC PAGE SETUP
# =========================
st.set_page_config(
    page_title="Civil Supplies AI Command Centre",
    layout="wide"
)

st.title("Civil Supplies AI Command Centre (PoC)")
st.markdown("### AI-driven Fiscal Intelligence for AP Civil Supplies (CSV-only build)")
st.write("VERSION: CSV + Chatbot + NFSA/Sale/Scheme Dashboards")

st.markdown("---")

# =========================
# FILE PATHS (ALL CSV)
# =========================
FPS_CSV_PATH = "FPSReportDistrictWiseAsPerLatestRecord.csv"
RC_CSV_PATH = "RCReportDistrictWise.csv"
NFSA_CSV_PATH = "NFSA_Date_Abstract.csv"
SALE_CSV_PATH = "sale_dist.csv"
SCHEME_CSV_PATH = "Scheme_Wise_Sale_Allotment_11_2025.csv"

# =========================
# SHOW WHERE STREAMLIT IS RUNNING & IF FILES EXIST
# =========================
cwd = os.getcwd()
st.markdown("#### Debug: File Locations")
st.write(f"**Current working folder:** `{cwd}`")

for name in [
    FPS_CSV_PATH,
    RC_CSV_PATH,
    NFSA_CSV_PATH,
    SALE_CSV_PATH,
    SCHEME_CSV_PATH,
]:
    exists = Path(name).exists()
    st.write(f"- `{name}` exists here? **{exists}**")

st.markdown("---")

# =========================
# HELPERS
# =========================
@st.cache_data
def load_csv(path: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.info(f"Could not load '{path}': {e}")
        return None


def to_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, safely (handles commas and junk)."""
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Return columns that can reasonably be treated as numeric
    (after coercion, have at least 1 non-null numeric value).
    """
    cols = []
    for col in df.columns:
        s = to_numeric(df[col])
        if s.notna().sum() > 0:
            cols.append(col)
    return cols


# =========================
# LOAD DATA
# =========================
fps_df = load_csv(FPS_CSV_PATH)
rc_df = load_csv(RC_CSV_PATH)
nfsa_df = load_csv(NFSA_CSV_PATH)
sale_df = load_csv(SALE_CSV_PATH)
scheme_df = load_csv(SCHEME_CSV_PATH)

# =========================
# SIDEBAR: SIMULATION CONTROLS
# =========================
st.sidebar.header("Simulation Controls")

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
st.sidebar.caption(
    "KPIs and risk scores are simulated for PoC demo. "
    "CSVs are used for tables and charts."
)

# =========================
# SIMULATED KPIs
# =========================
leakage_index = round(leakage_dev * 1.5, 1)
ghost_loss = ghost_pct * 3   # ₹ Cr (simulated)
quality_score = 95 if quality_level == "Good" else (78 if quality_level == "Mixed" else 60)
fraud_risk = round(dbt_anomalies / 5, 1)
fiscal_savings = max(
    0,
    round(750 - (leakage_index + ghost_loss + (100 - quality_score) + fraud_risk), 1)
)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Leakage Index", leakage_index, f"{leakage_dev}% deviation")
k2.metric("Ghost Beneficiary Loss (₹ Cr)", ghost_loss, f"{ghost_pct}% ghost")
k3.metric("Quality Score", quality_score, quality_level)
k4.metric("DBT Fraud Risk Score", fraud_risk, f"{dbt_anomalies} alerts/10k")
k5.metric("Estimated Annual Savings (₹ Cr)", fiscal_savings, "Simulated")

st.markdown("---")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "Overview",
    "FPS (District-wise)",
    "Ration Cards (District-wise)",
    "Leakage & Movement",
    "Ghost Beneficiaries",
    "Field Staff & FPS",
    "DBT Fraud Analytics",
    "AI Chatbot",
    "NFSA Date Abstract",
    "Sale Distribution",
    "Scheme-wise Allotment vs Sale",
    "Raw Data Explorer",
])

# =========================
# TAB 1: OVERVIEW
# =========================
with tabs[0]:
    st.subheader("Overview Dashboard")

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("#### Risk Trend (Simulated)")
        trend_df = pd.DataFrame({
            "Month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            "Leakage Index": [
                40,
                38,
                35,
                leakage_index + 2,
                leakage_index,
                max(leakage_index - 3, 10),
            ],
            "Fraud Risk": [
                30,
                28,
                25,
                fraud_risk + 3,
                fraud_risk,
                max(fraud_risk - 4, 5),
            ],
        }).set_index("Month")
        st.line_chart(trend_df)

    with c2:
        st.markdown("#### Health Snapshot")
        st.progress(fps_uptime / 100.0)
        st.write(f"FPS Uptime: **{fps_uptime}%**")

        if leakage_index > 50:
            st.error("High Leakage Risk in Supply Chain")
        elif leakage_index > 30:
            st.warning("Moderate Leakage Risk – Watchlist")
        else:
            st.success("Leakage Under Control")

        if fraud_risk > 60:
            st.error("DBT Fraud Risk is CRITICAL")
        elif fraud_risk > 30:
            st.warning("DBT Fraud Risk is ELEVATED")
        else:
            st.success("DBT Fraud Risk is NORMAL")

    st.markdown("#### AI Alert Feed (Simulated)")
    st.write("- 🚨 Truck diversion suspected on Route VJA-123 (off-route by 12 km).")
    st.write("- ⚠️ 5,432 ghost cards flagged in last Aadhaar sync.")
    st.write("- 🚨 DBT burst pattern detected in Tirupati cluster (₹1.2 Cr risk).")
    st.write("- ✅ Quality checks cleared for latest FCI shipment to Visakhapatnam.")

    st.markdown("#### Real Data Snapshots (from CSVs)")
    if fps_df is not None:
        st.write("FPS CSV (first 10 rows):")
        st.dataframe(fps_df.head(10), use_container_width=True)
    else:
        st.info("FPS CSV not loaded.")

    if rc_df is not None:
        st.write("RC CSV (first 10 rows):")
        st.dataframe(rc_df.head(10), use_container_width=True)
    else:
        st.info("RC CSV not loaded.")

# =========================
# TAB 2: FPS VIEW
# =========================
with tabs[1]:
    st.subheader("FPS District-wise View")

    if fps_df is not None:
        st.dataframe(fps_df, use_container_width=True)
    else:
        st.warning("FPSReportDistrictWiseAsPerLatestRecord.csv not found.")

# =========================
# TAB 3: RC VIEW
# =========================
with tabs[2]:
    st.subheader("Ration Cards District-wise View")

    if rc_df is not None:
        st.dataframe(rc_df, use_container_width=True)
    else:
        st.warning("RCReportDistrictWise.csv not found.")

# =========================
# TAB 4: LEAKAGE & MOVEMENT
# =========================
with tabs[3]:
    st.subheader("AI Module: Supply Chain Leakage Anomaly Detection")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("##### Route Deviation vs Alert Level (Simulated)")
        route_df = pd.DataFrame({
            "Route Deviation (%)": [0, 5, 10, 15, 20, leakage_dev],
            "Alert Score": [0, 10, 30, 50, 70, leakage_index],
        })
        st.bar_chart(route_df, x="Route Deviation (%)", y="Alert Score")

    with col_l2:
        st.markdown("##### Sample Route Alert (Narrative)")
        st.write("**Route ID:** MD-204")
        st.write(f"**Deviation Detected:** {leakage_dev}%")
        st.write(f"**AI Leakage Index:** {leakage_index}")
        if leakage_index > 50:
            st.error("Action: Freeze FPS withdrawals & alert Enforcement Cell.")
        else:
            st.info("Action: Monitor route & schedule surprise inspection.")

# =========================
# TAB 5: GHOST BENEFICIARIES
# =========================
with tabs[4]:
    st.subheader("AI Module: Ghost Beneficiary Cleanup")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("##### Ghost % vs Fiscal Loss (Simulated)")
        ghost_df = pd.DataFrame({
            "Ghost %": list(range(0, 21, 5)) + [ghost_pct],
            "Loss (₹ Cr)": [x * 3 for x in range(0, 21, 5)] + [ghost_loss],
        })
        st.area_chart(ghost_df, x="Ghost %", y="Loss (₹ Cr)")

    with col_g2:
        st.markdown("##### Cleanup Simulation")
        st.write(f"Ghost Cards: **{ghost_pct}%**")
        st.write(f"Estimated Loss: **₹{ghost_loss} Cr**")
        st.success(
            f"Potential AI Cleanup Savings (~70%): **₹{round(ghost_loss * 0.7, 1)} Cr/year**"
        )

# =========================
# TAB 6: FIELD STAFF & FPS
# =========================
with tabs[5]:
    st.subheader("AI Module: Field Staff Tracking & FPS Monitoring")

    visits_completed = int(fps_uptime / 5)
    visits_planned = 25

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("##### Inspector Visit Compliance (Simulated)")
        st.metric("Visits Completed", f"{visits_completed}", f"out of {visits_planned}")
        st.metric(
            "Compliance Rate",
            f"{int((visits_completed / visits_planned) * 100)}%",
        )

    with col_f2:
        st.markdown("##### Simple Visit Log (Demo)")
        inspector_name = st.text_input("Inspector Name", "Ravi Kumar")
        fps_code = st.text_input("FPS Code", "FPS-1039")
        issue_flag = st.selectbox(
            "Any Issue Observed?",
            ["No Issue", "Stock Mismatch", "Device Offline", "Suspected Diversion"],
        )

        if st.button("Submit Visit Log (Simulated)"):
            st.success(f"Visit recorded for {fps_code}. Issue: {issue_flag}")

# =========================
# TAB 7: DBT FRAUD ANALYTICS
# =========================
with tabs[6]:
    st.subheader("AI Module: DBT Fraud Analytics")

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.markdown("##### DBT Anomalies vs Risk Score (Simulated)")
        fraud_df = pd.DataFrame({
            "Anomalies per 10k txns": [0, 50, 100, 200, 300, dbt_anomalies],
            "Risk Score": [0, 20, 40, 60, 80, fraud_risk],
        })
        st.line_chart(fraud_df, x="Anomalies per 10k txns", y="Risk Score")

    with col_d2:
        st.markdown("##### Sample Fraud Case (Simulated)")
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

# =========================
# TAB 8: AI CHATBOT
# =========================
with tabs[7]:
    st.subheader("AI Assistant (Demo)")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []

    st.markdown(
        "Ask questions about the Civil Supplies AI Command Centre, PDS leakages, "
        "DBT fraud detection, or how this PoC works. "
        "This is a simulated chatbot with prepared answers for the demo."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)

    user_input = st.chat_input("Ask something about the Civil Supplies AI system...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        q = user_input.lower()

        if "what is this" in q or "what does this system do" in q or "explain this" in q:
            answer = (
                "This system is a Proof of Concept for an AI-enabled Civil Supplies Command Centre. "
                "It shows how data from AePDS, ePoS, DBT, FPS inspections and quality checks can be combined into one dashboard "
                "so that leakages, ghost beneficiaries and fraud can be detected early and acted on."
            )
        elif "minister" in q or "ias" in q or "secretary" in q:
            answer = (
                "For the Minister and senior IAS officers, this dashboard gives a top-down view: key KPIs like leakage index, "
                "ghost beneficiary loss, DBT fraud risk, FPS uptime and estimated savings. "
                "They can quickly see which districts are healthy, which are at risk and what actions the system recommends."
            )
        elif "leakage" in q or "diversion" in q or "truck" in q or "route" in q:
            answer = (
                "Leakage is detected by monitoring truck GPS routes, stock movement and FPS withdrawals. "
                "If a truck goes off its normal route or the stock issued at FPS does not match what was dispatched, "
                "the AI raises a leakage alert with a risk score for that route or FPS."
            )
        elif "ghost" in q or "beneficiary" in q or "duplicate" in q:
            answer = (
                "Ghost beneficiaries are identified using Aadhaar deduplication, inactivity checks and cross-district pattern analysis. "
                "The system looks for cards that are not used for many months, cards linked to the same Aadhaar or address, "
                "and suspicious claims across multiple locations."
            )
        elif "dbt" in q or "fraud" in q or "payment" in q or "transaction" in q:
            answer = (
                "DBT fraud is detected by analysing transaction patterns. The system flags unusual withdrawal bursts, "
                "multiple withdrawals from different locations for the same beneficiary and amounts that do not match typical behaviour. "
                "High-risk cases can be auto-frozen or sent for audit."
            )
        elif "quality" in q or "grain" in q or "fci" in q or "warehouse" in q:
            answer = (
                "Grain quality is monitored using image-based inspection and simple IoT inputs from warehouses. "
                "If colour, texture or moisture levels look abnormal, AI can flag a batch for manual inspection before it reaches beneficiaries."
            )
        elif "savings" in q or "money" in q or "roi" in q or "benefit" in q:
            answer = (
                "The PoC demonstrates how AI can reduce losses from leakage, ghost cards and fraud. "
                "By acting on these alerts, the department can save a significant portion of recurring losses each year, "
                "while improving reliability and trust in the PDS system."
            )
        elif "data" in q or "source" in q or "where does data come" in q:
            answer = (
                "In the real system, the data would come from AePDS, ePoS devices, DBT payment systems, GPS trackers and warehouse systems. "
                "In this PoC, all risk scores are simulated to show the behaviour without using any real beneficiary data."
            )
        elif "implementation" in q or "how will this be implemented" in q or "next steps" in q:
            answer = (
                "This PoC is the first step. Once approved, the next phases would include connecting to real data sources via APIs, "
                "fine-tuning AI models on Andhra Pradesh data and rolling out the dashboards in pilot districts before statewide scaling."
            )
        else:
            answer = (
                "This PoC chatbot is using prepared answers, not a live AI model. "
                "In simple terms, the system is designed to reduce leakage, clean up beneficiary data, detect DBT fraud and improve FPS performance "
                "using AI-driven analytics."
            )

        st.session_state.chat_history.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.write(answer)

# =========================
# TAB 9: NFSA DATE ABSTRACT (CSV)
# =========================
with tabs[8]:
    st.subheader("NFSA Date-wise Abstract (from NFSA_Date_Abstract.csv)")

    if nfsa_df is not None:
        st.dataframe(nfsa_df.head(200), use_container_width=True)

        date_col = st.selectbox(
            "Select Date column:",
            nfsa_df.columns.tolist()
        )

        num_cols = numeric_columns(nfsa_df)
        if not num_cols:
            st.info("No numeric-like columns found in NFSA CSV for charting.")
        else:
            value_col = st.selectbox(
                "Select Quantity / Value column:",
                num_cols
            )

            if st.button("Plot NFSA Trend"):
                tmp = nfsa_df[[date_col, value_col]].copy()
                tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
                tmp[value_col] = to_numeric(tmp[value_col])
                tmp = tmp.dropna()
                if not tmp.empty:
                    st.line_chart(tmp.set_index(date_col)[value_col])
                else:
                    st.warning("No valid data to plot after cleaning.")
    else:
        st.info("NFSA_Date_Abstract.csv not found.")

# =========================
# TAB 10: SALE DISTRIBUTION (CSV)
# =========================
with tabs[9]:
    st.subheader("Sale Distribution (from sale_dist.csv)")

    if sale_df is not None:
        st.dataframe(sale_df.head(200), use_container_width=True)

        group_col = st.selectbox(
            "Group by column:",
            sale_df.columns.tolist()
        )

        num_cols = numeric_columns(sale_df)
        if not num_cols:
            st.info("No numeric-like columns found in sale_dist CSV for charting.")
        else:
            value_col = st.selectbox(
                "Value column (amount/qty):",
                num_cols
            )

            if st.button("Plot Sale Distribution"):
                tmp = sale_df[[group_col, value_col]].copy()
                tmp[value_col] = to_numeric(tmp[value_col])
                agg = (
                    tmp.groupby(group_col)[value_col]
                    .sum()
                    .sort_values(ascending=False)
                )
                if not agg.empty:
                    st.bar_chart(agg)
                else:
                    st.warning("No numeric data to plot after aggregation.")
    else:
        st.info("sale_dist.csv not found.")

# =========================
# TAB 11: SCHEME-WISE (CSV)
# =========================
with tabs[10]:
    st.subheader("Scheme-wise Allotment vs Sale (from Scheme_Wise_Sale_Allotment_11_2025.csv)")

    if scheme_df is not None:
        st.dataframe(scheme_df.head(200), use_container_width=True)

        scheme_col = st.selectbox(
            "Scheme column:",
            scheme_df.columns.tolist()
        )

        num_cols = numeric_columns(scheme_df)
        if len(num_cols) < 2:
            st.info(
                "Need at least two numeric-like columns (e.g., Allotment & Sale) "
                "to plot a comparison chart."
            )
        else:
            allot_col = st.selectbox(
                "Allotment column:",
                num_cols,
                key="scheme_allot"
            )
            sale_col = st.selectbox(
                "Sale column:",
                num_cols,
                key="scheme_sale"
            )

            if st.button("Plot Scheme-wise Allotment vs Sale"):
                tmp = scheme_df[[scheme_col, allot_col, sale_col]].copy()
                tmp[allot_col] = to_numeric(tmp[allot_col])
                tmp[sale_col] = to_numeric(tmp[sale_col])
                agg = tmp.groupby(scheme_col)[[allot_col, sale_col]].sum()
                if not agg.empty:
                    st.bar_chart(agg)
                else:
                    st.warning("No numeric data to plot after aggregation.")
    else:
        st.info("Scheme_Wise_Sale_Allotment_11_2025.csv not found.")

# =========================
# TAB 12: RAW DATA EXPLORER
# =========================
with tabs[11]:
    st.subheader("Raw Data Explorer")

    datasets = {}
    if fps_df is not None:
        datasets["FPS CSV"] = fps_df
    if rc_df is not None:
        datasets["RC CSV"] = rc_df
    if nfsa_df is not None:
        datasets["NFSA CSV"] = nfsa_df
    if sale_df is not None:
        datasets["Sale Dist CSV"] = sale_df
    if scheme_df is not None:
        datasets["Scheme-wise CSV"] = scheme_df

    if not datasets:
        st.warning("No datasets loaded. Check that CSV files exist next to app.py.")
    else:
        choice = st.selectbox("Select dataset:", list(datasets.keys()))
        st.dataframe(datasets[choice], use_container_width=True)
