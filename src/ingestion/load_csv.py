from pathlib import Path
import pandas as pd


def load_trackman_csv(file_path: str) -> pd.DataFrame:
    """
    Load a TrackMan CSV export into a pandas DataFrame.

    Handles Excel-style exports that begin with a sep= line.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, got: {path.suffix}")

    encodings_to_try = ["utf-8-sig", "latin1"]

    for encoding in encodings_to_try:
        try:
            with open(path, "r", encoding=encoding, errors="replace") as f:
                first_line = f.readline().strip()

            # Handle Excel-style sep= line
            if "sep=" in first_line.lower():
                df = pd.read_csv(path, sep=",", skiprows=1, encoding=encoding)
            else:
                df = pd.read_csv(path, encoding=encoding)

            if df.empty:
                raise ValueError(f"CSV file is empty: {file_path}")

            print(f"Loaded {len(df)} rows and {len(df.columns)} columns from {file_path}")
            return df

        except Exception as e:
            last_error = e

    raise ValueError(f"Failed to read CSV file '{file_path}': {last_error}")