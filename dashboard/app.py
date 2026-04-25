from pathlib import Path
import pandas as pd
import streamlit as st


PROCESSED_DIR = Path("data/processed")

SESSION_METRICS_PATH = PROCESSED_DIR / "session_metrics.csv"
TREND_ANALYSIS_PATH = PROCESSED_DIR / "trend_analysis.csv"
INSIGHT_LABELS_PATH = PROCESSED_DIR / "insight_labels.csv"


st.set_page_config(
    page_title="TrackMan Performance Dashboard",
    layout="wide",
)


@st.cache_data
def load_data():
    session_metrics = pd.read_csv(SESSION_METRICS_PATH)
    trend_analysis = pd.read_csv(TREND_ANALYSIS_PATH)
    insight_labels = pd.read_csv(INSIGHT_LABELS_PATH)

    session_metrics["session_date"] = pd.to_datetime(
        session_metrics["session_date"],
        errors="coerce",
    )

    return session_metrics, trend_analysis, insight_labels


st.title("TrackMan Performance Data Pipeline Dashboard")

st.write(
    "This dashboard displays performance trends generated from processed TrackMan session data."
)

if not SESSION_METRICS_PATH.exists():
    st.error("No processed data found. Run the pipeline first.")
    st.stop()

session_metrics, trend_analysis, insight_labels = load_data()

clubs = sorted(session_metrics["club"].dropna().unique())

selected_club = st.selectbox("Select Club", clubs)

club_metrics = session_metrics[session_metrics["club"] == selected_club].copy()
club_metrics = club_metrics.sort_values("session_date")

club_insights = insight_labels[insight_labels["club"] == selected_club]

st.subheader(f"{selected_club} Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Sessions", len(club_metrics))
col2.metric("Total Valid Shots", int(club_metrics["shot_count"].sum()))
col3.metric(
    "Avg Ball Speed",
    round(club_metrics["avg_ball_speed"].mean(), 2),
)

st.subheader("Insight Labels")

if club_insights.empty:
    st.info("Not enough sessions yet to generate trend insights for this club.")
else:
    st.dataframe(club_insights, use_container_width=True)

st.subheader("Ball Speed Trend")
st.line_chart(
    club_metrics.set_index("session_date")["avg_ball_speed"]
)

st.subheader("Carry Distance Trend")
st.line_chart(
    club_metrics.set_index("session_date")["avg_carry"]
)

st.subheader("Dispersion Consistency Trend")
st.line_chart(
    club_metrics.set_index("session_date")["std_dispersion"]
)

st.subheader("Session Metrics Table")
st.dataframe(club_metrics, use_container_width=True)

st.subheader("All Trend Analysis")
st.dataframe(trend_analysis, use_container_width=True)