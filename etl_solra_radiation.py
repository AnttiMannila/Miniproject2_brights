import pandas as pd
import os
import glob

path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))

dfs =[]

for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

solar_radiation_df = pd.concat(dfs, ignore_index=True)
solar_radiation_df.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
just_radiation_df = solar_radiation_df.drop(columns=['Observation station', 'Time [Local time]', 'Direct solar radiation [W/m2]'])
solar_radiation_df.to_csv('direct_solar_radiation_2004_2024.csv')
just_radiation_df.to_csv('direct_solar_radiation_2004_2024_values.csv')
print(solar_radiation_df)
print(just_radiation_df)