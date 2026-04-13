import pandas as pd


def clean_trackman_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning on raw TrackMan shot data.

    Steps:
    - remove fully empty rows
    - remove non-shot rows missing a Date value
    - reset index
    """

    df = df.dropna(how="all").copy()

    if "Date" in df.columns:
        df = df[df["Date"].notna()].copy()

    df = df.reset_index(drop=True)

    return df