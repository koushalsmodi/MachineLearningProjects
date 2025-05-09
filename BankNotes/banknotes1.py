import csv
import random

from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

with open('banknotes.csv') as f:
    reader = csv.reader(f)
    next(reader)
    
    data = []
    for row in reader:
        data.append({
            "evidence": [ float(cell) for cell in row[:4]],
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })
    
evidence = [row["evidence"] for row in data]
label = [row["label"] for row in data]  
    
# Training data
# Validation data
# Model training
# Model prediction and loss function

X_train, X_val, y_train, y_val = train_test_split(evidence, label, train_size=.8)

model = Perceptron()

model.fit(X_train, y_train)

y_pred = model.predict(X_val)

correct = (y_pred == y_val).sum()
incorrect = (y_pred != y_val).sum()

total = len(y_pred)

print(f"Model name: {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Classification accuracy: {100*correct/total: .2f}")