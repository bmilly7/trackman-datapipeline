import pandas as pd


def compute_session_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-session, per-club performance metrics.

    Uses only shots marked as included_in_analysis == True.

    Returns:
        DataFrame with aggregated metrics per (date, club)
    """

    # Only use valid shots
    df = df[df["included_in_analysis"] == True].copy()

    # Convert date to datetime (if not already)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows where date is invalid
    df = df.dropna(subset=["date"])

    # Extract session date (remove time component)
    df["session_date"] = df["date"].dt.date

    # Group by session_date and club
    grouped = df.groupby(["session_date", "club"])

    # Compute metrics
    metrics_df = grouped.agg(
        shot_count=("club", "count"),

        avg_club_speed=("club_speed", "mean"),
        avg_ball_speed=("ball_speed", "mean"),
        avg_smash_factor=("smash_factor", "mean"),

        avg_launch_angle=("launch_angle", "mean"),
        avg_launch_direction=("launch_direction", "mean"),

        avg_spin_rate=("spin_rate", "mean"),

        avg_carry=("carry_flat_length", "mean"),
        std_carry=("carry_flat_length", "std"),

        avg_dispersion=("carry_flat_side", "mean"),
        std_dispersion=("carry_flat_side", "std"),
    ).reset_index()

    return metrics_df