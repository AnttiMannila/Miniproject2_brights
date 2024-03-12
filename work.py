import pandas as pd

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

def join_dataframes(solar_df, temp_snow_df, cloud_coverage_df):
    merged_df = pd.merge(solar_df, temp_snow_df, on='Date', how='inner')
    merged_df = pd.merge(merged_df, cloud_coverage_df, on='Date', how='inner')
    merged_df = merged_df[['Date', 'Average temperature [°C]', 'Snow depth [cm]', 'Cloud cover [1/8]', 'Direct solar radiation mean [W/m2]']]
    return merged_df

# print(os.getcwd())

# Check for null value amounts per final csv

# venues = []
# folders = os.listdir(os.path.join(os.getcwd(), "CSVs"))
# for folder in folders:
#     folder_path = os.path.join(os.getcwd(), "CSVs", folder)
#     if os.path.isdir(folder_path):
#         venues.append(folder)
# for i in venues:
#     df = pd.read_csv(os.getcwd() + f"\\CSVs\\{i}" + '\\combined_data.csv')
#     print()
#     print(i)
#     print(df.isnull().sum())

# Check for length of the concatenated solar radiation file (fixed now, unnecessary probably)

# df = pd.read_csv("C:\\Miniproject2\\CSVs\\concatenated_solar_radiation.csv")
# df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
# df.drop(columns=['Year', 'Month', 'Day'], inplace=True)
# print(len(df['Date']))