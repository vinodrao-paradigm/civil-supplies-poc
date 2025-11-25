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
st.markdown("### AP Civil Supplies · FPS, Ration Cards, NFSA & Scheme-wise Analytics")
st.write("VERSION: Dashboard-style build (CSV core, XLS optional)")

st.markdown("---")

# =========================
# FILE PATHS
# =========================
# All files should be in the same folder as app.py
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
    If this is .xls and xlrd isn't installed, it will raise an error which we catch.
    """
    return pd.read_excel(path)

def to_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, safely (handles commas)."""
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# =========================
# LOAD DATA (NEVER CRASHES APP)
# =========================
fps_df = rc_df = sale_dist_df = nfsa_date_df = scheme_sale_df = None

# FPS CSV
try:
    fps_df = load_csv(FPS_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {FPS_CSV_PATH}: {e}")

# RC CSV
try:
    rc_df = load_csv(RC_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {RC_CSV_PATH}: {e}")

# sale_dist.xls (optional)
try:
    sale_dist_df = load_excel(SALE_DIST_XLS_PATH)
except Exception as e:
    sale_dist_df = None
    st.warning(f"Optional file {SALE_DIST_XLS_PATH} not loaded: {e}")

# NFSA_Date_Abstract.xls (optional)
try:
    nfsa_date_df = load_excel(NFSA_DATE_ABSTRACT_XLS_PATH)
except Exception as e:
    nfsa_date_df = None
    st.warning(f"Optional file {NFSA_DATE_ABSTRACT_XLS_PATH} not loaded: {e}")

# Scheme_Wise_Sale_Allotment_11_2025.xls (optional)
try:
    scheme_sale_df = load_excel(SCHEME_SALE_ALLOT_XLS_PATH)
except Exception as e:
    scheme_sale_df = None
    st.warning(f"Optional file {SCHEME_SALE_ALLOT_XLS_PATH} not loaded: {e}")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "Overview",
    "FPS (District-wise)",
    "Ration Cards (District-wise)",
    "FPS vs RC Join",
    "NFSA Date Abstract",
    "Sale Distribution",
    "Scheme-wise Allotment vs Sale",
    "Raw Data Explorer"
])

# =========================
# TAB 1: OVERVIEW / DASHBOARD
# =========================
with tabs[0]:
    st.subheader("Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    fps_rows = len(fps_df) if fps_df is not None else 0
    rc_rows = len(rc_df) if rc_df is not None else 0
    sale_rows = len(sale_dist_df) if sale_dist_df is not None else 0
    scheme_rows = len(scheme_sale_df) if scheme_sale_df is not None else 0

    col1.metric("FPS rows (district-wise)", fps_rows)
    col2.metric("RC rows (district-wise)", rc_rows)
    col3.metric("Sale Dist rows (if file present)", sale_rows)
    col4.metric("Scheme-wise rows (if file present)", scheme_rows)

    st.markdown("### Quick Charts from CSVs (Always Available)")

    # Simple chart from RC (e.g., by some column)
    if rc_df is not None:
        st.markdown("#### Sample Aggregation from RC CSV")
        numeric_cols_rc = rc_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols_rc:
            gcol, vcol = st.columns(2)
            with gcol:
                rc_group_col = st.selectbox("Group RC by column:", rc_df.columns.tolist(), key="ov_rc_group")
            with vcol:
                rc_val_col = st.selectbox("RC numeric column:", numeric_cols_rc, key="ov_rc_val")

            tmp = rc_df[[rc_group_col, rc_val_col]].copy()
            agg = tmp.groupby(rc_group_col)[rc_val_col].sum().sort_values(ascending=False).head(15)
            st.bar_chart(agg)
        else:
            st.info("No numeric columns detected in RC CSV for quick aggregation.")

    else:
        st.warning("RC CSV not loaded, so overview chart based on RC is skipped.")

# =========================
# TAB 2: FPS (DISTRICT-WISE)
# =========================
with tabs[1]:
    st.subheader("FPS District-wise View")

    if fps_df is not None:
        st.markdown("#### FPS (from FPSReportDistrictWiseAsPerLatestRecord.csv)")
        st.dataframe(fps_df, use_container_width=True)

        numeric_cols = fps_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.markdown("#### FPS Aggregation")
            group_col = st.selectbox("Group by column:", fps_df.columns.tolist(), key="fps_group")
            value_col = st.selectbox("Numeric column to sum:", numeric_cols, key="fps_val")

            if st.button("Plot FPS aggregation"):
                tmp = fps_df[[group_col, value_col]].copy()
                agg = tmp.groupby(group_col)[value_col].sum().sort_values(ascending=False)
                st.bar_chart(agg.head(20))
        else:
            st.info("No numeric columns to aggregate in FPS CSV.")
    else:
        st.warning("FPS CSV not loaded. Ensure FPSReportDistrictWiseAsPerLatestRecord.csv is in the same folder as app.py.")

# =========================
# TAB 3: RATION CARDS (DISTRICT-WISE)
# =========================
with tabs[2]:
    st.subheader("Ration Cards District-wise View")

    if rc_df is not None:
        st.markdown("#### Ration Cards (from RCReportDistrictWise.csv)")
        st.dataframe(rc_df, use_container_width=True)

        numeric_cols = rc_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.markdown("#### RC Aggregation")
            group_col = st.selectbox("Group by column:", rc_df.columns.tolist(), key="rc_group2")
            value_col = st.selectbox("Numeric column to sum:", numeric_cols, key="rc_val2")

            if st.button("Plot RC aggregation"):
                tmp = rc_df[[group_col, value_col]].copy()
                agg = tmp.groupby(group_col)[value_col].sum().sort_values(ascending=False)
                st.bar_chart(agg.head(20))
        else:
            st.info("No numeric columns to aggregate in RC CSV.")
    else:
        st.warning("RC CSV not loaded. Ensure RCReportDistrictWise.csv is in the same folder as app.py.")

# =========================
# TAB 4: FPS vs RC JOIN
# =========================
with tabs[3]:
    st.subheader("FPS vs RC Join (by common district column)")

    if fps_df is not None and rc_df is not None:
        st.markdown("Select the columns that represent the same district/key in both files.")

        colj1, colj2 = st.columns(2)
        with colj1:
            fps_join_col = st.selectbox("FPS join column:", fps_df.columns.tolist())
        with colj2:
            rc_join_col = st.selectbox("RC join column:", rc_df.columns.tolist())

        if st.button("Join FPS & RC"):
            joined = fps_df.merge(
                rc_df,
                left_on=fps_join_col,
                right_on=rc_join_col,
                how="inner",
                suffixes=("_FPS", "_RC")
            )
            st.success(f"Joined dataframe has {len(joined)} rows.")
            st.dataframe(joined.head(100), use_container_width=True)
    else:
        st.warning("Need both FPS and RC CSVs loaded to perform join.")

# =========================
# TAB 5: NFSA DATE ABSTRACT (OPTIONAL XLS)
# =========================
with tabs[4]:
    st.subheader("NFSA Date-wise Abstract (from NFSA_Date_Abstract.xls)")

    if nfsa_date_df is not None:
        st.markdown("Raw table (first 100 rows):")
        st.dataframe(nfsa_date_df.head(100), use_container_width=True)

        date_col = st.selectbox(
            "Select Date column:",
            nfsa_date_df.columns.tolist()
        )
        value_col = st.selectbox(
            "Select Quantity / Value column:",
            nfsa_date_df.columns.tolist()
        )

        if st.button("Plot NFSA Date-wise Trend"):
            tmp = nfsa_date_df[[date_col, value_col]].copy()
            tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
            tmp[value_col] = to_numeric(tmp[value_col])
            tmp = tmp.dropna()

            if not tmp.empty:
                st.line_chart(tmp.set_index(date_col)[value_col])
            else:
                st.warning("No valid data to plot after cleaning.")
    else:
        st.warning(
            "NFSA_Date_Abstract.xls not loaded. "
            "Place it in the same folder as app.py to enable this tab."
        )

# =========================
# TAB 6: SALE DISTRIBUTION (OPTIONAL XLS)
# =========================
with tabs[5]:
    st.subheader("Sale Distribution (from sale_dist.xls)")

    if sale_dist_df is not None:
        st.markdown("Raw view (first 100 rows):")
        st.dataframe(sale_dist_df.head(100), use_container_width=True)

        col_options = sale_dist_df.columns.tolist()
        group_col = st.selectbox("Group by column:", col_options, key="sale_group")
        value_col = st.selectbox("Value column (amount/qty):", col_options, key="sale_val")

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
        st.warning(
            "sale_dist.xls not loaded. "
            "Place it in the same folder as app.py to enable this tab."
        )

# =========================
# TAB 7: SCHEME-WISE ALLOTMENT VS SALE (OPTIONAL XLS)
# =========================
with tabs[6]:
    st.subheader("Scheme-wise Allotment vs Sale (from Scheme_Wise_Sale_Allotment_11_2025.xls)")

    if scheme_sale_df is not None:
        st.markdown("Raw view (first 100 rows):")
        st.dataframe(scheme_sale_df.head(100), use_container_width=True)

        col_options = scheme_sale_df.columns.tolist()
        scheme_col = st.selectbox("Scheme column:", col_options, key="scheme_col")
        allot_col = st.selectbox("Allotment column:", col_options, key="allot_col")
        sale_col = st.selectbox("Sale column:", col_options, key="sale_col")

        if st.button("Plot Scheme-wise Allotment vs Sale"):
            tmp = scheme_sale_df[[scheme_col, allot_col, sale_col]].copy()

            tmp[allot_col] = to_numeric(tmp[allot_col])
            tmp[sale_col] = to_numeric(tmp[sale_col])

            agg = tmp.groupby(scheme_col)[[allot_col, sale_col]].sum()

            if not agg.empty:
                st.bar_chart(agg)
            else:
                st.warning("No numeric data to plot after aggregation.")
    else:
        st.warning(
            "Scheme_Wise_Sale_Allotment_11_2025.xls not loaded. "
            "Place it in the same folder as app.py to enable this tab."
        )

# =========================
# TAB 8: RAW DATA EXPLORER
# =========================
with tabs[7]:
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
        st.warning("No datasets loaded. Check that at least the CSV files are in the same folder as app.py.")
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
