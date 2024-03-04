# importing libraries
import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.model_selection
import sklearn.linear_model

# loading the California housing dataset
dataset = sk.datasets.fetch_california_housing()

X = dataset.data
y = dataset.target

# splitting the dataset into training and validation sets

X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X, y)

# training the model using scikit-learn
model = sk.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

# calculating the mean squared error using the validation dataset
mse_val = np.mean((y_pred - y_val) ** 2)
print(f'Mean squared error using validation dataset is: {mse_val}')

# getting the beta parameter values that scikit-learn has generated
beta0 = model.intercept_
beta1 = model.coef_

# the formula for a predicted probability follows the affine function:
# fxi = B0 + B1xi1 + B2xi2 + ........ + Bdxid
# here, B0 = beta0
# and B1, B2, ...., Bd are stored as an array in beta1
# adding B0 to teh dot product of the X values of the validation dataset with the beta1, gives the predicted probability.
# then mean squared error is the squared difference between the predicted and the ground truth and taking the mean.

y_pred_check = beta0 + X_val @ beta1
mse_val_check = np.mean((y_pred_check - y_val) ** 2)
print(f'Mean squared check error using validation dataset is: {mse_val_check}')
