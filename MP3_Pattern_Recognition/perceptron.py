# Import the necessary libraries
import numpy as np


class Perceptron(object):
    """
    This is the constructor for the perceptron.  It constructs the weights and biases
    (if it should have biases) and either initializes all of them randomly or to 0.
    If they are initialized randomly, their values are pulled from a standard normal
    distribution with mean 0 and variance 1.

    The weights are represented as a 10 x 1,024 numpy matrix.  The ith row of this
    matrix represents the weight vector for the ith class.

    The biases are represented as a 10-dimensional numpy vector.  They are stored
    separately from the weight matrix to make the code simpler, but the math is
    identical.  If there are no biases, they are set to a Nonetype.
    """
    def __init__(self, hasBias, hasRandomInitialization):
        # Initialize weights
        self.weights = None
        if hasRandomInitialization:
            self.weights = np.random.randn(10, 1024)
        else:
            self.weights = np.zeros(10, 1024)

        # Initialize biases, if they should be present
        self.biases = None
        if hasBias:
            if hasRandomInitialization:
                self.biases = np.random.randn(10, 1)
            else:
                self.biases = np.zeros(10, 1)


    """
    The classify function assigns a label to an image.  This is accomplished with
    the following procedure:

    1.  The image, represented as a 1,024-dimensional numpy vector of its bitmap, is multiplied
        with the perceptron's 10 x 1,024 weight matrix to generate a 10-dimensional
        numpy vector.  If the perceptron has biases, they are then added to this result.

    2.  The result of step 1 is then passed into np.sign (numpy's signum function)
        to generate the activations of the 10 neurons in the form of a 10-dimensional
        numpy vector.  This is the non-differentiable activation function from lecture.

    3.  The index of the first occurrence of the largest value in the result
        from step 2 is computed with np.argmax.  This is the label that is
        returned by this function.
    """
    def classify(self, image):
        # Compute the activations of the neurons
        activations = None
        if self.biases is not None:
            activations = np.sign(np.dot(self.weights, image) + self.biases)
        else:
            activations = np.sign(np.dot(self.weights, image))

        # Return the index of the first occurrence of the largest activation
        return np.argmax(activations)


    """
    The update_weights function will update the weights (and biases if present) of the
    perceptron given a training image, its true label, the label assigned to it by
    the perceptron, a function for computing the learning rate, and the number of the training
    training image within an epoch for computing the learning rate.

    If the true and assigned labels are the same, nothing happens.  Otherwise, a learning rate
    "eta" and the product of eta and the training_image are computed.  Then this product is added
    to the weight vector for the true class and subtracted from the weight vector for the
    misclassified class.
    """
    def update_weights(self, training_image, true_label, assigned_label, learning_rate_decay_function, num_training_image):
        # If the true and assigned labels are identical, there is nothing further to do.
        if true_label == assigned_label:
            return

        # Computes the learning rate and the update vector for the weight
        # vectors of the true and misclassified classes
        eta = learning_rate_decay_function(num_training_image)
        update = eta * training_image

        # Update the weight vectors of the true and misclassified classes
        self.weights[true_label, :] += update.T
        self.weights[assigned_label, :] -= update.T

        # If there are biases, updating them is equivalent to adding eta
        # to the bias of the true class and subtracting eta from the bias of the
        # misclassified class.
        if self.biases is not None:
            self.biases[true_label] += eta
            self.biases[assigned_label] -= eta


    """
    Given a set of training images, their true labels, a function to compute learning rates,
    whether or not the images are passed over in random order, and the number of epochs,
    the train function trains the perceptron.
    """
    def train(self, training_data, training_labels, learning_rate_decay_function, hasRandomTrainingOrder, epochs):
        # Pass over the training data and train in multiple epochs
        for i in range(epochs):
            # This numpy vector will control whether the training data is
            # passed over in fixed, sequential or random order.
            training_order = np.arange(len(training_labels))
            if hasRandomTrainingOrder:
                training_order = np.random.shuffle(training_order)

            # Pass over the training images in the determined order, classifying
            # them and then updating the perceptron's weights and biases
            for j in range(len(training_order)):
                # Identify the training image and its corresponding label for this iteration
                training_image_index = training_order[j]
                training_image = training_data[:,training_image_index]
                training_label = training_labels[training_image_index]

                # Classify the image and then update the perceptron's weights and biases
                assigned_label = self.classify(training_image)
                self.update_weights(training_image, training_label, assigned_label, learning_rate_decay_function, j+1)


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def compute_learning_rate(num_training_image):
    return (1 / num_training_image)
