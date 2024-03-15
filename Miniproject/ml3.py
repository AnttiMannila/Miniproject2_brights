import os
import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = os.getcwd()
with open(f"{path}\\linear.pkl", "rb") as file:
    model_linear = pkl.load(file)

with open(f"{path}\\random_forest.pkl", "rb") as file:
    model_forest = pkl.load(file)

models_polynomial = {}
for i in [2, 3, 6]:
    with open(f"{path}\\polynomial{i}.pkl", "rb") as file:
        models_polynomial[i] = pkl.load(file)

additional_venues = ['Pyhä', 'Salpausselkä', 'Sveitsi', 'Tahko', 'Talma', 'Vihti']
dfs_additional = []
for venue in additional_venues:
    file = f"{path}\\{venue}.csv"
    df = pd.read_csv(file)
    dfs_additional.append(df)
data_additional = pd.concat(dfs_additional, ignore_index=True)

data_additional['Date'] = pd.to_datetime(data_additional['Date'])
data_additional['Weeknr'] = data_additional['Date'].dt.isocalendar().week
data_additional['Snow depth [cm]'] = data_additional['Snow depth [cm]'].replace(-1, 0)
data_additional.drop(columns='Date', inplace=True)

def generate_features_for_date(date, existing_data):
    date_week_number = date.isocalendar()[1]
    data_within_week = existing_data[existing_data['Weeknr'] == date_week_number]
    features = data_within_week[['Weeknr', 'Average temperature [°C]', 'Cloud cover [1/8]', 'Direct solar radiation mean [W/m2]']].mean().values
    return features

years = 20
num_weeks_future = years * 52
start_date = pd.Timestamp.now().to_pydatetime()
future_dates = [start_date + pd.Timedelta(weeks=i) for i in range(num_weeks_future)]
predictions = {}

for venue in additional_venues:
    extrapolated_data = np.array([generate_features_for_date(date, data_additional) for date in future_dates])
    predictions_linear = model_linear.predict(extrapolated_data)
    predictions_forest = model_forest.predict(extrapolated_data)
    predictions_polynomial = {}
    for degree, model in models_polynomial.items():
        predictions_polynomial[degree] = model.predict(extrapolated_data)
    predictions[venue] = {'Linear': predictions_linear, 'Random Forest': predictions_forest, 'Polynomial': predictions_polynomial}

plt.figure(figsize=(12, 8))

plt.plot(future_dates, predictions_linear, label='Linear Regression')

plt.plot(future_dates, predictions_forest, label='Random Forest')

for degree, predictions in predictions_polynomial.items():
    plt.plot(future_dates, predictions, label=f'Polynomial Degree {degree}')

plt.xlabel('Date')
plt.ylabel('Snow Depth [cm]')
plt.title('Predicted Snow Depth for All Models')
plt.legend()
plt.grid(True)

weeks_low_snow_10cm = set()
weeks_low_snow_20cm = set()
for model_name, model_predictions in [('Linear Regression', predictions_linear[:52]),
                                      ('Random Forest', predictions_forest[:52])] + \
                                     [(f'Polynomial Degree {degree}', predictions[:52])
                                      for degree, predictions in predictions_polynomial.items()]:
    for i, preds in enumerate(model_predictions):
        if np.all(preds < 10):
            weeks_low_snow_10cm.add(i + 1)
            weeks_low_snow_20cm.add(i + 1)
        elif np.all(preds < 20):
            weeks_low_snow_20cm.add(i + 1)

weeks_high_snow_10cm = set(range(1, 53)) - weeks_low_snow_10cm
weeks_high_snow_20cm = set(range(1, 53)) - weeks_low_snow_20cm

if weeks_low_snow_10cm:
    print(f"Weeks with predicted snow depth < 10cm: {sorted(weeks_low_snow_10cm)}")
if weeks_high_snow_10cm:
    print(f"Weeks with predicted snow depth >= 10cm: {sorted(weeks_high_snow_10cm)}")
if weeks_low_snow_20cm:
    print(f"Weeks with predicted snow depth < 20cm: {sorted(weeks_low_snow_20cm)}")
if weeks_high_snow_20cm:
    print(f"Weeks with predicted snow depth >= 20cm: {sorted(weeks_high_snow_20cm)}")

plt.tight_layout()
plt.show()


# This is the same but separate subplots
# plt.figure(figsize=(12, 8))

# # Linear Regression
# plt.subplot(3, 2, 1)
# for venue in additional_venues:
#     predictions_linear = predictions[venue]['Linear']
#     plt.plot(future_dates, predictions_linear)

# plt.xlabel('Date')
# plt.ylabel('Snow Depth [cm]')
# plt.title('Predicted Snow Depth for Linear Regression')
# plt.legend()
# plt.grid(True)

# # Random Forest
# plt.subplot(3, 2, 2)
# for venue in additional_venues:
#     predictions_forest = predictions[venue]['Random Forest']
#     plt.plot(future_dates, predictions_forest)

# plt.xlabel('Date')
# plt.ylabel('Snow Depth [cm]')
# plt.title('Predicted Snow Depth for Random Forest')
# plt.legend()
# plt.grid(True)

# # Polynomial Regression
# for i, degree in enumerate(models_polynomial.keys(), start=3):
#     plt.subplot(3, 2, i)
#     for venue in additional_venues:
#         predictions_polynomial = predictions[venue]['Polynomial'][degree]
#         plt.plot(future_dates, predictions_polynomial)

#     plt.xlabel('Date')
#     plt.ylabel('Snow Depth [cm]')
#     plt.title(f'Predicted Snow Depth for Polynomial Regression (Degree {degree})')
#     plt.legend()
#     plt.grid(True)

# weeks_low_snow_10cm = set()
# weeks_low_snow_20cm = set()
# for model_name, model_predictions in [('Linear Regression', predictions_linear[:52]),
#                                       ('Random Forest', predictions_forest[:52])] + \
#                                      [(f'Polynomial Degree {degree}', predictions[:52])
#                                       for degree, predictions in predictions_polynomial.items()]:
#     for i, preds in enumerate(model_predictions):
#         if np.all(preds < 10):
#             weeks_low_snow_10cm.add(i + 1)
#             weeks_low_snow_20cm.add(i + 1)
#         elif np.all(preds < 20):
#             weeks_low_snow_20cm.add(i + 1)

# weeks_high_snow_10cm = set(range(1, 53)) - weeks_low_snow_10cm
# weeks_high_snow_20cm = set(range(1, 53)) - weeks_low_snow_20cm

# if weeks_low_snow_10cm:
#     print(f"Weeks with predicted snow depth < 10cm: {sorted(weeks_low_snow_10cm)}")
# if weeks_high_snow_10cm:
#     print(f"Weeks with predicted snow depth >= 10cm: {sorted(weeks_high_snow_10cm)}")
# if weeks_low_snow_20cm:
#     print(f"Weeks with predicted snow depth < 20cm: {sorted(weeks_low_snow_20cm)}")
# if weeks_high_snow_20cm:
#     print(f"Weeks with predicted snow depth >= 20cm: {sorted(weeks_high_snow_20cm)}")

# plt.tight_layout()
# plt.show()