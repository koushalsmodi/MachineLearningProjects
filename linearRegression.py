import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.model_selection
import sklearn.linear_model

dataset = sk.datasets.fetch_california_housing()

X = dataset.data
y = dataset.target

X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X, y)

model = sk.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

mse_val = np.mean((y_pred - y_val) ** 2)
print(f'Mean squared error using validation dataset is: {mse_val}')

beta0 = model.intercept_
beta1 = model.coef_

y_pred_check = beta0 + X_val @ beta1
mse_val_check = np.mean((y_pred_check - y_val) ** 2)
print(f'Mean squared check error using validation dataset is: {mse_val_check}')
