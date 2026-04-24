from pathlib import Path
import pandas as pd


def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Save a DataFrame to a CSV file.
    Creates the parent directory if it does not exist.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    print(f"Saved file: {output_path}")


def save_pipeline_outputs(
    processed_shots_df: pd.DataFrame,
    session_metrics_df: pd.DataFrame,
    trend_analysis_df: pd.DataFrame,
    insight_labels_df: pd.DataFrame,
    output_dir: str = "data/processed",
) -> None:
    """
    Save main pipeline outputs to the processed data folder.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    save_dataframe(
        processed_shots_df,
        str(output_path / "processed_shots.csv"),
    )

    save_dataframe(
        session_metrics_df,
        str(output_path / "session_metrics.csv"),
    )

    save_dataframe(
        trend_analysis_df,
        str(output_path / "trend_analysis.csv"),
    )

    save_dataframe(
        insight_labels_df,
        str(output_path / "insight_labels.csv"),
    )