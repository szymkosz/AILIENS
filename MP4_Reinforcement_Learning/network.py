"""
PARAMETERS TO VARY:

1. Number of layers
2. Number of units per layer
3. Learning rate
4. Weight scale parameter (for initializing weights randomly)
5. Number of epochs
6. Minibatch size


MISCELLANEOUS:

1. Numpy random seed
2. Random seed
"""


#### Libraries
# Standard library
import random

# Third-party libraries
import numpy as np

NUM_STATE_ATTRIBUTES = 5
NUM_UNITS_IN_LAST_LAYER = 3


class Network(object):
    def __init__(self, num_layers=4, num_units_per_layer=256, learning_rate=0.1, weight_scale_parameter=1.0):
        np.random.seed(7383)

        # Save the number of layers, number of units per layer (except the last layer, which is 3 units)
        self.num_layers = num_layers
        self.num_units_per_layer = num_units_per_layer
        self.learning_rate = learning_rate

        # Randomly initialize weight matrices with a uniform distribution multiplied by a scaling factor
        self.weights = [weight_scale_parameter * np.random.rand((NUM_STATE_ATTRIBUTES, num_units_per_layer))]
        self.weights += [(weight_scale_parameter * np.random.rand((num_units_per_layer, num_units_per_layer)) for i in range(num_layers-2)]
        self.weights.append( (weight_scale_parameter * np.random.rand((num_units_per_layer, NUM_UNITS_IN_LAST_LAYER))) )

        # Initialize bias vectors to zero
        self.biases = [np.zeros(num_units_per_layer) for i in range(num_layers-1)]
        self.biases.append(np.zeros(NUM_UNITS_IN_LAST_LAYER))

        # Of the form (A_i, W_i, b_i) for the ith layer
        self.affine_caches = [(None, None, None) for i in range(num_layers)] # Of the form (A_i, W_i, b_i) for the ith layer
        self.relu_caches = [None for i in range(num_layers-1)]


    # Handle feedforward
    def feedforward(self, X):
        # Handle feedforward
        A = mini_batch
        F = None
        for i in range(self.num_layers):
            W = self.weights[i]
            b = self.biases[i]

            if i < (self.num_layers - 1):
                Z, self.affine_caches[i] = Affine_Forward(A, W, b)
                A, self.relu_caches[i] = ReLU_Forward(Z)
            else:
                F, self.affine_caches[i] = Affine_Forward(A,W,b)

        return F


    # Handle backpropagation
    def backpropagation(self, F, y):
        loss, dF = Cross_Entropy(F, y)
        dZ = dF
        for i in range(self.num_layers - 1, -1, -1):
            acache = self.affine_caches[i]

            dA, dW, db = Affine_Backward(dZ, acache)

            # Do gradient descent
            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * db

            if i > 0:
                rcache = self.relu_caches[i-1]
                dZ = ReLU_Backward(dA, rcache)

        return loss


    def classify_or_train(self, X, y, test):
        F = self.feedforward(X)

        # If this is the test phase, assign actions to the states and return them
        if test:
            classifications = np.argmax(F, axis=1)
            return classifications
        else:
            return backpropagation

        loss = self.backpropagation(F, y)
        return loss


    def MinibatchGD(self, data, epochs=300, mini_batch_size=128):
        training_dataset = data[0]
        training_labels = data[1]
        n = training_dataset.shape[0]

        for i in range(epochs):
            row_indices = np.arange(n)
            np.random.shuffle(row_indices)

            for j in range(n/mini_batch_size):
                mini_batch_row_indices = row_indices[(j*mini_batch_size):((j+1)*mini_batch_size)]

                X = training_dataset[mini_batch_row_indices, :]
                y = training_labels[mini_batch_row_indices]
                self.classify_or_train(X, y, False)


def Affine_Forward(A, W, b):
    Z = np.dot(A, W) + b.T
    acache = (A, W, b)
    return (Z, acache)

def Affine_Backward(dZ, cache):
    A = cache[0]
    W = cache[1]
    b = cahce[2]

    dA =
    dW =
    db =
    return (dA, dW, db)

def ReLU_Forward(Z):
    A = np.maximum(Z, 0, Z)
    rcache = Z
    return (A, rcache)

def ReLU_Backward(dA, cache):
    dZ = np.where(cache < 0, np.zeros(cache.size), dA)
    return dZ

def Cross_Entropy(F, y):
    pass
