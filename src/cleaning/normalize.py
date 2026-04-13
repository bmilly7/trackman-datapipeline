import pandas as pd
import re


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize TrackMan column names into a clean, consistent format.

    Rules:
    - lowercase
    - replace non-alphanumeric characters with underscores
    - collapse multiple underscores into one
    - remove leading/trailing underscores

    Examples:
        'Club Speed' -> 'club_speed'
        'Spin Axis (Sim)' -> 'spin_axis_sim'
        'Carry Flat - Length' -> 'carry_flat_length'
        'Curve.1' -> 'curve_1'
        'Max Height - Dist.' -> 'max_height_dist'
    """

    df = df.copy()

    cleaned_columns = []

    for col in df.columns:
        # Convert to lowercase and strip whitespace
        col = col.strip().lower()

        # Replace any non-alphanumeric character with underscore
        col = re.sub(r'[^a-z0-9]+', '_', col)

        # Collapse multiple underscores into one
        col = re.sub(r'_+', '_', col)

        # Remove leading/trailing underscores
        col = col.strip('_')

        cleaned_columns.append(col)

    df.columns = cleaned_columns

    return df