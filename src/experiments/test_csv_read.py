file_path = "data/raw/session03-19-26(session03-19-26).csv"

with open(file_path, "r", encoding="latin1") as f:
    for _ in range(3):
        print(repr(f.readline()))


from src.ingestion.load_csv import load_trackman_csv
#a basic practice file to read a test csv file of some limited trackman data

#grab the project root 


#build a path to the experimental csv file

file_path = "data/raw/session03-19-26(session03-19-26).csv"

df = load_trackman_csv(file_path)

print(df.head())
print(df.columns.tolist())