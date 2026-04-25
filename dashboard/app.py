from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px


PROCESSED_DIR = Path("data/processed")

PROCESSED_SHOTS_PATH = PROCESSED_DIR / "processed_shots.csv"
SESSION_METRICS_PATH = PROCESSED_DIR / "session_metrics.csv"
TREND_ANALYSIS_PATH = PROCESSED_DIR / "trend_analysis.csv"
INSIGHT_LABELS_PATH = PROCESSED_DIR / "insight_labels.csv"


st.set_page_config(
    page_title="TrackMan Performance Dashboard",
    layout="wide",
)


@st.cache_data
def load_data():
    processed_shots = pd.read_csv(PROCESSED_SHOTS_PATH)
    session_metrics = pd.read_csv(SESSION_METRICS_PATH)
    trend_analysis = pd.read_csv(TREND_ANALYSIS_PATH)
    insight_labels = pd.read_csv(INSIGHT_LABELS_PATH)

    processed_shots["date"] = pd.to_datetime(processed_shots["date"], errors="coerce")
    processed_shots["session_date"] = processed_shots["date"].dt.date

    session_metrics["session_date"] = pd.to_datetime(
        session_metrics["session_date"],
        errors="coerce",
    )

    return processed_shots, session_metrics, trend_analysis, insight_labels


st.title("TrackMan Performance Data Pipeline Dashboard")

st.write(
    "This dashboard displays performance trends generated from processed TrackMan session data."
)

if not SESSION_METRICS_PATH.exists() or not PROCESSED_SHOTS_PATH.exists():
    st.error("No processed data found. Run the pipeline first.")
    st.stop()

processed_shots, session_metrics, trend_analysis, insight_labels = load_data()

clubs = sorted(session_metrics["club"].dropna().unique())

selected_club = st.selectbox("Select Club", clubs)

club_metrics = session_metrics[session_metrics["club"] == selected_club].copy()
club_metrics = club_metrics.sort_values("session_date")

club_shots = processed_shots[
    (processed_shots["club"] == selected_club)
    & (processed_shots["included_in_analysis"] == True)
].copy()

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

ball_speed_fig = px.line(
    club_metrics,
    x="session_date",
    y="avg_ball_speed",
    markers=True,
    title=f"{selected_club} Ball Speed Over Time",
)

st.plotly_chart(ball_speed_fig, use_container_width=True)

st.subheader("Carry Distance Trend")

carry_fig = px.line(
    club_metrics,
    x="session_date",
    y="avg_carry",
    markers=True,
    title=f"{selected_club} Carry Distance Over Time",
)

st.plotly_chart(carry_fig, use_container_width=True)

st.subheader("Dispersion Consistency Trend")

dispersion_fig = px.line(
    club_metrics,
    x="session_date",
    y="std_dispersion",
    markers=True,
    title=f"{selected_club} Dispersion Consistency Over Time",
)

st.plotly_chart(dispersion_fig, use_container_width=True)

st.subheader("Shot Dispersion Scatter Plot")

available_dates = sorted(club_shots["session_date"].dropna().unique())

if not available_dates:
    st.info("No valid shot data available for this club.")
else:
    selected_session = st.selectbox("Select Session Date", available_dates)

    scatter_df = club_shots[
        club_shots["session_date"] == selected_session
    ][["carry_flat_side", "carry_flat_length"]].copy()

    scatter_fig = px.scatter(
        scatter_df,
        x="carry_flat_side",
        y="carry_flat_length",
        title=f"{selected_club} Shot Dispersion - {selected_session}",
        labels={
            "carry_flat_side": "Left / Right Dispersion",
            "carry_flat_length": "Carry Distance",
        },
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

    st.caption(
        "Each point represents one valid shot. Left/right dispersion is shown on the x-axis, and carry distance is shown on the y-axis."
    )

st.subheader("Session Metrics Table")
st.dataframe(club_metrics, use_container_width=True)

st.subheader("All Trend Analysis")
st.dataframe(trend_analysis, use_container_width=True)