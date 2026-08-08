import os
import pandas as pd

files = os.listdir('data')

print('FILES IN DATA FOLDER:')
print(files)

for file in files:
    if file.endswith('.csv'):
        df = pd.read_csv(f'data/{file}', nrows=3)
        print(f'\\n--- {file} ---')
        print(df.columns.tolist())