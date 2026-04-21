import pandas as pd

from src.ingestion.load_csv import load_trackman_csv
from src.cleaning.clean_shots import clean_trackman_data
from src.cleaning.normalize import normalize_column_names
from src.validation.validate_schema import (
    validate_required_columns,
    report_optional_columns,
)
from src.filtering.filter_shots import filter_trackman_shots
from src.analytics.compute_metrics import compute_session_metrics

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

file_path = "data/raw/session03-19-26(session03-19-26).csv"

df = load_trackman_csv(file_path)
clean_df = clean_trackman_data(df)
normalized_df = normalize_column_names(clean_df)

validate_required_columns(normalized_df)
report_optional_columns(normalized_df)

filtered_df = filter_trackman_shots(normalized_df)
metrics_df = compute_session_metrics(filtered_df)

print("\nFiltered Data Preview:")
print(
    filtered_df[
        [
            "date",
            "club",
            "ball_speed",
            "smash_factor",
            "spin_rate",
            "carry_flat_length",
            "use_in_stat",
            "included_in_analysis",
            "exclusion_reason",
        ]
    ].head(10)
)

print("\nIncluded in analysis counts:")
print(filtered_df["included_in_analysis"].value_counts(dropna=False))

print("\nSession Metrics Preview:")
print(metrics_df.head(10))

print("\nMetrics Columns:")
print(metrics_df.columns.tolist())