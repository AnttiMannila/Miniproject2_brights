import pandas as pd
import os
import glob

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
    
    venue['Direct solar radiation mean [W/m2]'] = pd.to_numeric(venue['Direct solar radiation mean [W/m2]'], errors='coerce')
    try:
        venue.drop(columns=['Unnamed: 0', 'Time [Local time]'], axis=1, inplace=True)
    except:
        venue.drop(columns=['Unnamed: 0_x', 'Time [Local time]', 'Unnamed: 0_y'], axis=1, inplace=True)
    
    venue['Date'] = pd.to_datetime(venue[['Year', 'Month', 'Day']])
    venue.drop(columns= ['Year', 'Month', 'Day'], inplace=True)
    venue = pd.concat([venue.iloc[:, -1], venue.iloc[:, :-1]], axis=1)
    venue.to_csv(f'{venue_name}.csv', index=False)
    
if __name__ == '__main__':
    list_of_venues = ['Himos','Ilomantsi','Kilpisjärvi','Levi','Pyhä', 'Salpausselkä', 'Sveitsi', 'Tahko', 'Talma', 'Vihti']
    for i in list_of_venues:
        concat_venue_and_radiation(i)
        print("Ready!")