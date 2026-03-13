import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ---------------------------
# FILE PATHS
# ---------------------------
BASE_PATH = os.path.join(os.path.expanduser("~"), "Documents")
CURRENT_CSV = os.path.join(BASE_PATH, "kid_current.csv")
HISTORY_CSV = os.path.join(BASE_PATH, "kid_history.csv")

st.set_page_config(page_title="Kid Popularity Dashboard", layout="wide")

st.title("📊 YouTube Kid Popularity Dashboard")

# ---------------------------
# LOAD CURRENT DATA
# ---------------------------
if os.path.exists(CURRENT_CSV):
    current_df = pd.read_csv(CURRENT_CSV)
else:
    st.error("Current data file not found. Run backend first.")
    st.stop()

# ---------------------------
# LEADERBOARD
# ---------------------------
st.subheader("🏆 Current Leaderboard")

st.dataframe(current_df, use_container_width=True)

top_kid = current_df.iloc[0]

st.success(f"👑 Most Popular Right Now: {top_kid['Kid']} ({top_kid['Consensus %']}%)")

# ---------------------------
# PIE CHART
# ---------------------------
fig_pie = px.pie(
    current_df,
    names="Kid",
    values="Consensus %",
    title="Current Popularity Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------
# HISTORY TREND
# ---------------------------
st.subheader("📈 Popularity Trend Over Time")

if os.path.exists(HISTORY_CSV):
    history_df = pd.read_csv(HISTORY_CSV)

    fig_line = px.line(
        history_df,
        x="Date",
        y="Consensus %",
        color="Kid",
        markers=True,
        title="Trend Over Time"
    )

    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("History file not found yet. Run backend multiple times to build trend data.")

# ---------------------------
# REFRESH BUTTON
# ---------------------------
if st.button("🔄 Refresh Dashboard"):
    st.rerun()