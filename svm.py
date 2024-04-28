import data_handler as dh
import pandas as pd
import numpy as np
import sklearn as sk

from sklearn.svm import SVR
from train_model_tree import get_data


def train_svm(training, kernel='rbf', C=1.0, epsilon=0.1):
    # Extract features and target variable from training data
    X_train = training[:, :-1]
    y_train = training[:, -1]
    
    # Initialize SVM model
    svm_model = SVR(kernel=kernel, C=C, epsilon=epsilon)
    
    # Train the SVM model
    svm_model.fit(X_train, y_train)
    
    return svm_model

# Get the training data
train, _ = get_data()

# Train the SVM model
svm_model = train_svm(train)