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


# Import the necessary libraries
#from agent import Agent
from Agents.agent import Agent
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import helper
#sys.path.append('../Data')

# CONSTANTS
NUM_STATE_ATTRIBUTES = 5
NUM_UNITS_IN_LAST_LAYER = 3


class network(Agent):
    def __init__(self, num_layers=4, num_units_per_layer=256, learning_rate=0.1, weight_scale_parameter=(1.0/256)):
        np.random.seed(7383)

        # Save the number of layers, number of units per layer (except the last layer, which is 3 units)
        self.num_layers = num_layers
        self.num_units_per_layer = num_units_per_layer
        self.learning_rate = learning_rate

        # Randomly initialize weight matrices with a uniform distribution multiplied by a scaling factor
        self.weights = [weight_scale_parameter * np.random.rand(NUM_STATE_ATTRIBUTES, num_units_per_layer)]
        self.weights += [(weight_scale_parameter * np.random.rand(num_units_per_layer, num_units_per_layer)) for i in range(num_layers-2)]
        self.weights.append( (weight_scale_parameter * np.random.rand(num_units_per_layer, NUM_UNITS_IN_LAST_LAYER)) )

        # Initialize bias vectors to zero
        self.biases = [np.zeros(num_units_per_layer) for i in range(num_layers-1)]
        self.biases.append(np.zeros(NUM_UNITS_IN_LAST_LAYER))

        # Of the form (A_i, W_i, b_i) for the ith layer
        self.affine_caches = [(None, None, None) for i in range(num_layers)] # Of the form (A_i, W_i, b_i) for the ith layer
        self.relu_caches = [None for i in range(num_layers-1)]


    # Handle feedforward
    def feedforward(self, X):
        # TODO: Check if this function would break if X was a 1D 5-dimensional vector
        A = X
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


    """
    The classify_or_train function does one of two things:

    If test == True, the classify_or_train function takes in a mini-batch of training
    data X along with a corresponding vector of true labels y, feeds the mini-batch
    forward through the neural network, backpropagates the gradients, and updates
    the weights and biases of the neural network.

    If test == False, the classify_or_train function takes in either a single vector
    with the 5 attributes of the current state (if the agent is playing the game) or
    the entire training dataset (if the overall classification accuracy across the
    training dataset is being computed during the training phase).  The y argument
    is ignored in this case, so it can be set to a Nonetype.
    """
    def classify_or_train(self, X, y, test):
        F = self.feedforward(X)

        # If this is the test phase, assign actions to the states and return them
        if test:
            classifications = np.argmax(F, axis=1)
            return classifications

        loss = self.backpropagation(F, y)
        return loss


    def MinibatchGD(self, data, epochs=300, mini_batch_size=128):
        np.random.seed(3489)

        # Extract the training dataset and labels and scale the dataset
        training_dataset = data[0]
        scaled_dataset = scale_dataset(training_dataset)
        training_labels = data[1]

        # Identify the number of training vectors and compute the nubmer of mini-batches
        n = training_dataset.shape[0]
        num_mini_batches = int(np.ceil(n/mini_batch_size))

        # Initialize the vectors of average loss and accuracy
        # over training dataset within each epoch
        losses = np.zeros(epochs)
        accuracies = np.zeros(epochs)
        final_assigned_labels = None

        # Train the neural network over multiple epochs
        for i in range(epochs):
            # Shuffle the training data by making a vector of
            # row indices of training vectors and shuffling it
            row_indices = np.arange(n)
            np.random.shuffle(row_indices)

            total_loss = 0

            for j in range(num_mini_batches):
                # Extract the indices of the training vectors of this mini-batch
                beginning_index = (j*mini_batch_size)
                ending_index = min((j+1)*mini_batch_size, n)
                mini_batch_row_indices = row_indices[beginning_index:ending_index]

                # Extract the training vectors of this mini-batch and their
                # labels and propagate them through the network for training
                X = scaled_dataset[mini_batch_row_indices, :]
                y = training_labels[mini_batch_row_indices]
                total_loss += self.classify_or_train(X, y, False)

            # Compute and store the average loss for this epoch
            losses[i] = total_loss/num_mini_batches

            # Compute and store the accuracy over the training dataset for this epoch
            assigned_labels = self.classify_or_train(training_dataset, None, True)
            accuracies[i] = helper.compute_overall_accuracy(training_labels, assigned_labels)

            # If this is the last epoch, store assigned_labels in
            # final_assigned_labels to compute the confusion matrix
            if i == (epochs - 1):
                final_assigned_labels = assigned_labels

        # Compute and print out the confusion matrix
        confusion_matrix = helper.compute_confusion_matrix(training_labels, final_assigned_labels, numClasses=3)
        print("Confusion Matrix:\n\n" + str(confusion_matrix) + "\n")
        print("Final Overall Accuracy on Training Dataset: " + str(accuracies[epochs-1]))

        # Make the plot of losses over each epoch
        loss_xCoordinates = np.arange(len(losses))
        loss_yCoordinates = losses

        fig_loss, ax_loss = plt.subplots(figsize = (10, 10))
        ax_loss.title.set_text('Loss Plot')
        ax_loss.set_xlabel('Loss')
        ax_loss.set_ylabel('Training Epoch')
        plt_loss.plot(loss_xCoordinates, loss_yCoordinates)
        plt_loss.show()

        # Make the plot of accuracies over each epoch
        accuracy_xCoordinates = np.arange(len(accuracies))
        accuracy_yCoordinates = accuracies

        fig_accuracy, ax_accuracy = plt.subplots(figsize = (10, 10))
        ax_accuracy.title.set_text('Accuracy Plot')
        ax_accuracy.set_xlabel('Accuracy')
        ax_accuracy.set_ylabel('Training Epoch')
        plt_accuracy.plot(accuracy_xCoordinates, accuracy_yCoordinates)
        plt_accuracy.show()


def Affine_Forward(A, W, b):
    Z = np.dot(A, W) + b.T
    acache = (A, W, b)
    return (Z, acache)


def Affine_Backward(dZ, cache):
    A = cache[0]
    W = cache[1]
    b = cache[2]

    dA = np.dot(dZ, W.T)
    dW = np.dot(A.T, dZ)
    db = np.sum(dZ, axis=0)
    return (dA, dW, db)


def ReLU_Forward(Z):
    A = np.maximum(Z, 0)
    rcache = Z
    return (A, rcache)


def ReLU_Backward(dA, cache):
    dZ = np.where(cache < 0, np.zeros(cache.shape), dA)
    return dZ


def Cross_Entropy(F, y):
    n = F.shape[0]

    # Compute the loss one operation at a time
    F_by_true_action_per_row = F[np.arange(F.shape[0]), y]
    exp_F = np.exp(F)
    row_sum_exp_F = np.sum(exp_F, axis=1)
    log_row_sum_exp_F = np.log(row_sum_exp_F)

    loss = -1*(np.sum(F_by_true_action_per_row - log_row_sum_exp_F))/n

    # Set up the indicator matrix for computing dF
    indicator_matrix = np.zeros(F.shape)
    indicator_matrix[np.arange(indicator_matrix.shape[0]), y] = 1.0

    dF = -1*(indicator_matrix - np.divide(exp_F.T, row_sum_exp_F).T)/n
    return (loss, dF)


"""
The scale_dataset function scales the training dataset.  It takes in the
n x 5 state matrix where n is the number of states in the training dataset
and each row represents a state.  It takes each column, subtracts its mean,
then divides by the standard deviation.
"""
def scale_dataset(states):
    (num_rows, num_columns) = states.shape
    scaled_states = np.zeros(states.shape)

    for col_index in range(0, num_columns):
        col_mean = np.mean(states[:, col_index])
        col_stdev = np.std(states[:, col_index])
        scaled_states[:, col_index] = (states[:, col_index] - col_mean)/col_stdev

    return scaled_states




"""
from Data import affine
from Data import relu
from Data import entropy

affine_Z_result, affine_acache = Affine_Forward(affine.A,affine.W,affine.b)
print("Affine_Forward Z result:\n\n")
print(np.allclose(affine_Z_result, affine.Z))

relu_A_result, relu_rcache = ReLU_Forward(affine_Z_result)
print("Relu_Forward A result:\n\n")
print(np.allclose(relu_A_result, relu.A))

loss_result, dF_result = Cross_Entropy(entropy.F, entropy.y)
print("Entropy results:\n\n")
print(np.allclose(loss_result, entropy.L))
print(np.allclose(dF_result, entropy.dF))

dZ_result = ReLU_Backward(relu.dA, relu_rcache)
print("ReLU_Backward A result:\n\n")
print(np.allclose(dZ_result, relu.dZ))

dA_result, dW_result, db_result = Affine_Backward(affine.dZ, affine_acache)
print("ReLU_Backward A result:\n\n")
print(np.allclose(dA_result, affine.dA))
print(np.allclose(dW_result, affine.dW))
print(np.allclose(db_result, affine.db))
"""
