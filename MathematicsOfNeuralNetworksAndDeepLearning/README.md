# Mathematics and Recipe for Deep Learning

## Overview

Linear Regression
- Training Data: Feature vectors and Target values
- Prediction function: f(xi) ~ y(i)
- Loss function: l(yi, f(xi)) = (yi - f(xi))^2 (Mean Squared Error); l(y,y^)=  |y-y^| (Absolute Error Loss)
- Cost/ Objective function
L(B) = 1/N * ||XB-Y||^2

Logistic Regression:
- Logistic Regression, Naive Bayes Classifier

## Geometric interpretation of tensor operations
- Translation
- Rotation
- Scaling
- Linear Transform
- Affine Transform (Linear Transform + Translation) = Dense layer without activation function
- Dense layer with relu activation

## Derivative
- If you want to reduce the value of f(x), need to move x a little in the opposite direction from the derivative. Gradient points in the direction of the steepest increase and since we want to minimize cost, we need to move in the opposite direction from the derivative.
- If slope is negative, it means a small increase in x around point p will result in a decrease of f(x), and if slope is positive, it means a small increase in x around point p will result in an increase of f(x).
- grad(f(W), W) is a combination of scalar functions grad_ij(f(W), w_ij), each of which would return the derivative of loss_value = f(W) with respect to the coefficient W[i,j] of W, assuming all other coefficients are constant. grad_ij is called the partial derivative of f with respect to W[i,j].
