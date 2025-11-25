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
st.markdown("### AP Civil Supplies · FPS & Ration Card Analytics (Minimal Stable Build)")
st.write("VERSION: CSV-only reset (no XLS dependencies)")

st.markdown("---")

# =========================
# FILE PATHS
# =========================
# All files must be in the same folder as this app.py
FPS_CSV_PATH = "FPSReportDistrictWiseAsPerLatestRecord.csv"
RC_CSV_PATH = "RCReportDistrictWise.csv"

# =========================
# HELPERS
# =========================
@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def to_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, safely (handles commas)."""
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# =========================
# LOAD DATA (WITH ERRORS SHOWN BUT NOT CRASHING)
# =========================
fps_df = rc_df = None

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

# =========================
# TABS
# =========================
tabs = st.tabs([
    "Overview",
    "FPS (District-wise)",
    "Ration Cards (District-wise)",
    "FPS vs RC Join",
    "Raw Data Explorer"
])

# =========================
# TAB 1: OVERVIEW
# =========================
with tabs[0]:
    st.subheader("High-level Snapshot (CSV-only)")

    col1, col2 = st.columns(2)

    fps_rows = len(fps_df) if fps_df is not None else 0
    rc_rows = len(rc_df) if rc_df is not None else 0

    col1.metric("FPS rows (district-wise)", fps_rows)
    col2.metric("RC rows (district-wise)", rc_rows)

    st.info(
        "This reset build only uses the two CSV files:\n\n"
        "- FPSReportDistrictWiseAsPerLatestRecord.csv\n"
        "- RCReportDistrictWise.csv\n\n"
        "All XLS-based features are temporarily disabled so the app is stable again."
    )

# =========================
# TAB 2: FPS (DISTRICT-WISE)
# =========================
with tabs[1]:
    st.subheader("FPS District-wise View")

    if fps_df is not None:
        st.markdown("#### FPS (from FPSReportDistrictWiseAsPerLatestRecord.csv)")
        st.dataframe(fps_df, use_container_width=True)

        # Simple grouping if there is any obvious numeric column
        numeric_cols = fps_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.markdown("#### Quick Aggregation")
            group_col = st.selectbox("Group by column (e.g. district):", fps_df.columns.tolist())
            value_col = st.selectbox("Numeric column to sum:", numeric_cols)

            if st.button("Plot FPS aggregation"):
                tmp = fps_df[[group_col, value_col]].copy()
                agg = tmp.groupby(group_col)[value_col].sum().sort_values(ascending=False)
                st.bar_chart(agg.head(20))
        else:
            st.info("No obvious numeric columns to aggregate in FPS CSV.")
    else:
        st.warning("FPS CSV not loaded. Check that FPSReportDistrictWiseAsPerLatestRecord.csv is in the same folder as app.py.")

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
            st.markdown("#### Quick Aggregation")
            group_col = st.selectbox("Group by column (e.g. district):", rc_df.columns.tolist(), key="rc_group")
            value_col = st.selectbox("Numeric column to sum:", numeric_cols, key="rc_val")

            if st.button("Plot RC aggregation"):
                tmp = rc_df[[group_col, value_col]].copy()
                agg = tmp.groupby(group_col)[value_col].sum().sort_values(ascending=False)
                st.bar_chart(agg.head(20))
        else:
            st.info("No obvious numeric columns to aggregate in RC CSV.")
    else:
        st.warning("RC CSV not loaded. Check that RCReportDistrictWise.csv is in the same folder as app.py.")

# =========================
# TAB 4: FPS vs RC JOIN
# =========================
with tabs[3]:
    st.subheader("FPS vs RC Join (by common district column)")

    if fps_df is not None and rc_df is not None:
        st.markdown("Select the join columns (the ones that represent the same district/key in both files).")

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
# TAB 5: RAW DATA EXPLORER
# =========================
with tabs[4]:
    st.subheader("Raw Data Explorer")

    dataset_options = []
    if fps_df is not None:
        dataset_options.append("FPS CSV")
    if rc_df is not None:
        dataset_options.append("RC CSV")

    if not dataset_options:
        st.warning("No datasets loaded. Check that both CSV files are in the same folder as app.py.")
    else:
        choice = st.selectbox("Choose dataset:", dataset_options)

        if choice == "FPS CSV":
            st.write("FPSReportDistrictWiseAsPerLatestRecord.csv")
            st.dataframe(fps_df, use_container_width=True)
        elif choice == "RC CSV":
            st.write("RCReportDistrictWise.csv")
            st.dataframe(rc_df, use_container_width=True)
