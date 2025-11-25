import streamlit as st
import pandas as pd

# ---------- BASIC PAGE SETUP ----------
st.set_page_config(
    page_title="Civil Supplies AI Command Centre",
    layout="wide"
)

st.title("Civil Supplies AI Command Centre (PoC)")
st.markdown("### Simulated AI-driven Fiscal & PDS Intelligence for Andhra Pradesh")
st.write("VERSION: CSV + NFSA + Scheme-wise Build")

st.markdown("---")

# ---------- FILE PATHS ----------
FPS_CSV_PATH = "FPSReportDistrictWiseAsPerLatestRecord.csv"
RC_CSV_PATH = "RCReportDistrictWise.csv"
SALE_DIST_XLS_PATH = "sale_dist.xls"
NFSA_DATE_ABSTRACT_XLS_PATH = "NFSA_Date_Abstract.xls"
SCHEME_SALE_ALLOT_XLS_PATH = "Scheme_Wise_Sale_Allotment_11_2025.xls"

# ---------- DATA LOAD HELPERS ----------
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

@st.cache_data
def load_xls(path):
    return pd.read_excel(path)

# ---------- LOAD DATA ----------
try:
    fps_df = load_csv(FPS_CSV_PATH)
except Exception as e:
    fps_df = None
    st.error(f"Could not load FPS CSV: {e}")

try:
    rc_df = load_csv(RC_CSV_PATH)
except Exception as e:
    rc_df = None
    st.error(f"Could not load RC CSV: {e}")

try:
    sale_dist_df = load_xls(SALE_DIST_XLS_PATH)
except Exception as e:
    sale_dist_df = None
    st.error(f"Could not load sale_dist.xls: {e}")

try:
    nfsa_date_df = load_xls(NFSA_DATE_ABSTRACT_XLS_PATH)
except Exception as e:
    nfsa_date_df = None
    st.error(f"Could not load NFSA_Date_Abstract.xls: {e}")

try:
    scheme_sale_df = load_xls(SCHEME_SALE_ALLOT_XLS_PATH)
except Exception as e:
    scheme_sale_df = None
    st.error(f"Could not load Scheme_Wise_Sale_Allotment_11_2025.xls: {e}")

# ---------- TABS LAYOUT ----------
tabs = st.tabs([
    "Overview",
    "District-wise FPS / RC",
    "NFSA Date Abstract",
    "Sale Distribution",
    "Scheme-wise Allotment vs Sale",
    "Raw Data"
])

# ---------- TAB 1: OVERVIEW ----------
with tabs[0]:
    st.subheader("High-level Snapshot")

    cols = st.columns(4)

    fps_rows = len(fps_df) if fps_df is not None else 0
    rc_rows = len(rc_df) if rc_df is not None else 0
    sale_rows = len(sale_dist_df) if sale_dist_df is not None else 0
    scheme_rows = len(scheme_sale_df) if scheme_sale_df is not None else 0

    with cols[0]:
        st.metric("FPS rows", value=fps_rows)
    with cols[1]:
        st.metric("RC rows", value=rc_rows)
    with cols[2]:
        st.metric("Sale Dist rows", value=sale_rows)
    with cols[3]:
        st.metric("Scheme-wise rows", value=scheme_rows)

    st.info("Use the tabs above to explore each dataset slice for the PoC.")

# ---------- TAB 2: DISTRICT-WISE FPS / RC ----------
with tabs[1]:
    st.subheader("District-wise FPS & Ration Card Summary")

    if fps_df is not None:
        st.markdown("#### FPS (from FPSReportDistrictWiseAsPerLatestRecord.csv)")
        st.dataframe(fps_df)

    if rc_df is not None:
        st.markdown("#### Ration Cards (from RCReportDistrictWise.csv)")
        st.dataframe(rc_df)

# ---------- TAB 3: NFSA DATE ABSTRACT ----------
with tabs[2]:
    st.subheader("NFSA Date-wise Abstract")

    if nfsa_date_df is not None:
        st.markdown("Raw table from NFSA_Date_Abstract.xls (first 100 rows).")
        st.dataframe(nfsa_date_df.head(100))

        date_col = st.selectbox(
            "Select Date column:",
            nfsa_date_df.columns.tolist()
        )
        value_col = st.selectbox(
            "Select Quantity / Value column:",
            nfsa_date_df.columns.tolist()
        )

        if st.button("Plot Date-wise Trend"):
            tmp = nfsa_date_df[[date_col, value_col]].copy()
            tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
            tmp[value_col] = pd.to_numeric(
                tmp[value_col].astype(str).str.replace(",", ""),
                errors="coerce"
            )
            tmp = tmp.dropna()

            st.line_chart(tmp.set_index(date_col)[value_col])
    else:
        st.warning("NFSA_Date_Abstract.xls not loaded.")

# ---------- TAB 4: SALE DISTRIBUTION ----------
with tabs[3]:
    st.subheader("Sale Distribution")

    if sale_dist_df is not None:
        st.markdown("Raw view (first 100 rows):")
        st.dataframe(sale_dist_df.head(100))

        col_options = sale_dist_df.columns.tolist()

        group_col = st.selectbox("Group by colu_
