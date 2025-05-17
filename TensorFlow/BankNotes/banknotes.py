import csv
import tensorflow as tf  # pylint: disable=no-member
from sklearn.model_selection import train_test_split
import numpy as np

with open('banknotes.csv') as f:

    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({
            "evidence":[float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and test groups

evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]

X_train, X_val, y_train, y_val = train_test_split(evidence, labels, train_size=.8)

X_train = np.array(X_train)
y_train = np.array(y_train)
X_val = np.array(X_val)
y_val = np.array(y_val)

# Create a neural network
model = tf.keras.models.Sequential()

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))

# Add output layer with 1 unit

model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(X_train, y_train, epochs=20)

# Evaluate how well model performs

model.evaluate(X_val, y_val, verbose=2)



