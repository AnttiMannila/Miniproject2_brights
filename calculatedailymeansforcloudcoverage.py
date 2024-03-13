import pandas as pd

def calculate_median_cloud_cover(input_file, output_file):
    df = pd.read_csv(input_file)
    df['Cloud cover [1/8]'] = df['Cloud cover [1/8]'].str.extract(r'\((\d+)/\d+\)').astype(float)
    median_cloud_cover = df.groupby(['Year', 'Month', 'Day'])['Cloud cover [1/8]'].median().reset_index()
    median_cloud_cover['Cloud cover [1/8]'] = median_cloud_cover['Cloud cover [1/8]'].round().astype(int)
    cloud_cover_mapping = {
        0: 'Clear (0/8)',
        1: 'Clear (1/8)',
        2: 'Mostly clear (2/8)',
        3: 'Mostly clear (3/8)',
        4: 'Partly cloudy (4/8)',
        5: 'Partly cloudy (5/8)',
        6: 'Mostly cloudy (6/8)',
        7: 'Mostly cloudy (7/8)',
        8: 'Cloudy (8/8)',
        9: 'Cloudiness cannot be determined (9/8)'
    }
    median_cloud_cover['Cloud cover [1/8]'] = median_cloud_cover['Cloud cover [1/8]'].map(cloud_cover_mapping)
    df = df.merge(median_cloud_cover[['Year', 'Month', 'Day', 'Cloud cover [1/8]']], on=['Year', 'Month', 'Day'])
    df.rename(columns={'Cloud cover [1/8]_x': 'Cloud cover [1/8]'}, inplace=True)
    df.drop_duplicates(subset=['Year', 'Month', 'Day'], inplace=True)
    df.drop(columns=['Cloud cover [1/8]'], inplace=True)
    df.rename(columns={'Cloud cover [1/8]_y': 'Cloud cover [1/8]'}, inplace=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "C:\\yourfilehere.csv" #Input file to do the daily mean calculation for
    output_file = "C:\\yournewfilehere.csv" #Output file with daily means
    calculate_median_cloud_cover(input_file, output_file)