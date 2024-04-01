# normal equations: linear regression
# XTX = XTy
import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.model_selection
import sklearn.linear_model

dataset = sk.datasets.fetch_california_housing()
X_full = dataset.data
y_full = dataset.target

X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X_full, y_full)

mu = np.mean(X_train, axis = 0)
s = np.std(X_train, axis = 0)

X_train = (X_train - mu) / s
X_val = (X_val - mu) / s

X = np.insert(X_train, 0, 1, axis = 1)

XTX = X.T @ X

XTy = X.T @ y_train

beta = np.linalg.solve(XTX, XTy)

y_pred = beta[0] + X_val @ beta[1:]
mse_normal_equations = np.mean((y_val - y_pred)**2)
print(f'mse_normal_equations: {mse_normal_equations}')

# what scikit-learn does under the hood^
# checking against scikit-learn's actual version
model = sk.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_scikit_learn = model.predict(X_val)
mse_scikit_learn = np.mean((y_val - y_scikit_learn)**2)
print(f'mse_scikit_learn: {mse_scikit_learn}')
 
max_error = np.max(np.abs(y_scikit_learn - y_pred))
print(f'Both the values are same because the max error is: {max_error}')
