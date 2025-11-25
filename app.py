import streamlit as st
import pandas as pd

# =========================
# BASIC PAGE SETUP
# =========================
st.set_page_config(
    page_title="Civil Supplies AI Command Centre",
    layout="wide"
)

st.title("Civil Supplies AI Command Centre (PoC)")
st.markdown("### AP Civil Supplies · NFSA · Scheme-wise Analytics (Demo)")
st.write("VERSION: Clean reset build (CSV + XLS)")

st.markdown("---")

# =========================
# FILE PATHS
# =========================
# All files must be in the same folder as this app.py
FPS_CSV_PATH = "FPSReportDistrictWiseAsPerLatestRecord.csv"
RC_CSV_PATH = "RCReportDistrictWise.csv"
SALE_DIST_XLS_PATH = "sale_dist.xls"
NFSA_DATE_ABSTRACT_XLS_PATH = "NFSA_Date_Abstract.xls"
SCHEME_SALE_ALLOT_XLS_PATH = "Scheme_Wise_Sale_Allotment_11_2025.xls"

# =========================
# HELPERS
# =========================
@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_data
def load_excel(path: str) -> pd.DataFrame:
    """
    Generic Excel loader.
    For .xls files you may need: pip install xlrd
    """
    return pd.read_excel(path)

def to_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, safely (handles commas)."""
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# =========================
# LOAD DATA (WITH ERRORS SHOWN BUT NOT CRASHING)
# =========================
fps_df = rc_df = sale_dist_df = nfsa_date_df = scheme_sale_df = None

# FPS
try:
    fps_df = load_csv(FPS_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {FPS_CSV_PATH}: {e}")

# RC
try:
    rc_df = load_csv(RC_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {RC_CSV_PATH}: {e}")

# sale_dist.xls
try:
    sale_dist_df = load_excel(SALE_DIST_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {SALE_DIST_XLS_PATH}: {e}")

# NFSA_Date_Abstract.xls
try:
    nfsa_date_df = load_excel(NFSA_DATE_ABSTRACT_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {NFSA_DATE_ABSTRACT_XLS_PATH}: {e}")

# Scheme_Wise_Sale_Allotment_11_2025.xls
try:
    scheme_sale_df = load_excel(SCHEME_SALE_ALLOT_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {SCHEME_SALE_ALLOT_XLS_PATH}: {e}")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "Overview",
    "District-wise FPS / RC",
    "NFSA Date Abstract",
    "Sale Distribution",
    "Scheme-wise Allotment vs Sale",
    "Raw Data Explorer"
])

# =========================
# TAB 1: OVERVIEW
# =========================
with tabs[0]:
    st.subheader("High-level Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    fps_rows = len(fps_df) if fps_df is not None else 0
    rc_rows = len(rc_df) if rc_df is not None else 0
    sale_rows = len(sale_dist_df) if sale_dist_df is not None else 0
    scheme_rows = len(scheme_sale_df) if scheme_sale_df is not None else 0

    col1.metric("FPS rows (district-wise)", fps_rows)
    col2.metric("RC rows (district-wise)", rc_rows)
    col3.metric("Sale Dist rows", sale_rows)
    col4.metric("Scheme-wise rows", scheme_rows)

    st.info("Use the tabs above to explore each dataset slice in this PoC dashboard.")

# =========================
# TAB 2: DISTRICT-WISE FPS / RC
# =========================
with tabs[1]:
    st.subheader("District-wise FPS & Ration Card Summary")

    if fps_df is not None:
        st.markdown("#### FPS (from FPSReportDistrictWiseAsPerLatestRecord.csv)")
        st.dataframe(fps_df, use_container_width=True)
    else:
        st.warning("FPS CSV not loaded.")

    st.markdown("---")

    if rc_df is not None:
        st.markdown("#### Ration Cards (from RCReportDistrictWise.csv)")
        st.dataframe(rc_df, use_container_width=True)
    else:
        st.warning("RC CSV not loaded.")

# =========================
# TAB 3: NFSA DATE ABSTRACT
# =========================
with tabs[2]:
    st.subheader("NFSA Date-wise Abstract")

    if nfsa_date_df is not None:
        st.markdown("Raw table from NFSA_Date_Abstract.xls (first 100 rows).")
        st.dataframe(nfsa_date_df.head(100), use_container_width=True)

        # Let you choose which columns represent Date and Quantity
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
            tmp[value_col] = to_numeric(tmp[value_col])
            tmp = tmp.dropna()

            if not tmp.empty:
                st.line_chart(tmp.set_index(date_col)[value_col])
            else:
                st.warning("No valid data to plot after cleaning.")
    else:
        st.warning("NFSA_Date_Abstract.xls not loaded.")

# =========================
# TAB 4: SALE DISTRIBUTION
# =========================
with tabs[3]:
    st.subheader("Sale Distribution (from sale_dist.xls)")

    if sale_dist_df is not None:
        st.markdown("Raw view (first 100 rows):")
        st.dataframe(sale_dist_df.head(100), use_container_width=True)

        col_options = sale_dist_df.columns.tolist()

        group_col = st.selectbox("Group by column:", col_options)
        value_col = st.selectbox("Value column (amount/qty):", col_options)

        if st.button("Plot Sale Distribution"):
            tmp = sale_dist_df[[group_col, value_col]].copy()
            tmp[value_col] = to_numeric(tmp[value_col])
            agg = (
                tmp.groupby(group_col)[value_col]
                .sum()
                .sort_values(ascending=False)
                .head(20)
            )

            if not agg.empty:
                st.bar_chart(agg)
            else:
                st.warning("No numeric data to plot after aggregation.")
    else:
        st.warning("sale_dist.xls not loaded.")

# =========================
# TAB 5: SCHEME-WISE ALLOTMENT VS SALE
# =========================
with tabs[4]:
    st.subheader("Scheme-wise Allotment vs Sale (Nov 2025)")

    if scheme_sale_df is not None:
        st.markdown("Raw view (first 100 rows) from Scheme_Wise_Sale_Allotment_11_2025.xls:")
        st.dataframe(scheme_sale_df.head(100), use_container_width=True)

        col_options = scheme_sale_df.columns.tolist()
        scheme_col = st.selectbox("Scheme column:", col_options)
        allot_col = st.selectbox("Allotment column:", col_options)
        sale_col = st.selectbox("Sale column:", col_options)

        if st.button("Plot Allotment vs Sale"):
            tmp = scheme_sale_df[[scheme_col, allot_col, sale_col]].copy()

            tmp[allot_col] = to_numeric(tmp[allot_col])
            tmp[sale_col] = to_numeric(tmp[sale_col])

            agg = tmp.groupby(scheme_col)[[allot_col, sale_col]].sum()

            if not agg.empty:
                st.bar_chart(agg)
            else:
                st.warning("No numeric data to plot after aggregation.")
    else:
        st.warning("Scheme_Wise_Sale_Allotment_11_2025.xls not loaded.")

# =========================
# TAB 6: RAW DATA EXPLORER
# =========================
with tabs[5]:
    st.subheader("Raw Data Explorer")

    dataset_options = []
    if fps_df is not None:
        dataset_options.append("FPS CSV")
    if rc_df is not None:
        dataset_options.append("RC CSV")
    if sale_dist_df is not None:
        dataset_options.append("Sale Dist XLS")
    if nfsa_date_df is not None:
        dataset_options.append("NFSA Date Abstract XLS")
    if scheme_sale_df is not None:
        dataset_options.append("Scheme-wise Sale/Allot XLS")

    if not dataset_options:
        st.warning("No datasets loaded. Check that all files are in the same folder as app.py.")
    else:
        choice = st.selectbox("Choose dataset:", dataset_options)

        if choice == "FPS CSV":
            st.write("FPSReportDistrictWiseAsPerLatestRecord.csv")
            st.dataframe(fps_df, use_container_width=True)
        elif choice == "RC CSV":
            st.write("RCReportDistrictWise.csv")
            st.dataframe(rc_df, use_container_width=True)
        elif choice == "Sale Dist XLS":
            st.write("sale_dist.xls")
            st.dataframe(sale_dist_df, use_container_width=True)
        elif choice == "NFSA Date Abstract XLS":
            st.write("NFSA_Date_Abstract.xls")
            st.dataframe(nfsa_date_df, use_container_width=True)
        elif choice == "Scheme-wise Sale/Allot XLS":
            st.write("Scheme_Wise_Sale_Allotment_11_2025.xls")
            st.dataframe(scheme_sale_df, use_container_width=True)
