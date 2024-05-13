import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.linear_model 
import sklearn.model_selection
import matplotlib.pyplot as plt

#%%
dataset = sk.datasets.load_breast_cancer()
X_full = dataset.data
y_full = dataset.target

#%%
X_train, X_val, y_train, y_val = sk.model_selection.train_test_split(X_full, y_full) 
    
#%%
mu = np.mean(X_train, axis = 0)
s = np.std(X_train, axis = 0) 

X_train = (X_train-mu)/s
X_val = (X_val-mu)/s  

#%%
X = np.insert(X_train, 0, 1, axis = 1) 
X_val_aug = np.insert(X_val, 0, 1, axis = 1)

#%%
def sigmoid(u):
    return 1 / (1+ np.exp(-u))

def bce(p, q):
    return -p*np.log(q) - (1-p)*np.log(1-q)

def average_cross_entropy(beta, X, y):
    N = len(X)
    L = 0
    
    for i in range(N):
        xiHat = X[i]
        yi = y[i]
        yi_pred = sigmoid(np.vdot(xiHat, beta))
        cross_entropy = bce(yi, yi_pred)
        L += cross_entropy
    L = L / N 
    return L

def grad_L(beta, X, y):
    N = len(X)
    grad = np.zeros(d+1)
    
    for i in range(N):
        xiHat = X[i]
        yi = y[i]
        yi_pred = sigmoid(np.vdot(xiHat, beta))
        grad = grad + (yi_pred - yi)*xiHat
    grad = grad / N 
    return grad
N_train, d = X_train.shape
#%%
num_iters = 200
learning_rates = [.001, .01, .1]
plt.figure()
for learning_rate in learning_rates:
    beta = np.zeros(d+1)
    ace_vals = []
    
    for i in range(num_iters):
        beta = beta - learning_rate*grad_L(beta, X, y_train)
        
        ace = average_cross_entropy(beta, X, y_train)
        
        ace_vals.append(ace)
    plt.plot(ace_vals, label = f'Learning Rate: {learning_rate}')
    
plt.title('Avg. cross entropy vs. iteration')
plt.legend()
plt.show()
#%%
N_val = len(X_val)
num_correct = 0

for i in range(N_val):
    xiHat = X_val_aug[i]
    yi = y_val[i]
    yi_pred = sigmoid(np.vdot(xiHat, beta))
    yi_pred = np.round(yi_pred)
    
    if yi == yi_pred:
        num_correct += 1
accuracy = num_correct / N_val
print(f'Classifcation accuracy: {accuracy}')
    
    
    
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    



