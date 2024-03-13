import pandas as pd
import os
import glob

def radiation_to_one_file():
    path = os.getcwd()
    solar_path = f"{path}\\solar_data"
    csv_files = glob.glob(os.path.join(solar_path, "*.csv"))

    dfs =[]

    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    solar_radiation_df = pd.concat(dfs, ignore_index=True)
    solar_radiation_df.sort_values(by=['Year', 'Month', 'Day'], inplace=True)

    just_radiation_df = solar_radiation_df.drop(columns=['Observation station', 'Time [Local time]'])

    solar_radiation_df.to_csv('direct_solar_radiation_2004_2024.csv')
    just_radiation_df.to_csv('direct_solar_radiation_2004_2024_values.csv')


def concat_venue_and_radiation(venue_name):
    path = os.getcwd() # "C:\\project2\\Miniproject2_brights\\venue"
    cloud_path = f"{path}\\data\\{venue_name}\\cloud_coverage"
    venue_files = glob.glob(os.path.join(cloud_path, "*.csv"))
    radiation = pd.read_csv('direct_solar_radiation_2004_2024_values.csv')
    

    dfs = []
    for file in venue_files:
        df = pd.read_csv(file)
        df.drop(columns=['Observation station'], inplace=True)
        df['Cloud cover [1/8]'] = df['Cloud cover [1/8]'].str.extract(r'(\d+)').astype(float)
        dfs.append(df)
    venue_df = pd.concat(dfs, ignore_index=True)
    venue_df.drop('Time [Local time]', axis=1, inplace=True)
    venue_df.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
    
    venue_path = f"{path}\\data\\{venue_name}"
    selected_venue = glob.glob(os.path.join(venue_path, "*.csv"))
    venue = pd.read_csv(selected_venue[0])

    venue.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
    venue = pd.merge(pd.merge(venue, venue_df, on=['Year', 'Month', 'Day']), radiation, on=['Year', 'Month', 'Day'])
    venue.drop(columns=['Unnamed: 0', 'Time [Local time]'], axis=1, inplace=True)
    venue.to_csv(f'{venue_name}.csv')
    
    
if __name__ == '__main__':
    radiation_to_one_file()
    concat_venue_and_radiation('Vihti')