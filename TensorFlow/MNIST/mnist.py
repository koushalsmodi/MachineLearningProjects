from tensorflow.keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# 1) Training data: feature vectors and target values
print(train_images.shape)
print(len(train_labels))
print(train_labels)

print()

print(test_images.shape)
print(len(test_labels))
print(test_labels)

# 2) Prediction function: neural network
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(512, activation="relu"),
    layers.Dense(10, activation="softmax")
])

# 3) Loss function

model.compile(
    optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Preparing the image data
train_images = train_images.reshape((60000, 28*28))
train_images = train_images.astype("float32") / 255
test_images = test_images.reshape((10000), 28*28)
test_images = test_images.astype("float32") /255
print()
print(train_images.shape)

print()

print(test_images.shape)

# Neural networks
model.fit(train_images, train_labels, epochs=5, batch_size=128)

# Prediction
test_digits = test_images[0:10]
predictions = model.predict(test_digits)
print(predictions[0])

print(predictions[0].argmax())
print(predictions[0][7])
print(test_labels[0])

# Evaluating on new data
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"test_acc: {test_acc}")