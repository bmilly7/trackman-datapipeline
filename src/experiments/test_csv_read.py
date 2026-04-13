'''
file_path = "data/raw/session03-19-26(session03-19-26).csv"

with open(file_path, "r", encoding="latin1") as f:
    for _ in range(3):
        print(repr(f.readline()))

'''
from src.ingestion.load_csv import load_trackman_csv #function loads raw file
from src.cleaning.clean_shots import clean_trackman_data #function that cleans uneeded rows
from src.cleaning.normalize import normalize_column_names #function that standardizes dataframe (column names ect)
import pandas as pd
#a basic practice file to read a test csv file of some limited trackman data

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


#build a path to the experimental csv file

file_path = "data/raw/session03-19-26(session03-19-26).csv"


#call functions from connected files
df = load_trackman_csv(file_path)
clean_df = clean_trackman_data(df)
normalize_df = normalize_column_names(clean_df)




print(normalize_df.head())
print("\nColumns:")
print(normalize_df.columns.tolist())
