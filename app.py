import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------
# BASIC PAGE SETUP
# -----------------------------------
st.set_page_config(
    page_title="Civil Supplies AI Command Centre (PoC)",
    layout="wide"
)

st.title("Civil Supplies AI Command Centre (PoC)")
st.markdown("### AP Civil Supplies · NFSA · Scheme-wise Analytics (Demo Dashboard)")
st.write("VERSION: Multi-file build with joins, heatmaps, anomalies & AI-style insights")
st.markdown("---")

# -----------------------------------
# FILE PATHS (KEEP IN SAME FOLDER AS app.py)
# -----------------------------------
FPS_CSV_PATH = "FPSReportDistrictWiseAsPerLatestRecord.csv"
RC_CSV_PATH = "RCReportDistrictWise.csv"
SALE_DIST_XLS_PATH = "sale_dist.xls"
NFSA_DATE_ABSTRACT_XLS_PATH = "NFSA_Date_Abstract.xls"
SCHEME_SALE_ALLOT_XLS_PATH = "Scheme_Wise_Sale_Allotment_11_2025.xls"
DISTRICT_LAT_LONG_CSV = "district_lat_long.csv"  # optional

# -----------------------------------
# HELPERS TO LOAD DATA
# -----------------------------------
@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_data
def load_xls(path: str) -> pd.DataFrame:
    # For .xls files we typically need xlrd
    return pd.read_excel(path, engine="xlrd")

@st.cache_data
def safe_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, stripping commas."""
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

@st.cache_data
def join_on_columns(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_col: str,
    right_col: str
) -> pd.DataFrame:
    return left_df.merge(
        right_df,
        left_on=left_col,
        right_on=right_col,
        how="inner",
        suffixes=("_FPS", "_RC")
    )

@st.cache_data
def load_district_lat_long(path: str) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(path)
        # expecting: district, lat, lon
        return df
    except Exception:
        return None

# -----------------------------------
# LOAD ALL DATASETS (WITH ERROR HANDLING)
# -----------------------------------
fps_df = rc_df = sale_dist_df = nfsa_date_df = scheme_sale_df = district_geo_df = None

try:
    fps_df = load_csv(FPS_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {FPS_CSV_PATH}: {e}")

try:
    rc_df = load_csv(RC_CSV_PATH)
except Exception as e:
    st.error(f"Could not load {RC_CSV_PATH}: {e}")

try:
    sale_dist_df = load_xls(SALE_DIST_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {SALE_DIST_XLS_PATH}: {e}")

try:
    nfsa_date_df = load_xls(NFSA_DATE_ABSTRACT_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {NFSA_DATE_ABSTRACT_XLS_PATH}: {e}")

try:
    scheme_sale_df = load_xls(SCHEME_SALE_ALLOT_XLS_PATH)
except Exception as e:
    st.error(f"Could not load {SCHEME_SALE_ALLOT_XLS_PATH}: {e}")

# Optional district geo file
district_geo_df = load_district_lat_long(DISTRICT_LAT_LONG_CSV)

# -----------------------------------
# TABS
# -----------------------------------
tabs = st.tabs([
    "Overview",
    "District-wise FPS / RC & Join",
    "NFSA Date Abstract",
    "Sale Distribution",
    "Scheme-wise Allotment vs Sale",
    "Heatmaps & Map",
    "AI Insights (Demo)",
    "Raw Data Explorer"
])

# -----------------------------------
# TAB 1: OVERVIEW
# -----------------------------------
with tabs[0]:
    st.subheader("High-level Snapshot & KPIs")

    col1, col2, col3, col4 = st.columns(4)

    fps_rows = len(fps_df) if fps_df is not None else 0
    rc_rows = len(rc_df) if rc_df is not None else 0
    sale_rows = len(sale_dist_df) if sale_dist_df is not None else 0
    scheme_rows = len(scheme_sale_df) if scheme_sale_df is not None else 0

    with col1:
        st.metric("FPS rows (district-wise file)", value=fps_rows if fps_rows else "N/A")
    with col2:
        st.metric("RC rows (district-wise file)", value=rc_rows if rc_rows else "N/A")
    with col3:
        st.metric("NFSA Date Abstract rows", value=len(nfsa_date_df) if nfsa_date_df is not None else "N/A")
    with col4:
        st.metric("Scheme-wise Allotment/Sale rows", value=scheme_rows if scheme_rows else "N/A")

    st.markdown("---")
    st.markdown("""
    **How to use this PoC:**
    - **District-wise FPS / RC & Join**: See core structural data and join on district codes.
    - **NFSA Date Abstract**: Date-wise analytics with quick charting.
    - **Sale Distribution**: Group & plot sales by district/scheme/FPS.
    - **Scheme-wise Allotment vs Sale**: Compare Allotment vs Sale for November 2025.
    - **Heatmaps & Map**: Table heatmaps and optional geo map (if district lat/long is provided).
    - **AI Insights (Demo)**: Rule-based 'AI-style' summaries & anomaly detection.
    - **Raw Data Explorer**: Inspect any dataset quickly.
    """)

    # Example simple KPI: if scheme_sale_df has obvious numeric columns
    if scheme_sale_df is not None:
        st.markdown("#### Quick KPI Guess (from Scheme-wise Allotment vs Sale)")
        num_cols = scheme_sale_df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) >= 2:
            allot_guess = num_cols[0]
            sale_guess = num_cols[1]
            total_allot = scheme_sale_df[allot_guess].sum()
            total_sale = scheme_sale_df[sale_guess].sum()
            coverage = (total_sale / total_allot * 100) if total_allot else None
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Allotment (guessed)", value=f"{total_allot:,.0f}")
            with c2:
                st.metric("Total Sale (guessed)", value=f"{total_sale:,.0f}")
            with c3:
                st.metric("Sale vs Allotment (%)", value=f"{coverage:.1f}%" if coverage is not None else "N/A")
        else:
            st.info("Once we know exact allotment/sale columns, KPIs can be made more precise.")

# -----------------------------------
# TAB 2: DISTRICT-WISE FPS / RC + JOIN
# -----------------------------------
with tabs[1]:
    st.subheader("District-wise FPS & Ration Card Summary + Join")

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

    st.markdown("---")
    st.markdown("### Auto-join FPS & RC on District Columns")

    if fps_df is not None and rc_df is not None:
        col_join1, col_join2 = st.columns(2)
        with col_join1:
            fps_join_col = st.selectbox(
                "FPS district column",
                fps_df.columns.tolist()
            )
        with col_join2:
            rc_join_col = st.selectbox(
                "RC district column",
                rc_df.columns.tolist()
            )

        if st.button("Join FPS & RC"):
            joined_df = join_on_columns(fps_df, rc_df, fps_join_col, rc_join_col)
            st.success(f"Joined dataframe has {len(joined_df)} rows.")
            st.dataframe(joined_df.head(100), use_container_width=True)

            st.markdown("You can build more KPIs on this join (e.g., FPS per 1000 ration cards).")
    else:
        st.info("Need both FPS and RC datasets loaded to perform join.")

# -----------------------------------
# TAB 3: NFSA DATE ABSTRACT
# -----------------------------------
with tabs[2]:
    st.subheader("NFSA Date-wise Abstract")

    if nfsa_date_df is not None:
        st.markdown("Raw table from **NFSA_Date_Abstract.xls** (first 100 rows).")
        st.dataframe(nfsa_date_df.head(100), use_container_width=True)

        st.markdown("#### Quick Chart (you choose Date & Quantity columns)")
        date_col = st.selectbox(
            "Select Date column:",
            nfsa_date_df.columns.tolist()
        )
        value_col = st.selectbox(
            "Select Quantity / Value column:",
            nfsa_date_df.columns.tolist()
        )

        chart_btn = st.button("Plot Date-wise Trend")

        if chart_btn:
            tmp = nfsa_date_df[[date_col, value_col]].copy()
            tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
            tmp[value_col] = safe_numeric(tmp[value_col])
            tmp = tmp.dropna().sort_values(date_col)

            if not tmp.empty:
                st.line_chart(tmp.set_index(date_col)[value_col])
            else:
                st.warning("No valid data to plot after cleaning.")
    else:
        st.warning("NFSA_Date_Abstract.xls not loaded.")

# -----------------------------------
# TAB 4: SALE DISTRIBUTION
# -----------------------------------
with tabs[3]:
    st.subheader("Sale Distribution (from sale_dist.xls)")

    if sale_dist_df is not None:
        st.markdown("Raw view (first 100 rows):")
        st.dataframe(sale_dist_df.head(100), use_container_width=True)

        st.markdown("#### Aggregate & Plot")
        col_options = sale_dist_df.columns.tolist()

        group_col = st.selectbox("Group by column (e.g., District / Scheme / FPS):", col_options, key="sale_group")
        value_col = st.selectbox("Value column (e.g., Sale Qty / Amount):", col_options, key="sale_value")

        plot_btn = st.button("Plot Aggregated Sale Distribution")

        if plot_btn:
            tmp = sale_dist_df[[group_col, value_col]].copy()
            tmp[value_col] = safe_numeric(tmp[value_col])
            agg = (
                tmp.groupby(group_col)[value_col]
                .sum()
                .sort_values(ascending=False)
                .head(20)
            )

            if not agg.empty:
                st.bar_chart(agg)
            else:
                st.warning("No numeric data available to plot.")
    else:
        st.warning("sale_dist.xls not loaded.")

# -----------------------------------
# TAB 5: SCHEME-WISE ALLOTMENT VS SALE
# -----------------------------------
with tabs[4]:
    st.subheader("Scheme-wise Allotment vs Sale (Nov 2025)")

    if scheme_sale_df is not None:
        st.markdown("Raw view (first 100 rows) from **Scheme_Wise_Sale_Allotment_11_2025.xls**:")
        st.dataframe(scheme_sale_df.head(100), use_container_width=True)

        col_options = scheme_sale_df.columns.tolist()

        scheme_col = st.selectbox("Scheme column:", col_options, key="scheme_col")
        allot_col = st.selectbox("Allotment column:", col_options, key="allot_col")
        sale_col = st.selectbox("Sale column:", col_options, key="sale_col")

        plot_scheme_btn = st.button("Plot Scheme-wise Allotment vs Sale")

        if plot_scheme_btn:
            tmp = scheme_sale_df[[scheme_col, allot_col, sale_col]].copy()

            tmp[allot_col] = safe_numeric(tmp[allot_col])
            tmp[sale_col] = safe_numeric(tmp[sale_col])

            agg = (
                tmp.groupby(scheme_col)[[allot_col, sale_col]]
                .sum()
                .sort_values(by=sale_col, ascending=False)
            )

            if not agg.empty:
                st.bar_chart(agg)
            else:
                st.warning("No numeric data available to plot.")
    else:
        st.warning("Scheme_Wise_Sale_Allotment_11_2025.xls not loaded.")

# -----------------------------------
# TAB 6: HEATMAPS & MAP
# -----------------------------------
with tabs[5]:
    st.subheader("Heatmaps & Optional Map View")

    st.markdown("### Table Heatmap (any numeric metric by district/scheme)")

    source_choice = st.selectbox(
        "Choose dataset for heatmap:",
        ["None",
         "FPS CSV",
         "RC CSV",
         "Sale Dist XLS",
         "Scheme-wise Sale/Allot XLS"]
    )

    df_for_heatmap = None
    if source_choice == "FPS CSV" and fps_df is not None:
        df_for_heatmap = fps_df
    elif source_choice == "RC CSV" and rc_df is not None:
        df_for_heatmap = rc_df
    elif source_choice == "Sale Dist XLS" and sale_dist_df is not None:
        df_for_heatmap = sale_dist_df
    elif source_choice == "Scheme-wise Sale/Allot XLS" and scheme_sale_df is not None:
        df_for_heatmap = scheme_sale_df

    if df_for_heatmap is not None:
        st.markdown("Raw (first 50 rows):")
        st.dataframe(df_for_heatmap.head(50), use_container_width=True)

        cols = df_for_heatmap.columns.tolist()
        dim_col = st.selectbox("Dimension column (e.g., District / Scheme):", cols, key="heat_dim")
        val_col = st.selectbox("Numeric column for heat:", cols, key="heat_val")

        heat_btn = st.button("Build Heatmap Table")

        if heat_btn:
            tmp = df_for_heatmap[[dim_col, val_col]].copy()
            tmp[val_col] = safe_numeric(tmp[val_col])
            agg = tmp.groupby(dim_col)[val_col].sum().reset_index()

            # Style as heatmap using dataframe styles
            heat_df = agg.set_index(dim_col)
            styled = heat_df.style.background_gradient()
            st.dataframe(styled, use_container_width=True)
    elif source_choice != "None":
        st.warning("Selected dataset not loaded or empty.")

    st.markdown("---")
    st.markdown("### Map View (optional, if district_lat_long.csv is present)")

    if district_geo_df is not None:
        st.info("Using district_lat_long.csv to plot map. Expecting columns: district, lat, lon")
        st.dataframe(district_geo_df.head(), use_container_width=True)

        if df_for_heatmap is not None:
            # Try to join district_geo_df.district with df_for_heatmap[dim_col]
            try:
                join_df = df_for_heatmap.copy()
                join_df[val_col] = safe_numeric(join_df[val_col])
                agg = join_df.groupby(dim_col)[val_col].sum().reset_index()

                geo_join = agg.merge(
                    district_geo_df,
                    left_on=dim_col,
                    right_on="district",
                    how="inner"
                )

                if not geo_join.empty:
                    st.map(
                        geo_join[["lat", "lon"]],
                    )
                else:
                    st.warning("No matching districts found between data and geo file.")
            except Exception as e:
                st.warning(f"Could not build geo-join for map: {e}")
        else:
            st.info("Select a dataset and build a heatmap first to use map.")
    else:
        st.info("district_lat_long.csv not found. Add it in the folder if you want geo maps.")

# -----------------------------------
# TAB 7: AI INSIGHTS (DEMO)
# -----------------------------------
with tabs[6]:
    st.subheader("AI Insights (Rule-based Demo – No External API)")

    st.markdown("""
    This tab gives **automatic textual insights** based on simple rules:
    - Finds top & bottom districts/schemes by a selected metric.
    - Highlights basic anomalies using z-scores.
    - Summarises patterns in a narrative format.
    """)

    source_choice_ai = st.selectbox(
        "Choose dataset for AI-style summary:",
        ["None",
         "FPS CSV",
         "RC CSV",
         "Sale Dist XLS",
         "Scheme-wise Sale/Allot XLS",
         "NFSA Date Abstract XLS"]
    )

    df_ai = None
    if source_choice_ai == "FPS CSV" and fps_df is not None:
        df_ai = fps_df
    elif source_choice_ai == "RC CSV" and rc_df is not None:
        df_ai = rc_df
    elif source_choice_ai == "Sale Dist XLS" and sale_dist_df is not None:
        df_ai = sale_dist_df
    elif source_choice_ai == "Scheme-wise Sale/Allot XLS" and scheme_sale_df is not None:
        df_ai = scheme_sale_df
    elif source_choice_ai == "NFSA Date Abstract XLS" and nfsa_date_df is not None:
        df_ai = nfsa_date_df

    if df_ai is not None:
        cols = df_ai.columns.tolist()
        dim_col_ai = st.selectbox("Dimension column (District / Scheme / FPS):", cols, key="ai_dim")
        val_col_ai = st.selectbox("Numeric column (Qty / Count / Amount):", cols, key="ai_val")

        if st.button("Generate AI-style Insight"):
            tmp = df_ai[[dim_col_ai, val_col_ai]].copy()
            tmp[val_col_ai] = safe_numeric(tmp[val_col_ai])
            agg = tmp.groupby(dim_col_ai)[val_col_ai].sum().reset_index().dropna()

            if agg.empty:
                st.warning("No numeric data available after cleaning.")
            else:
                # Basic stats & anomaly detection via z-score
                values = agg[val_col_ai]
                mean_val = values.mean()
                median_val = values.median()
                std_val = values.std(ddof=0)

                agg["z_score"] = (agg[val_col_ai] - mean_val) / (std_val if std_val else 1)
                top = agg.sort_values(val_col_ai, ascending=False).head(5)
                bottom = agg.sort_values(val_col_ai, ascending=True).head(5)
                high_anom = agg[agg["z_score"] > 2].sort_values("z_score", ascending=False)
                low_anom = agg[agg["z_score"] < -2].sort_values("z_score", ascending=True)

                st.markdown("#### Quick Numeric Snapshot")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Mean", f"{mean_val:,.2f}")
                with c2:
                    st.metric("Median", f"{median_val:,.2f}")
                with c3:
                    st.metric("Std Dev", f"{std_val:,.2f}")

                st.markdown("#### Top 5 by value")
                st.dataframe(top[[dim_col_ai, val_col_ai]], use_container_width=True)

                st.markdown("#### Bottom 5 by value")
                st.dataframe(bottom[[dim_col_ai, val_col_ai]], use_container_width=True)

                st.markdown("#### Detected Anomalies (z-score > 2 or < -2)")
                if not high_anom.empty or not low_anom.empty:
                    if not high_anom.empty:
                        st.write("**High positive anomalies (unusually high values):**")
                        st.dataframe(high_anom[[dim_col_ai, val_col_ai, "z_score"]], use_container_width=True)
                    if not low_anom.empty:
                        st.write("**High negative anomalies (unusually low values):**")
                        st.dataframe(low_anom[[dim_col_ai, val_col_ai, "z_score"]], use_container_width=True)
                else:
                    st.write("No strong anomalies detected on this metric.")

                # AI-style narrative
                st.markdown("### Narrative Insight (Auto-generated)")
                narrative = []

                narrative.append(
                    f"For the selected metric **{val_col_ai}** across **{dim_col_ai}**, "
                    f"the average value is about **{mean_val:,.0f}**, with a median of **{median_val:,.0f}**."
                )

                if not top.empty:
                    top_names = ", ".join(top[dim_col_ai].astype(str).head(3).tolist())
                    narrative.append(
                        f"The top-performing segments are **{top_names}**, which together account for a "
                        f"significant share of the overall volume."
                    )

                if not bottom.empty:
                    bottom_names = ", ".join(bottom[dim_col_ai].astype(str).head(3).tolist())
                    narrative.append(
                        f"On the lower side, **{bottom_names}** show relatively small values on this metric."
                    )

                if not high_anom.empty:
                    an_name = high_anom.iloc[0][dim_col_ai]
                    an_val = high_anom.iloc[0][val_col_ai]
                    narrative.append(
                        f"One particularly high outlier is **{an_name}** with a value of **{an_val:,.0f}**, "
                        f"which is more than 2 standard deviations above the mean."
                    )

                if not low_anom.empty:
                    an_name = low_anom.iloc[0][dim_col_ai]
                    an_val = low_anom.iloc[0][val_col_ai]
                    narrative.append(
                        f"On the lower extreme, **{an_name}** appears as a potential underperformer "
                        f"with a value of just **{an_val:,.0f}**."
                    )

                narrative.append(
                    "At a policy level, you can treat extremely high values as potential concentration or leakage risks "
                    "and extremely low values as coverage/uptake gaps that require targeted interventions."
                )

                st.write(" ".join(narrative))
    else:
        st.info("Select a dataset above to generate insights.")

# -----------------------------------
# TAB 8: RAW DATA EXPLORER
# -----------------------------------
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
        st.warning("No datasets loaded. Check file names and paths.")
    else:
        choice = st.selectbox("Choose dataset to view:", dataset_options)

        if choice == "FPS CSV":
            st.write("**FPSReportDistrictWiseAsPerLatestRecord.csv**")
            st.dataframe(fps_df, use_container_width=True)
        elif choice == "RC CSV":
            st.write("**RCReportDistrictWise.csv**")
            st.dataframe(rc_df, use_container_width=True)
        elif choice == "Sale Dist XLS":
            st.write("**sale_dist.xls**")
            st.dataframe(sale_dist_df, use_container_width=True)
        elif choice == "NFSA Date Abstract XLS":
            st.write("**NFSA_Date_Abstract.xls**")
            st.dataframe(nfsa_date_df, use_container_width=True)
        elif choice == "Scheme-wise Sale/Allot XLS":
            st.write("**Scheme_Wise_Sale_Allotment_11_2025.xls**")
            st.dataframe(scheme_sale_df, use_container_width=True)
