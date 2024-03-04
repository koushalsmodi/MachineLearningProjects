
import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.linear_model
import sklearn.model_selection
from pprint import pprint

dataset = sk.datasets.load_breast_cancer()

X = dataset.data
y = dataset.target

X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X, y)

model = sk.linear_model.LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_val)
accuracy = np.mean(y_pred == y_val)
print(f'accuracy is: {accuracy}') # 0.9370629370629371

# 1st approach alternate way to find a probability with a set threshold
threshold = .7
probabilities = model.predict_proba(X_val)
y_pred2 = (probabilities[:, 1] > threshold).astype('float64')
accuracy2 = np.mean(y_pred2 == y_val)
print(f'accuracy2 is: {accuracy2}') # 0.9440559440559441

# 1st approach with a for loop to find a probability with a set threshold
N = len(X_val)
y_pred3 = np.zeros(N)

for i in range(N):
    if probabilities[i, 1] > threshold:
        y_pred3[i] = 1
    else:
        y_pred3[i] = 0
        
accuracy3 = np.mean(y_pred3 == y_val)
print(f'accuracy3 is: {accuracy3}') # 0.9440559440559441

# Here, accuracy2 and accuracy3 will have the same answer
