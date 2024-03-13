import pandas as pd
import os
import work as wk
import time

start_time = time.time()

if __name__ == "__main__":
    venues = []
    folders = os.listdir(os.path.join(os.getcwd(), "CSVs"))
    for folder in folders:
        folder_path = os.path.join(os.getcwd(), "CSVs", folder)
        if os.path.isdir(folder_path):
            venues.append(folder)
    for i in venues:
        input_folder = os.getcwd() + f"\\CSVs\\{i}\\"
        solar_radiation_file = os.path.join(os.getcwd() + "\\CSVs\\", "concatenated_solar_radiation.csv")
        average_temperatures_and_snow_depth_file = os.path.join(input_folder, [file for file in os.listdir(input_folder) if file.endswith("average_temperature_and_snow_depth.csv")][0])
        cloud_coverage_file = os.path.join(input_folder, [file for file in os.listdir(input_folder) if file.endswith("cloud_coverage.csv")][0])
        solar_radiation_df = pd.read_csv(solar_radiation_file)
        solar_radiation_df = wk.preprocess_solar_radiation_data(solar_radiation_df)
        temp_snow_df = pd.read_csv(average_temperatures_and_snow_depth_file)
        temp_snow_df = wk.preprocess_temperature_and_snow_depth_data(temp_snow_df)
        cloud_coverage_df = pd.read_csv(cloud_coverage_file)
        cloud_coverage_df = wk.preprocess_cloud_coverage_data(cloud_coverage_df)
        final_df = wk.join_dataframes(solar_radiation_df, temp_snow_df, cloud_coverage_df, i)
        output_file = os.path.join(os.getcwd() + f"\\Finished_CSVs\\{i}_combined_data.csv")
        if os.path.exists(output_file):
            os.remove(output_file)
        final_df.to_csv(output_file, index=False)
        print(f"Combined data saved to: {output_file}")
        wk.count_nulls()

end_time = time.time()
print(f"The script took {end_time - start_time} seconds.")
