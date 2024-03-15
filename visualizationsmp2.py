import os
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

# use trained models from ml1.py
path = os.getcwd()
with open(f"{path}\\linear.pkl", "rb") as file:
    model_linear = pkl.load(file)

with open(f"{path}\\random_forest.pkl", "rb")as file:
    model_random_forest = pkl.load(file)

with open(f"{path}\\polynomial2.pkl", "rb")as file:
    model_polynomial2 = pkl.load(file)

with open(f"{path}\\polynomial3.pkl", "rb")as file:
    model_polynomial3 = pkl.load(file)

with open(f"{path}\\polynomial6.pkl", "rb")as file:
    model_polynomial6 = pkl.load(file)

# dataset from in ml1.py
trainingvenues = ['Himos', 'Ilomantsi', 'Kilpisjärvi', 'Levi']
dfs = []
for i in trainingvenues:
    file = f"{path}\\{i}.csv"
    df = pd.read_csv(file)
    dfs.append(df)
dataset = pd.concat(dfs, ignore_index=True)
dataset = pd.DataFrame(dataset)
dataset = dataset.dropna(axis=0, how='any')

# convert/extract wk number/replace/drop
dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset['Weeknr'] = dataset['Date'].dt.isocalendar().week
dataset['Snow depth [cm]'] = dataset['Snow depth [cm]'].replace(-1, 0)
dataset.drop(columns='Date', inplace=True)

# feat and target
y = dataset['Snow depth [cm]']
X = dataset[['Weeknr', 'Average temperature [°C]', 'Cloud cover [1/8]', 'Direct solar radiation mean [W/m2]']]

# use models for predictions
predictions_linear = model_linear.predict(X)
predictions_random_forest = model_random_forest.predict(X)
predictions_polynomial2 = model_polynomial2.predict(X)
predictions_polynomial3 = model_polynomial3.predict(X)
predictions_polynomial6 = model_polynomial6.predict(X)

# evaluate the models
models = {
    'Linear': predictions_linear,
    'Random Forest': predictions_random_forest,
    'Polynomial (degree 2)': predictions_polynomial2,
    'Polynomial (degree 3)': predictions_polynomial3,
    'Polynomial (degree 6)': predictions_polynomial6
}

# change plots to scatter plts 
fig, axs = plt.subplots(3, 2, figsize=(15, 15), tight_layout=True)
colors = ['red', 'green', 'blue', 'orange', 'purple']
axs = axs.ravel()

for ax, (name, predictions), color in zip(axs, models.items(), colors):
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    ax.scatter(X['Weeknr'], y, color='black', alpha=0.5, label='Actual')
    ax.scatter(X['Weeknr'], predictions, color=color, alpha=0.5, label=f'{name}\nMSE: {mse:.2f}\nR-squared: {r2:.2f}')
    ax.set_title(f'{name} Regression Model Predictions')
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Snow depth [cm]')
    ax.legend()
    ax.grid(True)

# fremove extra empty subplot 
fig.delaxes(axs[-1])

plt.show()
