import pandas as pd

from src.ingestion.load_all_csvs import load_all_trackman_csvs
from src.analytics.compute_metrics import compute_session_metrics
from src.analytics.trend_analysis import compute_trend_analysis
from src.storage.save_outputs import save_pipeline_outputs


def run_pipeline(
    raw_data_dir: str = "data/raw",
    output_dir: str = "data/processed",
) -> None:
    """
    Run the full TrackMan performance data pipeline.

    Steps:
    - load all raw CSV files
    - clean, normalize, validate, and filter shots
    - compute session-level metrics
    - compute trend analysis
    - save outputs to processed folder
    """

    print("Starting TrackMan data pipeline...")

    processed_shots_df = load_all_trackman_csvs(raw_data_dir)

    metrics_df = compute_session_metrics(processed_shots_df)

    trend_df = compute_trend_analysis(metrics_df)

    save_pipeline_outputs(
        processed_shots_df=processed_shots_df,
        session_metrics_df=metrics_df,
        trend_analysis_df=trend_df,
        output_dir=output_dir,
    )

    print("\nPipeline completed successfully.")
    print(f"Processed shots: {len(processed_shots_df)}")
    print(f"Session metrics rows: {len(metrics_df)}")
    print(f"Trend analysis rows: {len(trend_df)}")


if __name__ == "__main__":
    run_pipeline()