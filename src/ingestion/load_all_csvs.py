from pathlib import Path
import pandas as pd

from src.ingestion.load_csv import load_trackman_csv
from src.cleaning.clean_shots import clean_trackman_data
from src.cleaning.normalize import normalize_column_names
from src.validation.validate_schema import validate_required_columns, report_optional_columns
from src.filtering.filter_shots import filter_trackman_shots


def load_all_trackman_csvs(raw_data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Load and process all TrackMan CSV files from the raw data directory.

    Pipeline steps per file:
    - load CSV
    - clean rows
    - normalize column names
    - validate schema
    - apply filtering flags

    Returns:
        A combined DataFrame containing all processed shots.
    """
    raw_path = Path(raw_data_dir)

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_data_dir}")

    csv_files = sorted(raw_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {raw_data_dir}")

    processed_frames = []

    for csv_file in csv_files:
        print(f"\nProcessing file: {csv_file}")

        df = load_trackman_csv(str(csv_file))
        clean_df = clean_trackman_data(df)
        normalized_df = normalize_column_names(clean_df)

        validate_required_columns(normalized_df)
        report_optional_columns(normalized_df)

        filtered_df = filter_trackman_shots(normalized_df)

        # Keep track of source file for traceability
        filtered_df["source_file"] = csv_file.name

        processed_frames.append(filtered_df)

    combined_df = pd.concat(processed_frames, ignore_index=True)

    print(f"\nProcessed {len(csv_files)} file(s).")
    print(f"Combined dataset contains {len(combined_df)} rows.")

    return combined_df