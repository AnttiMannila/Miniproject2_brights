import pandas as pd
import os

def preprocess_solar_radiation_data(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df.drop(columns=['Observation station','Year', 'Month', 'Day', 'Time [Local time]'], inplace=True)
    return df

def preprocess_temperature_and_snow_depth_data(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df.drop(columns=['Observation station', 'Year', 'Month', 'Day', 'Time [Local time]'], inplace=True)
    return df

def preprocess_cloud_coverage_data(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df['Cloud cover [1/8]'] = df['Cloud cover [1/8]'].str.extract(r'(\d+)').astype(float)
    df.drop(columns=['Observation station', 'Year', 'Month', 'Day', 'Time [Local time]'], inplace=True)
    return df

def join_dataframes(solar_df, temp_snow_df, cloud_coverage_df, venue):
    merged_df = pd.merge(solar_df, temp_snow_df, on='Date', how='inner')
    merged_df = pd.merge(merged_df, cloud_coverage_df, on='Date', how='inner')
    merged_df['Venue'] = f"{venue}"
    merged_df = merged_df[['Date', 'Venue', 'Average temperature [°C]', 'Snow depth [cm]', 'Cloud cover [1/8]', 'Direct solar radiation mean [W/m2]']]
    return merged_df

def count_nulls():
    finished_csvs = os.listdir(os.path.join(os.getcwd(), "Finished_CSVs"))
    for i in finished_csvs:
        file = os.path.join(os.getcwd(), "Finished_CSVs", i)
        df = pd.read_csv(file)
        print()
        print(file)
        print(df.isnull().sum())
        print(len(df))

def check_value_types():
    finished_csvs = os.listdir(os.path.join(os.getcwd(), "Finished_CSVs"))
    for i in finished_csvs:
        file = os.path.join(os.getcwd(), "Finished_CSVs", i)
        df = pd.read_csv(file)
        print()
        print(file)
        print(df.dtypes)

def fix_value_types():
    finished_csvs = os.listdir(os.path.join(os.getcwd(), "Working"))
    for file in finished_csvs:
        i = os.path.join(os.getcwd(), "Working", file)
        df = pd.read_csv(i)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        df = df.sort_values('Date')
        df['Average temperature [°C]'] = pd.to_numeric(df['Average temperature [°C]'], errors='coerce')
        df['Snow depth [cm]'] = pd.to_numeric(df['Snow depth [cm]'], errors='coerce') 
        df['Cloud cover [1/8]'] = pd.to_numeric(df['Cloud cover [1/8]'], errors='coerce') 
        df['Direct solar radiation mean [W/m2]'] = pd.to_numeric(df['Direct solar radiation mean [W/m2]'], errors='coerce') 
        df.to_csv(os.path.join(os.getcwd(), "Finished_CSVs", f"finished{file}"), index=False)

# print(os.getcwd())

# Check for length of the concatenated solar radiation file (fixed now, unnecessary probably)

# df = pd.read_csv("C:\\Miniproject2\\CSVs\\concatenated_solar_radiation.csv")
# df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
# df.drop(columns=['Year', 'Month', 'Day'], inplace=True)
# print(len(df['Date']))
