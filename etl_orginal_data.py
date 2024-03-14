import pandas as pd
import os
import glob

def radiation_to_one_file():
    '''This function will concat solar radiation files together'''
    
    #Create path to the working folder
    path = os.getcwd()
    solar_path = f"{path}\\solar_data"
    csv_files = glob.glob(os.path.join(solar_path, "*.csv"))


    # going through files
    dfs =[]

    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    # concat files and drop unneccary columns and change datatypes
    solar_radiation_df = pd.concat(dfs, ignore_index=True)
    solar_radiation_df['Direct solar radiation mean [W/m2]'] = pd.to_numeric(solar_radiation_df['Direct solar radiation mean [W/m2]'], errors='coerce')
    solar_radiation_df.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
    just_radiation_df = solar_radiation_df.drop(columns=['Observation station', 'Time [Local time]'])
    
    #make CSV files
    solar_radiation_df.to_csv('direct_solar_radiation_2004_2024.csv')
    just_radiation_df.to_csv('direct_solar_radiation_2004_2024_values.csv')


def concat_venue_and_radiation(venue_name):

    '''this function will concat all the files on wanted venue'''

    #creating path to the working folder
    path = os.getcwd() 
    cloud_path = f"{path}\\data\\{venue_name}\\cloud_coverage"
    venue_files = glob.glob(os.path.join(cloud_path, "*.csv"))
    radiation = pd.read_csv('direct_solar_radiation_2004_2024_values.csv')
    
    #going through files and dropping not needed columns, and changing cloud cover datatype
    dfs = []
    for file in venue_files:
        df = pd.read_csv(file)
        df.drop(columns=['Observation station'], inplace=True)
        try:
            df['Cloud cover [1/8]'] = df['Cloud cover [1/8]'].str.extract(r'(\d+)').astype(float)
        except:
            df['Cloud cover [1/8]'] = df['Cloud cover[1/8]'].str.extract(r'(\d+)').astype(float)
        dfs.append(df)
    
    venue_df = pd.concat(dfs, ignore_index=True)
    venue_df.drop('Time [Local time]', axis=1, inplace=True)
    venue_df.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
    
    venue_path = f"{path}\\data\\{venue_name}"
    selected_venue = glob.glob(os.path.join(venue_path, "*.csv"))
    venue = pd.read_csv(selected_venue[0])

    # Datatype changes
    # Snow depth
   
    venue['Snow depth [cm]'] = venue['Snow depth [cm]'].str.replace(',', '.').replace('-1', '0')
    venue['Snow depth [cm]'] = pd.to_numeric(venue['Snow depth [cm]'], errors='coerce')

    #average temperature
    try:
        venue['Average temperature [°C]'] = pd.to_numeric(venue['Average temperature [°C]'], errors='coerce')
    except:
        pass

    venue.sort_values(by=['Year', 'Month', 'Day'], inplace=True)
    venue = pd.merge(pd.merge(venue, venue_df, on=['Year', 'Month', 'Day']), radiation, on=['Year', 'Month', 'Day'])
    try:
        venue.drop(columns=['Unnamed: 0', 'Time [Local time]'], axis=1, inplace=True)
    except:
        venue.drop(columns=['Unnamed: 0_x', 'Time [Local time]', 'Unnamed: 0_y'], axis=1, inplace=True)
    venue.to_csv(f'{venue_name}.csv')
    
    
if __name__ == '__main__':
    
    list_of_venues = ['Himos','Ilomantsi','Kilpisjärvi','Levi','Pyhä', 'Ruka', 'Salpausselkä', 'Sveitsi', 'Tahko', 'Vihti']
    radiation_to_one_file()
    for i in list_of_venues:
        concat_venue_and_radiation(i)