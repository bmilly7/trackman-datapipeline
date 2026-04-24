import pandas as pd

from src.ingestion.load_all_csvs import load_all_trackman_csvs
from src.analytics.compute_metrics import compute_session_metrics
from src.analytics.trend_analysis import compute_trend_analysis
from src.storage.save_outputs import save_pipeline_outputs

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

processed_shots_df = load_all_trackman_csvs("data/raw")

metrics_df = compute_session_metrics(processed_shots_df)
trend_df = compute_trend_analysis(metrics_df)

save_pipeline_outputs(
    processed_shots_df=processed_shots_df,
    session_metrics_df=metrics_df,
    trend_analysis_df=trend_df,
    output_dir="data/processed",
)

print("\nProcessed Shots Preview:")
print(
    processed_shots_df[
        [
            "date",
            "club",
            "ball_speed",
            "smash_factor",
            "spin_rate",
            "carry_flat_length",
            "included_in_analysis",
            "exclusion_reason",
            "source_file",
        ]
    ].head(10)
)

print("\nSession Metrics Preview:")
print(metrics_df.head(10))

print("\nTrend Analysis Preview:")
print(trend_df.head(10))