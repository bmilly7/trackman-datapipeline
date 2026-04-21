import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "club",
    "club_speed",
    "ball_speed",
    "launch_angle",
    "launch_direction",
    "spin_rate",
    "carry_flat_length",
]


OPTIONAL_COLUMNS = [
    "attack_angle",
    "club_path",
    "face_angle",
    "face_to_path",
    "smash_factor",
    "spin_axis",
    "est_total_flat_length",
]


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that the normalized TrackMan DataFrame contains
    all required columns for the pipeline.

    Raises:
        ValueError: if one or more required columns are missing
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(
            "Validation failed. Missing required columns: "
            + ", ".join(missing_columns)
        )

    print("Required column validation passed.")


def report_optional_columns(df: pd.DataFrame) -> None:
    """
    Report which optional columns are missing.
    Optional columns do not fail the pipeline.
    """
    missing_optional = [col for col in OPTIONAL_COLUMNS if col not in df.columns]

    if missing_optional:
        print(
            "Warning: Missing optional columns: "
            + ", ".join(missing_optional)
        )
    else:
        print("All optional columns are present.")