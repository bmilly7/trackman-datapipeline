import pandas as pd


CORE_REQUIRED_COLUMNS = [
    "date",
    "club",
    "club_speed",
    "ball_speed",
    "smash_factor",
    "launch_angle",
    "launch_direction",
    "spin_rate",
    "carry_flat_length",
    "carry_flat_side",
    "use_in_stat",
]


OUTLIER_COLUMNS = [
    "ball_speed",
    "smash_factor",
    "spin_rate",
    "carry_flat_length",
]


def _safe_numeric(series: pd.Series) -> pd.Series:
    """Convert a series to numeric, coercing invalid values to NaN."""
    return pd.to_numeric(series, errors="coerce")


def _mad(series: pd.Series) -> float:
    """
    Compute Median Absolute Deviation (MAD).
    Returns 0 if the series is empty or has no spread.
    """
    clean = series.dropna()
    if clean.empty:
        return 0.0

    median = clean.median()
    deviations = (clean - median).abs()
    mad = deviations.median()

    if pd.isna(mad):
        return 0.0

    return float(mad)


def initialize_filter_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add default filtering/audit fields to the dataset.
    """
    df = df.copy()
    df["included_in_analysis"] = True
    df["exclusion_reason"] = ""
    return df


def apply_rule_based_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply rule-based filtering flags.

    Rules:
    - required core fields must be present
    - use_in_stat must be True
    - basic impossible-value checks
    - very low smash factor shots are flagged
    """
    df = df.copy()

    # Convert key numeric fields
    numeric_cols = [
        "club_speed",
        "ball_speed",
        "smash_factor",
        "launch_angle",
        "launch_direction",
        "spin_rate",
        "carry_flat_length",
        "carry_flat_side",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = _safe_numeric(df[col])

    for idx, row in df.iterrows():
        reasons = []

        # Missing required fields
        for col in CORE_REQUIRED_COLUMNS:
            if col not in df.columns:
                reasons.append(f"missing_column:{col}")
                continue

            value = row[col]
            if pd.isna(value):
                reasons.append(f"missing_value:{col}")

        # use_in_stat flag
        if "use_in_stat" in df.columns:
            if row["use_in_stat"] is not True:
                reasons.append("trackman_use_in_stat_false")

        # Impossible / suspicious values
        if "club_speed" in df.columns and pd.notna(row["club_speed"]):
            if row["club_speed"] <= 0:
                reasons.append("invalid_club_speed")

        if "ball_speed" in df.columns and pd.notna(row["ball_speed"]):
            if row["ball_speed"] <= 0:
                reasons.append("invalid_ball_speed")

        if "spin_rate" in df.columns and pd.notna(row["spin_rate"]):
            if row["spin_rate"] <= 0:
                reasons.append("invalid_spin_rate")

        if "carry_flat_length" in df.columns and pd.notna(row["carry_flat_length"]):
            if row["carry_flat_length"] <= 0:
                reasons.append("invalid_carry_distance")

        # Low smash factor rule
        if "smash_factor" in df.columns and pd.notna(row["smash_factor"]):
            if row["smash_factor"] < 0.9:
                reasons.append("low_smash_factor")

        if reasons:
            df.at[idx, "included_in_analysis"] = False
            df.at[idx, "exclusion_reason"] = "; ".join(reasons)

    return df


def apply_mad_outlier_flags(df: pd.DataFrame, threshold: float = 3.5) -> pd.DataFrame:
    """
    Apply per-club MAD-based outlier detection.

    For each club and each selected metric:
    - compute club-specific median
    - compute club-specific MAD
    - flag values whose modified z-like distance exceeds threshold

    Notes:
    - Only rows not already excluded are evaluated for outliers
    - If MAD is 0, outlier detection is skipped for that metric/club
    """
    df = df.copy()

    if "club" not in df.columns:
        return df

    for col in OUTLIER_COLUMNS:
        if col not in df.columns:
            continue

        df[col] = _safe_numeric(df[col])

    clubs = df["club"].dropna().unique()

    for club in clubs:
        club_mask = (df["club"] == club) & (df["included_in_analysis"] == True)
        club_df = df.loc[club_mask].copy()

        if club_df.empty:
            continue

        for metric in OUTLIER_COLUMNS:
            if metric not in club_df.columns:
                continue

            series = club_df[metric].dropna()
            if len(series) < 5:
                continue

            median = series.median()
            mad = _mad(series)

            if mad == 0:
                continue

            for idx in club_df.index:
                value = df.at[idx, metric]

                if pd.isna(value):
                    continue

                deviation_score = abs(value - median) / mad

                if deviation_score > threshold:
                    existing_reason = df.at[idx, "exclusion_reason"]

                    new_reason = f"mad_outlier:{metric}"
                    if existing_reason:
                        updated_reason = f"{existing_reason}; {new_reason}"
                    else:
                        updated_reason = new_reason

                    df.at[idx, "included_in_analysis"] = False
                    df.at[idx, "exclusion_reason"] = updated_reason

    return df


def filter_trackman_shots(df: pd.DataFrame, mad_threshold: float = 3.5) -> pd.DataFrame:
    """
    Full filtering pipeline for TrackMan shot data.

    Returns the original dataset plus:
    - included_in_analysis
    - exclusion_reason
    """
    df = initialize_filter_flags(df)
    df = apply_rule_based_flags(df)
    df = apply_mad_outlier_flags(df, threshold=mad_threshold)
    return df