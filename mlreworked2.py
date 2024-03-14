import os
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

path = os.getcwd()
testingvenues = ['Levi']

with open(f"{path}\\linear.pkl", "rb") as file:
    model_linear = pkl.load(file)

with open(f"{path}\\polynomial2.pkl", "rb")as file:
    model_polynomial2 = pkl.load(file)

with open(f"{path}\\polynomial23.pkl", "rb")as file:
    model_polynomial3 = pkl.load(file)

with open(f"{path}\\polynomial26.pkl", "rb")as file:
    model_polynomial6 = pkl.load(file)

for i in testingvenues:
    file = f"{path}\\data\\{i}.csv"
    df = pd.read_csv(file)
    dataset = pd.concat(df)
dataset = dataset.dropna(axis= 0, how='any')
dataset['Date'] = pd.to_datetime(dataset[['Year', 'Month', 'Day']])
dataset['Weeknr'] = dataset['Date'].dt.isocalendar().week
dataset['Snow depth [cm]'] = dataset['Snow depth [cm]'].replace(-1, 0)
dataset.drop(columns=['Date', 'Year', 'Month', 'Day'])

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