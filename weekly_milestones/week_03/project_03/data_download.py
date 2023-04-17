import pandas as pd
import zipfile


dataframes = []
for i in range(1, 101):
    filename = f'file{i}.zip'
    with zipfile.ZipFile(filename) as myzip:
        with myzip.open('data.csv') as myfile:
            df = pd.read_csv(myfile)
            dataframes.append(df)
final_df = pd.concat(dataframes, ignore_index=True)