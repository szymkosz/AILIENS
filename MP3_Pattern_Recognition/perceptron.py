# Import the necessary libraries
import numpy as np
import helper
import matplotlib.pyplot as plt


"""
This is the driver function for training a perceptron with the training data
and then classifying the test data.
"""
def run_perceptron(training_data_tuple, test_data_tuple, learning_rate_power, hasBias, weightsAreRandom, hasRandomTrainingOrder, epochs):
    # Extract the training and test data and labels, and construct a perceptron
    training_data, training_data_by_class, training_labels = training_data_tuple
    test_data, test_data_by_class, test_labels = test_data_tuple
    perceptron = Perceptron(hasBias, weightsAreRandom)

    # Train and classify with perceptron
    perceptron.train(training_data, training_labels, learning_rate_power, hasRandomTrainingOrder, epochs)
    classify_test_data(perceptron, test_data, test_labels)
    #perceptron.plot_weights()

    perceptron.plot_weights()


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
            self.weights = np.random.randn((10, 1024))
        else:
            self.weights = np.zeros((10, 1024))

        # Initialize biases, if they should be present
        self.biases = None
        if hasBias:
            if hasRandomInitialization:
                self.biases = np.random.randn((10, 1))
            else:
                self.biases = np.zeros((10, 1))


    """
    The classify function assigns a label to an image.  This is accomplished with
    the following procedure:

    1.  The image, represented as a 1,024-dimensional numpy vector of its bitmap, is multiplied
        with the perceptron's 10 x 1,024 weight matrix to generate a 10-dimensional
        numpy vector.  If the perceptron has biases, they are then added to this result.

    2.  The index of the first occurrence of the largest value in the result
        from step 1 is computed with np.argmax.  This is the label that is
        returned by this function.
    """
    def classify(self, image):
        if self.biases is not None:
            return np.argmax(np.dot(self.weights, image) + self.biases)
        else:
            return np.argmax(np.dot(self.weights, image))


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
    def update_weights(self, training_image, true_label, assigned_label, eta):
        # If the true and assigned labels are identical, there is nothing further to do.
        if true_label == assigned_label:
            return

        # Computes the learning rate and the update vector for the weight
        # vectors of the true and misclassified classes
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
    def train(self, training_data, training_labels, learning_rate_power, hasRandomTrainingOrder, epochs):
        accuracy_by_epoch = np.zeros(epochs)

        # Pass over the training data and train in multiple epochs
        for i in range(epochs):
            # Compute the learning rate for this epoch
            num_epoch = i+1
            eta = compute_learning_rate(num_epoch, learning_rate_power)

            # This numpy vector will control whether the training data is
            # passed over in fixed, sequential or random order.
            training_order = np.arange(len(training_labels))
            if hasRandomTrainingOrder:
                training_order = np.random.shuffle(training_order)

            curEpoch_assigned_labels = np.zeros(len(training_labels))

            # Pass over the training images in the determined order, classifying
            # them and then updating the perceptron's weights and biases
            for j in range(len(training_order)):
                # Identify the training image and its corresponding label for this iteration
                training_image_index = training_order[j]
                training_image = training_data[:,training_image_index]
                training_label = training_labels[training_image_index]

                # Classify the image and then update the perceptron's weights and biases
                assigned_label = self.classify(training_image)
                curEpoch_assigned_labels[training_image_index] = assigned_label
                self.update_weights(training_image, training_label, assigned_label, eta)

            accuracy_by_epoch[i] = np.sum(np.equal(training_labels, curEpoch_assigned_labels))

        print("Accuracy By Epoch: " + str(accuracy_by_epoch))


    def compute_learning_rate(num_epoch, learning_rate_power):
        return (1 / (num_epoch**learning_rate_power))


    """
    This function plots the perceptron's weights for each digit class.  The weights are
    a 10 x 1,024 matrix where the ith row is the weight vector for the ith digit class.
    Each row should be plotted as a 32 x 32 image in a similar vein to the log odds ratio plots.
    """
    def plot_weights(self):
        # Plot self.weights
        def add_plot(ax, dataset):

            ## Overhead to make colorbar work
            from mpl_toolkits.axes_grid1 import make_axes_locatable

            divider = make_axes_locatable(ax)

            ax_cb = divider.new_horizontal(size="10%", pad=0.05)
            fig1 = ax.get_figure()
            fig1.add_axes(ax_cb)

            ## Heat map
            im = ax.imshow(dataset, cmap='jet')

            ## Turn off axis labels and tick marks
            ax.tick_params(
                axis='both',
                which='both',
                bottom=False,
                left=False,
                labelbottom=False,
                labelleft=False)

            plt.colorbar(im, cax=ax_cb)
            ax_cb.yaxis.tick_right()
            ax_cb.yaxis.set_tick_params(labelright=True)

        fig = plt.figure()

        # Plot likelihoods of first digit in pair
        for i in range(len(self.weights)):
            ax = plt.subplot(4, 3, i+1)
            add_plot(ax, np.reshape(self.weights[i], (32,32)))

        # Used for good spacing
        plt.tight_layout()

        ## Save to file as PDF
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages("Perceptron_Weights.pdf") as pdf:
            pdf.savefig()

        plt.show()


#### Miscellaneous functions
def classify_test_data(perceptron, test_data, test_labels):
    num_test_images = test_data.shape[1]
    assigned_labels = np.zeros(num_test_images)

    for i in range(num_test_images):
        assigned_labels[i] = perceptron.classify(test_data[:,i])

    overall_accuracy = helper.compute_overall_accuracy(test_labels, assigned_labels)
    print("Overall Accuracy on Test Data Set: " + str(overall_accuracy))

    confusion_matrix = helper.compute_confusion_matrix(test_labels, assigned_labels)
    print("Confusion Matrix:\n")
    print(confusion_matrix)
