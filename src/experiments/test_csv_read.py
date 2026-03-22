import pandas as pd
from pathlib import Path

#a basic practice file to read a test csv file of some limited trackman data

#grab the project root 
BASE_DIR = Path(__file__).resolve().parents[2]

#build a path to the experimental csv file

csv_file_path = BASE_DIR / "data" / "experimental" / "trackman_session_experiment.csv"

df = pd.read_csv(csv_file_path)

print(df.head())