import pandas as pd


HIGHER_IS_BETTER = {
    "avg_ball_speed": "ball_speed",
    "avg_carry": "carry_distance",
    "avg_smash_factor": "smash_factor",
}

LOWER_IS_BETTER = {
    "std_carry": "carry_consistency",
    "std_dispersion": "dispersion_consistency",
}


def classify_trend(
    pct_change: float,
    higher_is_better: bool,
    threshold: float = 2.0,
) -> str:
    """
    Classify a metric trend using percent change.

    Args:
        pct_change: Percent change from first session to last session.
        higher_is_better: Whether an increase is considered good.
        threshold: Minimum percent change needed to classify as meaningful.

    Returns:
        A readable label: improving, declining, stable, or worsening.
    """
    if pd.isna(pct_change):
        return "needs_more_data"

    if abs(pct_change) < threshold:
        return "stable"

    if higher_is_better:
        return "improving" if pct_change > 0 else "declining"

    return "improving" if pct_change < 0 else "worsening"


def generate_insight_labels(trend_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert trend metrics into readable insight labels.

    Returns one row per club with separate labels for each core metric.
    """
    if trend_df.empty:
        return pd.DataFrame()

    insights = []

    for _, row in trend_df.iterrows():
        club_insight = {
            "club": row["club"],
            "session_count": row["session_count"],
            "first_session": row["first_session"],
            "last_session": row["last_session"],
        }

        for metric, label_name in HIGHER_IS_BETTER.items():
            pct_col = f"{metric}_pct_change"

            club_insight[f"{label_name}_label"] = classify_trend(
                row.get(pct_col),
                higher_is_better=True,
            )

        for metric, label_name in LOWER_IS_BETTER.items():
            pct_col = f"{metric}_pct_change"

            club_insight[f"{label_name}_label"] = classify_trend(
                row.get(pct_col),
                higher_is_better=False,
            )

        insights.append(club_insight)

    return pd.DataFrame(insights)