import csv
import random
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

# model = Perceptron()
# model = svm.SVC()
# model = GaussianNB()
model = KNeighborsClassifier(n_neighbors=1)

# Reading data from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    # Skipping header row
    next(reader)
    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": "Authentic" if int(row[4]) == 0 else "Counterfeit"
        })
        
# Separating data into training and test sets
holdout = int(.40 * len(data))
random.shuffle(data)
test = data[:holdout]
train = data[holdout:]

# Training model
X_train = [row["evidence"] for row in train]
y_train = [row["label"] for row in train]
model.fit(X_train, y_train)

# Making predictions
X_test = [row["evidence"] for row in test]
y_test = [row["label"] for row in test]

y_pred = model.predict(X_test)

# Compute how well we performed

correct = 0
incorrect = 0
total = 0
for actual, predicted in zip(y_test, y_pred):
    
    if actual == predicted:
        correct+=1
    else:
        incorrect+=1
    
    total+=1
    
# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy:{100*correct / total: .2f}%")
        