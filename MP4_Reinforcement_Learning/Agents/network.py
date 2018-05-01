# Import the necessary libraries
from Agents.agent import Agent
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import helper
import loader

# CONSTANTS
NAME = "NETWORK"
NUM_STATE_ATTRIBUTES = 5        # Number of attributes to represent game state
NUM_UNITS_IN_LAST_LAYER = 3     # Number of actions that can be picked


class network(Agent):
    def __init__(self, num_layers=4, num_units_per_layer=256, learning_rate=0.1, weight_scale_parameter=(1.0/256), playerNum=1):
        # Initialize seed before random weight initialization for consistent results
        np.random.seed(7383)
        super().__init__(NAME, playerNum)

        # Save the number of layers, number of units per layer (except the last layer, which is 3 units)
        self.num_layers = num_layers
        self.num_units_per_layer = num_units_per_layer
        self.learning_rate = learning_rate

        # Randomly initialize weight matrices with a uniform distribution multiplied by a scaling factor
        self.weights = None
        if(num_layers == 1):
            # If there is only one layer, there is a single NUM_STATE_ATTRIBUTES x NUM_UNITS_IN_LAST_LAYER weight matrix
            self.weights = [(weight_scale_parameter * np.random.rand(NUM_STATE_ATTRIBUTES, NUM_UNITS_IN_LAST_LAYER))]
        else:
            # The first weight matrix is NUM_STATE_ATTRIBUTES x num_units_per_layer, the last weight matrix is
            # num_units_per_layer x NUM_UNITS_IN_LAST_LAYER, and every weight matrix in between is
            # num_units_per_layer x num_units_per_layer.
            self.weights = [weight_scale_parameter * np.random.rand(NUM_STATE_ATTRIBUTES, num_units_per_layer)]
            self.weights += [(weight_scale_parameter * np.random.rand(num_units_per_layer, num_units_per_layer)) for i in range(num_layers-2)]
            self.weights.append( (weight_scale_parameter * np.random.rand(num_units_per_layer, NUM_UNITS_IN_LAST_LAYER)) )

        # Initialize bias vectors to zero
        self.biases = [np.zeros(num_units_per_layer) for i in range(num_layers-1)]
        self.biases.append(np.zeros(NUM_UNITS_IN_LAST_LAYER))

        # Set up lists for the affine and ReLU caches of each layer
        self.affine_caches = [(None, None, None) for i in range(num_layers)] # Of the form (A_i, W_i, b_i) for the ith layer
        self.relu_caches = [None for i in range(num_layers-1)] # Last layer doesn't use ReLU, so only
                                                               # first num_layers - 1 have ReLU caches

        # Save the means and standard deviations of the columns of the training dataset
        self.training_dataset_means = np.zeros(5)
        self.training_dataset_stdevs = np.zeros(5)


    """
    The getAction function should decide the action this agent should take
    given the current state s of the game.  It should return 0 if the paddle
    should move up, 2 if the paddle should move down, or 1 if the paddle should
    do nothing.

    The "is_training" parameter isn't used here.
    """
    def getAction(self, is_training, cur_state_tuple):
        # Scale the current state with the means and standard deviations of
        # the training dataset before passing it in to the neural network
        scaled_input_state = np.zeros((1,5))
        for i in range(NUM_STATE_ATTRIBUTES):
            col_mean = self.training_dataset_means[i]
            col_stdev = self.training_dataset_stdevs[i]
            scaled_input_state[0, i] = (cur_state_tuple[i] - col_mean)/col_stdev

        action = self.classify_or_train(scaled_input_state, None, True)[0]
        return action


    # Handle feedforward
    def feedforward(self, X):
        # Set the layer input matrix A to X initially and initialize F
        A = X
        F = None

        # Feed the minibatch forward through the neural network
        for i in range(self.num_layers):
            # Get the weight matrix and bias vector for this layer
            W = self.weights[i]
            b = self.biases[i]

            # Compute the input matrix to the next layer or the
            # output of the network if this is the final layer
            if i < (self.num_layers - 1):
                # Do an affine transformation followed by ReLU
                # and pass the output onto the next layer
                Z, self.affine_caches[i] = Affine_Forward(A, W, b)
                A, self.relu_caches[i] = ReLU_Forward(Z)
            else:
                # Compute the output of the network.  Note that the
                # last layer doesn't have a ReLU function call.
                F, self.affine_caches[i] = Affine_Forward(A,W,b)

        return F


    # Handle backpropagation
    def backpropagation(self, F, y):
        # Compute cross-entropy loss and dF's
        loss, dF = Cross_Entropy(F, y)
        dZ = dF

        # Compute dW's and db's and perform gradient descent starting at
        # the end of the network and backpropagating to the beginning
        for i in range(self.num_layers - 1, -1, -1):
            # Get the affine cache that was generated by this layer
            # and compute dA's, dW's, and db's for this layer
            acache = self.affine_caches[i]
            dA, dW, db = Affine_Backward(dZ, acache)

            # Do gradient descent update for this layer
            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * db

            # If this is not the final layer, backpropagate
            # through ReLU to the next layer
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
        # Feed minibatch X forward through the network to compute F
        F = self.feedforward(X)

        # If this is the test phase, assign actions to the states and return them
        if test:
            classifications = np.argmax(F, axis=1)
            return classifications

        # Compute loss over this minibatch and perform gradient descent updates
        loss = self.backpropagation(F, y)
        return loss


    """
    The scale_dataset function scales the training dataset.  It takes in the
    n x 5 state matrix where n is the number of states in the training dataset
    and each row represents a state.  It takes each column, subtracts its mean,
    then divides by the standard deviation.  It also stores each mean and standard
    deviation so that during the test games, the game state can be scaled
    properly before getting passed through the neural network.
    """
    def scale_dataset(self, states):
        (num_rows, num_columns) = states.shape
        scaled_states = np.zeros(states.shape)

        # Scale each column and store each column's mean and standard deviation
        for col_index in range(0, num_columns):
            col_mean = np.mean(states[:, col_index])
            col_stdev = np.std(states[:, col_index])
            scaled_states[:, col_index] = (states[:, col_index] - col_mean)/col_stdev

            self.training_dataset_means[col_index] = col_mean
            self.training_dataset_stdevs[col_index] = col_stdev

        return scaled_states


    """
    The MinibatchGD function runs the minibatch gradient descent algorithm given
    the expert policy dataset, number of epochs, and size of each minibatch.

    The parameter "data" is the output of the parser function in loader.py.  See
    the documentation for parser in loader.py for more information.
    """
    def MinibatchGD(self, data, epochs=300, mini_batch_size=128):
        # Initialize seed before shuffling training data for consistent results
        np.random.seed(3489)

        # Extract the training dataset and labels and scale the dataset
        training_dataset = data[0]
        scaled_dataset = self.scale_dataset(training_dataset)
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
            print("Epoch: " + str(i))
            # Shuffle the training data by making a vector of
            # row indices of training vectors and shuffling it
            row_indices = np.arange(n)
            np.random.shuffle(row_indices)

            # Sums up the loss over every minibatch for making the loss plot
            total_loss = 0

            for j in range(num_mini_batches):
                # Extract the indices of the training vectors of this mini-batch
                beginning_index = (j*mini_batch_size)
                ending_index = min((j+1)*mini_batch_size, n)
                mini_batch_row_indices = row_indices[beginning_index:ending_index]

                # Extract the training vectors of this minibatch and their
                # labels and propagate them through the network for training
                X = scaled_dataset[mini_batch_row_indices, :]
                y = training_labels[mini_batch_row_indices]
                total_loss += self.classify_or_train(X, y, False)

            # Compute and store the average loss for this epoch
            losses[i] = total_loss/num_mini_batches

            # Compute and store the accuracy over the scaled training dataset for this epoch
            assigned_labels = self.classify_or_train(scaled_dataset, None, True)
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
        loss_xCoordinates = np.arange(len(losses)) + np.ones(len(losses))
        loss_yCoordinates = losses

        fig_loss, ax_loss = plt.subplots(figsize = (10, 10))
        ax_loss.title.set_text('Loss Plot')
        ax_loss.set_xlabel('Training Epoch')
        ax_loss.set_ylabel('Loss')
        plt.plot(loss_xCoordinates, loss_yCoordinates)
        plt.show()

        # Make the plot of accuracies over each epoch
        accuracy_xCoordinates = np.arange(len(accuracies)) + np.ones(len(accuracies))
        accuracy_yCoordinates = accuracies

        fig_accuracy, ax_accuracy = plt.subplots(figsize = (10, 10))
        ax_accuracy.title.set_text('Accuracy Plot')
        ax_accuracy.set_xlabel('Training Epoch')
        ax_accuracy.set_ylabel('Accuracy')
        plt.plot(accuracy_xCoordinates, accuracy_yCoordinates)
        plt.show()


    def save_network(self):
        loader.save_training_results_to_file(self.num_layers, self.num_units_per_layer, self.learning_rate,
                                      self.weights, self.biases, self.training_dataset_means,
                                      self.training_dataset_stdevs)


    def load_network(self):
        self.num_layers, self.num_units_per_layer, self.learning_rate, self.weights, self.biases, \
        self.training_dataset_means, self.training_dataset_stdevs = loader.load_training_results_from_file()

        self.affine_caches = [(None, None, None) for i in range(self.num_layers)]
        self.relu_caches = [None for i in range(self.num_layers-1)]


"""
THE FIVE NEURAL NETWORK FUNCTIONS DESCRIBED IN THE ASSIGNMENT FOLLOW!
"""
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
