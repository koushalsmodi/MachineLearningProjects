# -*- coding: utf-8 -*-
"""ManipulatingTensorsandRealWorldExamples.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j9aE_kNq-Agq6LknF4iasnH7CE5GoZZR
"""

# ManipulatingTensors
import numpy as np
from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print(train_images.ndim)
print(train_images.shape)
print(train_images.dtype)

my_slice = train_images[10:100]
print(my_slice.ndim) # 3
print(my_slice.shape) # (90, 28, 28)

my_slice_check = train_images[10:100, :, :]
print(my_slice_check.ndim) # 3
print(my_slice_check.shape) # (90, 28, 28)

my_slice_check_another = train_images[10:100, 0:28, 0:28]
print(my_slice_check_another.ndim) # 3
print(my_slice_check_another.shape) # (90, 28, 28)

# Data batches
batch = train_images[:128]
batch = train_images[128:256]

# nth batch
n=3
batch = train_images[128*n:128*(n+1)]
print(batch)

# nth batch and having batch size constant
n=3
batch_size=128
batch = train_images[batch_size*n:batch_size*(n+1)]
print(batch)

# Data tensors in real-world
"""
Vector data (Rank-2): (samples, features) -> (people, (age, gender, income)) (100000,3)
Timeseries data (Rank-3): (samples, timesteps, features) -> (day, [[minutes], [current price, highest price, lowest price]]) (250,390,3)
Image data (Rank-4): (samples, height, width, channel) -> (128, 28,28,1) ; (128, 28, 28, 3) (channels-last)
Video data (Rank-5): (samples, frames, height, width, channel) -> (4, 240, 144,256, 3)

"""