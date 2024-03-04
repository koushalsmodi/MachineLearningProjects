# importing libraries
import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.model_selection
import sklearn.linear_model

# working with iris dataset
dataset = sk.datasets.load_iris()
X = dataset.data
y = dataset.target

# splitting the dataset into training and validation sets
X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X, y)

# training the model using scikit-learn
model = sk.linear_model.LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

# measuring accuracy, that is, how well do the predicted probabilities agree with the ground truth probability.
accuracy = np.mean(y_pred == y_val)
print(f'accuracy: {accuracy}')
