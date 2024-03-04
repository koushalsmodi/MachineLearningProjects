import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.model_selection
import sklearn.linear_model

dataset = sk.datasets.load_iris()
X = dataset.data
y = dataset.target

X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X, y)

model = sk.linear_model.LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

accuracy = np.mean(y_pred == y_val)
print(f'accuracy: {accuracy}')
