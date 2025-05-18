# Traffic Sign Multiclass Classification with TensorFlow

**Dataset**: https://benchmark.ini.rub.de/?section=gtsrb&subsection=news

This project implements and compares two Convolutional Neural Network (CNN) architectures on the German Traffic Sign Recognition Benchmark (GTSRB) dataset using TensorFlow/Keras for the task of road sign classification across **43 categories** of road signs such as stop signs, speed limit signs, yield signs, and so on.

--

## Project Summary

Using TensorFlow/Keras, 2 distinct CNN models are trained and evaluated to classify traffic signs. Both models are evaluated on **training accuracy and test accuracy**.

--- 
# Model 1: Deeper CNN

**Architecture**:
- 2 Convolutional Layers: 64 filters and 32 filtes
- Max Pooling
- Flattening
- 1 Dense Hidden Layer
- Output Layer: Softmax (43 classes)

**Performance**:
- Training Accuracy: ~90.3%
- Test Accuracy: ~93.4%
- Training Time: Longer due to higher filter complexity

# Model 2: Shallow CNN with more Dense Layers

**Architecture**:
- 1 Convolutional Layer: 32 filters
- Max Pooling (larger size)
- Multiple Dense Layers
- Dropout Regularization
- Output Layer: Softmax (43 classes)

**Performance**:
- Training Accuracy: ~5.1%
- Test Accuracy: ~5.6%
- Training Time: Significantly faster (6–10 seconds per epoch)

> Model 2 is significantly faster and avoids early complexity by relying on dense layers and dropout.


## Sample Output from Model 1
![Model 1](image-1.png)

## Sample Output from Model 2
![Model 2](image.png)

## 📊 Accuracy Comparison

**Baseline Accuracy** (random guessing):  
1/43= 2.3%.

Model 1 (the deeper CNN) significantly outperforms Model 2 (the shallow CNN with more dense layers) in the task of traffic sign multiclass classification on the GTSRB dataset.
---

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
python3 traffic.py directory_name
