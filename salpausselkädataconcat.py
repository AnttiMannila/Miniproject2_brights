import pandas as pd
import os

# Makes the data from Salpausselkä in accordance of standard expected by the work.py file
# Already done, this is just here to see what was done to the files if required
# The original files are in CSVs/Salpausselkä/Raw

def concatenate_csv_files(input_folder, output_filename, file_extension):
    csv_files = [file for file in os.listdir(input_folder) if file.endswith(file_extension)]
    dfs = []
    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        dfs.append(df)
    concatenated_df = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(input_folder, output_filename)
    concatenated_df.to_csv(output_path, index=False)
    print(f"Concatenated CSV files saved to: {output_path}")

def merge_dataframes(input_folder, output_filename):
    average_temp_df = pd.read_csv(os.path.join(input_folder, "concatenated_average_temperature.csv"))
    snow_depth_df = pd.read_csv(os.path.join(input_folder, "concatenated_snow_depth.csv"))
    
    merged_df = pd.merge(average_temp_df, snow_depth_df[['Year', 'Month', 'Day', 'Snow depth [cm]']], on=['Year', 'Month', 'Day'], how='inner')
    
    # Drop duplicates based on Year, Month, and Day
    merged_df = merged_df.drop_duplicates(subset=['Year', 'Month', 'Day'])
    
    output_path = os.path.join(input_folder, output_filename)
    merged_df.to_csv(output_path, index=False)
    print(f"Merged CSV files saved to: {output_path}")

if __name__ == "__main__":
    input_folder = os.getcwd() + "\\CSVs\\Salpausselkä\\"

    concatenate_csv_files(input_folder, "Salpausselkä_cloud_coverage.csv", "cloud_coverage.csv")
    concatenate_csv_files(input_folder, "concatenated_average_temperature.csv", "average_temperature.csv")
    concatenate_csv_files(input_folder, "concatenated_snow_depth.csv", "snow_depth.csv")
    
    merge_dataframes(input_folder, "Salpausselkä_average_temperature_and_snow_depth.csv")