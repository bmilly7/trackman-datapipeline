import pandas as pd
import numpy as np


TREND_METRICS = [
    "avg_ball_speed",
    "avg_carry",
    "avg_smash_factor",
    "std_carry",
    "std_dispersion",
]


def compute_trend_analysis(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-club longitudinal trend insights.

    For each club and metric, this calculates:
    - first value
    - last value
    - total change
    - percent change
    - trend slope across sessions
    """

    df = metrics_df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"], errors="coerce")
    df = df.dropna(subset=["session_date"])
    df = df.sort_values(["club", "session_date"])

    trend_results = []

    for club, club_df in df.groupby("club"):
        club_df = club_df.sort_values("session_date").reset_index(drop=True)

        # Need at least 2 sessions to calculate meaningful change
        if len(club_df) < 2:
            continue

        x = np.arange(len(club_df))

        result = {
            "club": club,
            "session_count": len(club_df),
            "first_session": club_df["session_date"].min().date(),
            "last_session": club_df["session_date"].max().date(),
        }

        for metric in TREND_METRICS:
            if metric not in club_df.columns:
                continue

            y = pd.to_numeric(club_df[metric], errors="coerce")

            if y.notna().sum() < 2:
                continue

            first_value = y.dropna().iloc[0]
            last_value = y.dropna().iloc[-1]
            total_change = last_value - first_value

            if first_value != 0:
                percent_change = (total_change / first_value) * 100
            else:
                percent_change = np.nan

            slope = np.polyfit(x[y.notna()], y[y.notna()], 1)[0]

            result[f"{metric}_first"] = first_value
            result[f"{metric}_last"] = last_value
            result[f"{metric}_change"] = total_change
            result[f"{metric}_pct_change"] = percent_change
            result[f"{metric}_slope_per_session"] = slope

        trend_results.append(result)

    return pd.DataFrame(trend_results)