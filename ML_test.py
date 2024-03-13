
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Directory containing CSV files

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
directory = CURR_DIR_PATH + "\\ML_data\\"

# List to store DataFrames
combined_dfs = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        combined_df = pd.read_csv(os.path.join(directory, filename))
        # Append the DataFrame to the list
        combined_dfs.append(combined_df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(combined_dfs, ignore_index=True)

# Now combined_combined_df contains data from all CSV files


combined_df.dropna(inplace=True)

# Convert 'Date' column to datetime
combined_df['Date'] = pd.to_datetime(combined_df['Date'])

# Extract week number and year from date
combined_df['Week'] = combined_df['Date'].dt.isocalendar().week
combined_df['Year'] = combined_df['Date'].dt.year

# Use 'Week' and 'Year' as features for the x-axis
X = combined_df[['Year', 'Week']].values

y = combined_df.iloc[:, 3].astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6)

model = LinearRegression()
model.fit(X_train, y_train)
print(model.score(X_train, y_train))

# plt.figure(figsize=(8, 6))
# plt.scatter(X_test[:, 1], y_test, color='blue', label='Actual')
# plt.xlabel('Year-Week')
# plt.ylabel('Snow depth')
# plt.title('1. ML testi')
# plt.show()

# Predictions
year = 2050
week = 1
predicted_depth = model.predict([[year, week]])
print(f"Lumen syvyys viikko {week} & vuosi {year}: {predicted_depth[0]}")
