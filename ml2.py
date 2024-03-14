import os
import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
files_path = CURR_DIR_PATH + "\\Finished_CSVs\\"

with open(CURR_DIR_PATH + "\\Models\\linear.pkl", "rb") as file:
    model_linear = pkl.load(file)

with open(CURR_DIR_PATH + "\\Models\\polynomial2.pkl", "rb")as file:
    model_polynomial2 = pkl.load(file)

with open(CURR_DIR_PATH + "\\Models\\polynomial3.pkl", "rb")as file:
    model_polynomial3 = pkl.load(file)

with open(CURR_DIR_PATH + "\\Models\\polynomial6.pkl", "rb")as file:
    model_polynomial6 = pkl.load(file)

dataset = pd.read_csv(files_path + "finishedTalma_finished.csv")
dataset = dataset.dropna(axis= 0, how='any')
dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset['Weeknr'] = dataset['Date'].dt.isocalendar().week
dataset['Snow depth [cm]'] = dataset['Snow depth [cm]'].replace(-1, 0)
dataset.drop(columns='Date')

y = dataset['Snow depth [cm]']
X = dataset[['Weeknr', 'Average temperature [°C]','Cloud cover [1/8]','Direct solar radiation mean [W/m2]']]

predictions_linear = model_linear.predict(X)
predictions_polynomial2 = model_polynomial2.predict(X)
predictions_polynomial3 = model_polynomial3.predict(X)
predictions_polynomial6 = model_polynomial6.predict(X)

print("Linear Model:")
print("Mean Squared Error:", mean_squared_error(y, predictions_linear))
print("R-squared:", r2_score(y, predictions_linear))
print("\n")

print("Polynomial (degree 2) Model:")
print("Mean Squared Error:", mean_squared_error(y, predictions_polynomial2))
print("R-squared:", r2_score(y, predictions_polynomial2))
print("\n")

print("Polynomial (degree 3) Model:")
print("Mean Squared Error:", mean_squared_error(y, predictions_polynomial3))
print("R-squared:", r2_score(y, predictions_polynomial3))
print("\n")

print("Polynomial (degree 6) Model:")
print("Mean Squared Error:", mean_squared_error(y, predictions_polynomial6))
print("R-squared:", r2_score(y, predictions_polynomial6))
print("\n")

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.scatter(X['Weeknr'], predictions_linear, color='red', alpha=0.1)
plt.scatter(X['Weeknr'], y, color='blue', alpha=0.1)
plt.xlabel('Weeknr')
plt.ylabel('Snow depth [cm]')
plt.title('Linear Regression Prediction vs Actual')

plt.subplot(2, 2, 2)
plt.scatter(X['Weeknr'], predictions_polynomial2, color='red', alpha=0.1)
plt.scatter(X['Weeknr'], y, color='blue', alpha=0.1)
plt.xlabel('Weeknr')
plt.ylabel('Snow depth [cm]')
plt.title('Linear Regression Prediction vs Actual')

plt.subplot(2, 2, 3)
plt.scatter(X['Weeknr'], predictions_polynomial3, color='red', alpha=0.1)
plt.scatter(X['Weeknr'], y, color='blue', alpha=0.1)
plt.xlabel('Weeknr')
plt.ylabel('Snow depth [cm]')
plt.title('Linear Regression Prediction vs Actual')

plt.subplot(2, 2, 4)
plt.scatter(X['Weeknr'], predictions_polynomial6, color='red', alpha=0.1)
plt.scatter(X['Weeknr'], y, color='blue', alpha=0.1)
plt.xlabel('Weeknr')
plt.ylabel('Snow depth [cm]')
plt.title('Linear Regression Prediction vs Actual')

plt.legend(['Predicted', 'Actual'])
plt.tight_layout()
plt.show()