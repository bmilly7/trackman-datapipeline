from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_ball_speed_trends(
    session_metrics_df: pd.DataFrame,
    output_dir: str = "data/processed/plots",
) -> None:
    """
    Create and save a ball speed trend line chart for each club.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = session_metrics_df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"], errors="coerce")
    df = df.dropna(subset=["session_date"])
    df = df.sort_values(["club", "session_date"])

    for club, club_df in df.groupby("club"):
        if len(club_df) < 2:
            continue

        plt.figure(figsize=(8, 5))
        plt.plot(
            club_df["session_date"],
            club_df["avg_ball_speed"],
            marker="o",
        )

        plt.title(f"{club} Ball Speed Trend")
        plt.xlabel("Session Date")
        plt.ylabel("Average Ball Speed")
        plt.xticks(rotation=45)
        plt.tight_layout()

        safe_club_name = (
            str(club)
            .lower()
            .replace(" ", "_")
            .replace("°", "deg")
            .replace("/", "_")
        )

        file_path = output_path / f"{safe_club_name}_ball_speed_trend.png"
        plt.savefig(file_path)
        plt.close()

        print(f"Saved plot: {file_path}")