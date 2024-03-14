import os
import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

print(CURR_DIR_PATH)
files_path = CURR_DIR_PATH + "\\Finished_CSVs\\"

file_paths = [files_path + "finishedHimos_finished.csv", files_path + "finishedKilpisjärvi_finished.csv", files_path + "finishedLevi_finished.csv", files_path + "finishedPyhä_finished.csv"]
dfs = [pd.read_csv(file) for file in file_paths]
dataset = pd.concat(dfs)
dataset = pd.DataFrame(dataset)
# Drop rows where the average temperature is over 5, somehow makes the models worse
# dataset = dataset[dataset['Average temperature [°C]'] <= 5]
dataset = dataset.dropna(axis= 0, how='any')

# Tried some labeling stuff
# def assign_label(depth):
#     if depth < 10:
#         return 0
#     elif depth < 20:
#         return 10
#     else:
#         return 20

dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset['Weeknr'] = dataset['Date'].dt.isocalendar().week
dataset['Snow depth [cm]'] = dataset['Snow depth [cm]'].replace(-1, 0)
#dataset['Snow depth [cm] label'] = dataset['Snow depth [cm]'].apply(lambda x: assign_label(x)) #labeling stuff
dataset.drop(columns='Date')

y = dataset['Snow depth [cm]']
# y = dataset['Snow depth [cm] label'] #labeling stuff
X = dataset[['Weeknr', 'Average temperature [°C]', 'Cloud cover [1/8]','Direct solar radiation mean [W/m2]']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model_linear = LinearRegression()
model_linear.fit(X_train, y_train)
y_pred_linear_train = model_linear.predict(X_train)
y_pred_linear_test = model_linear.predict(X_test)
y_pred_linear_train = np.maximum(y_pred_linear_train, 0)
y_pred_linear_test = np.maximum(y_pred_linear_test, 0)
mse_train = mean_squared_error(y_train, y_pred_linear_train)
mse_test = mean_squared_error(y_test, y_pred_linear_test)
r2_train = r2_score(y_train, y_pred_linear_train)
r2_test = r2_score(y_test, y_pred_linear_test)
print(f"Linear Regression Train MSE: {mse_train}")
print(f"Linear Regression Test MSE: {mse_test}")
print(f"Linear Regression Train R2 Score: {r2_train}")
print(f"Linear Regression Test R2 Score: {r2_test}")
with open(CURR_DIR_PATH + "\\Models\\linear.pkl", 'wb') as file:
    pkl.dump(model_linear, file)

models = {}
for i in [2, 3, 6]:
    model = make_pipeline(PolynomialFeatures(i), LinearRegression())
    model.fit(X_train, y_train)
    models[i] = model
    with open(CURR_DIR_PATH + f"\\Models\\polynomial{i}.pkl", 'wb') as file:
        pkl.dump(model, file)

for i, model in models.items():
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    y_pred_train = np.maximum(y_pred_train, 0)
    y_pred_test = np.maximum(y_pred_test, 0)
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    final_mse = (mse_train + mse_test).mean()
    final_r2 = (r2_train + r2_test).mean()
    print(f"Polynomial({i}) Regression Train MSE: {mse_train}")
    print(f"Polynomial({i}) Regression Test MSE: {mse_test}")
    print(f"Polynomial({i}) Regression Train R2 Score: {r2_train}")
    print(f"Polynomial({i}) Regression Test R2 Score: {r2_test}")

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.scatter(X_test['Weeknr'], y_pred_linear_test, color='red', alpha=0.1)
plt.scatter(X_test['Weeknr'], y_test, color='blue', alpha=0.1)
plt.xlabel('Weeknr')
plt.ylabel('Snow depth [cm]')
plt.title('Linear Regression Prediction vs Actual')

for j, (i, model) in enumerate(models.items(), start=2):
    plt.subplot(2, 2, j)
    y_pred = model.predict(X_test)
    plt.scatter(X_test['Weeknr'], y_pred, color='red', alpha=0.1)
    plt.scatter(X_test['Weeknr'], y_test, color='blue', alpha=0.1)
    plt.xlabel('Weeknr')
    plt.ylabel('Snow depth [cm]')
    plt.title(f'Polynomial({i}) Regression Prediction vs Actual')

plt.legend(['Predicted', 'Actual'])
plt.tight_layout()
plt.show()
