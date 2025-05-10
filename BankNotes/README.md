# Banknote Authentication Classifier

This Python script trains and evaluates a simple machine learning model to classify banknotes as either "Authentic" or "Counterfeit" based on a dataset of banknote features. Project idea is from Harvard CS50's AI course.

## Overview

The script reads data from a CSV file named `banknotes.csv`. This file is expected to contain five columns: four numerical features representing characteristics of a banknote (e.g., variance of wavelet transformed image, skewness, curtosis, entropy), and a fifth column indicating the class label (0 for Authentic, 1 for Counterfeit).

The script performs the following steps:

1.  **Data Loading and Preprocessing:**
    * Reads the `banknotes.csv` file using the `csv` module.
    * Skips the header row.
    * Parses each row, extracting the four feature values as floating-point numbers and the class label, converting '0' to "Authentic" and '1' to "Counterfeit".
    * Separates the data into two lists: `evidence` (containing the feature vectors) and `label` (containing the corresponding class labels).

2.  **Data Splitting:**
    * Uses the `train_test_split` function from `sklearn.model_selection` to split the data into training and validation sets.
    * 80% of the data is used for training (`X_train`, `y_train`), and 20% is used for validation (`X_val`, `y_val`). This allows for evaluating the model's performance on unseen data.

3.  **Model Training:**
    * Initializes a `Perceptron` model from `sklearn.linear_model`. The Perceptron is a simple linear classifier.
    * Trains the model using the training data (`X_train`, `y_train`) with the `fit()` method. The model learns to associate the banknote features with their respective classes.

4.  **Model Evaluation:**
    * Uses the trained model to predict the class labels for the validation data (`X_val`) using the `predict()` method. The predictions are stored in `y_pred`.
    * Compares the predicted labels (`y_pred`) with the actual labels (`y_val`) to calculate the number of correct and incorrect predictions.
    * Calculates the classification accuracy as the percentage of correctly classified banknotes in the validation set.

5.  **Output:**
    * Prints the name of the model used (in this case, "Perceptron").
    * Prints the number of correctly and incorrectly classified banknotes in the validation set.
    * Prints the classification accuracy of the model, formatted to two decimal places.

## Requirements

* Python 3.x
* The following Python libraries:
    * `csv` (built-in)
    * `random` (built-in)
    * `scikit-learn` (`sklearn`) - You can install it using pip: `pip install scikit-learn`

## Usage

1.  **Save the code:** Save the Python script as a `.py` file (e.g., `banknote_classifier.py`).
2.  **Prepare the data:** Ensure you have a CSV file named `banknotes.csv` in the same directory as the script. The file should be formatted as described in the "Overview" section.
3.  **Run the script:** Open a terminal or command prompt, navigate to the directory where you saved the script and the CSV file, and run the script using the command: `python banknote_classifier.py`

## Expected Output

The output will be similar to the following (the exact numbers may vary slightly due to the random splitting of the data):
* Model name: Perceptron
* Correct: 270
* Incorrect: 5
* Classification accuracy:  98.18