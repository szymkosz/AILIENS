# Import the necessary libraries
import numpy as np
import helper
import matplotlib.pyplot as plt


"""
This is the driver function for training a perceptron with particular parameters
on the training data and then classifying the test data.
"""
def run_perceptron(training_data_tuple, test_data_tuple, learning_rate_exponent, epochs):
    # Extract the training and test data and labels
    training_data, training_data_by_class, training_labels = training_data_tuple
    test_data, test_data_by_class, test_labels = test_data_tuple

    # Initialize arrays for storing the training dataset
    # accuracies by epoch and test dataset accuracies
    training_epoch_accuracies = np.zeros((8, epochs))
    overall_accuracies = np.zeros((8,))

    # Create, train, and classify with all perceptrons of all 8 possible combinations
    # of having biases or not having them, initializing weights to zero or initializing
    # them randomly, and passing through the training examples in a fixed order or in a
    # random order
    for i in range(8):
        hasBias = ((i & 4) == 4)
        weightsAreRandom = ((i & 2) == 2)
        hasRandomTrainingOrder = ((i & 1) == 1)

        # Train and classify with perceptron
        perceptron = Perceptron(hasBias, weightsAreRandom)
        training_epoch_accuracies[i,:] = perceptron.train(training_data, training_labels, learning_rate_exponent, hasRandomTrainingOrder, epochs)
        assigned_labels = classify_test_data(perceptron, test_data, test_labels)

        overall_accuracies[i] = helper.compute_overall_accuracy(test_labels, assigned_labels)
        print("Overall Accuracy on Test Data Set: " + str(overall_accuracies[i]) + "\n")

        confusion_matrix = helper.compute_confusion_matrix(test_labels, assigned_labels)
        print("Confusion Matrix:\n")
        print(confusion_matrix)

    # Print all the test dataset accuracies
    print("Overall Accuracies on Test Data Set: " + str(overall_accuracies))

    # Initialize all the x-coordinates of all the points to be plotted
    epoch_indices = np.arange(epochs) + np.ones(epochs)

    for i in range(8):
        hasBias = ((i & 4) == 4)
        weightsAreRandom = ((i & 2) == 2)
        hasRandomTrainingOrder = ((i & 1) == 1)

        plot_label = "(hasBias, weightsAreRandom, hasRandomTrainingOrder) = ({0}, {1}, {2})".format(hasBias, weightsAreRandom, hasRandomTrainingOrder)
        #plot_label = "Has Bias = {0}, Weights Are Random = {1}, Has Random Training Order = {2}".format(hasBias, weightsAreRandom, hasRandomTrainingOrder)
        plt.plot(epoch_indices, training_epoch_accuracies[i,:], label=plot_label)

    plt.xlabel("Epoch")
    plt.ylabel("Training Accuracy")

    plt.title("Training Accuracy Vs. Epoch")
    plt.legend(loc="lower right", fontsize=6)

    # Save to file as PDF
    file_name = "Learning_Rate_Exponent={0},Epochs={1}.pdf".format(learning_rate_exponent, epochs)

    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(file_name) as pdf:
        pdf.savefig()

    #plt.show()


"""
This is the driver function for reproducing the best empirical results discovered
for either the differentiable or non-differentiable perceptron.
"""
def reproduce_best_results(training_data_tuple, test_data_tuple):
    # Set the parameters that produced the best test dataset accuracy
    learning_rate_exponent = 3
    hasBias = True
    weightsAreRandom = True
    hasRandomTrainingOrder = True
    epochs = 30

    print("Best learning_rate_exponent: " + str(learning_rate_exponent))
    print("Best number of epochs: " + str(epochs))

    # Extract the training and test data and labels, and construct the perceptron
    training_data, training_data_by_class, training_labels = training_data_tuple
    test_data, test_data_by_class, test_labels = test_data_tuple
    perceptron = Perceptron(hasBias, weightsAreRandom)

    # Train and classify with perceptron
    training_epoch_accuracies = perceptron.train(training_data, training_labels, learning_rate_exponent, hasRandomTrainingOrder, epochs)
    assigned_labels = classify_test_data(perceptron, test_data, test_labels)

    # Compute the perceptron's accuracy on the test dataset and print it
    overall_accuracy = helper.compute_overall_accuracy(test_labels, assigned_labels)
    print("Overall Accuracy on Test Data Set: " + str(overall_accuracy) + "\n")

    # Compute the perceptron's confusion matrix on the test dataset and print it
    confusion_matrix = helper.compute_confusion_matrix(test_labels, assigned_labels)
    print("Confusion Matrix:\n")
    print(confusion_matrix)

    # Plot the training curve
    epoch_indices = np.arange(epochs) + np.ones(epochs)
    plot_label = "(hasBias, weightsAreRandom, hasRandomTrainingOrder) = ({0}, {1}, {2})".format(hasBias, weightsAreRandom, hasRandomTrainingOrder)
    plt.plot(epoch_indices, training_epoch_accuracies, label=plot_label)

    # Set the axis labels, title, and legend
    plt.xlabel("Epoch")
    plt.ylabel("Training Accuracy")
    plt.title("Training Accuracy Vs. Epoch")
    plt.legend(loc="lower right", fontsize=8)

    # Save to file as PDF
    file_name = "Best_Perceptron_Training_Curve.pdf"

    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(file_name) as pdf:
        pdf.savefig()

    #plt.show()

    # For the extra credit, plot the learned
    # weight vectors of the perceptron
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

    The third parameter is used to determine if the perceptron uses the
    differentiable or non-differentiable learning rule.
    """
    def __init__(self, hasBias, hasRandomInitialization, isDifferentiable=False):
        # Store whether or not this is a differentiable perceptron
        self.isDifferentiable = isDifferentiable

        # Initialize weights
        np.random.seed(938)
        self.weights = None
        if hasRandomInitialization:
            self.weights = np.random.randn(10, 1024)
        else:
            self.weights = np.zeros((10, 1024))

        # Initialize biases, if they should be present
        self.biases = None
        if hasBias:
            if hasRandomInitialization:
                self.biases = np.random.randn(10)
            else:
                self.biases = np.zeros((10,))


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
            #print(self.biases)
            return np.argmax(np.dot(self.weights, image) + self.biases)
        else:
            return np.argmax(np.dot(self.weights, image))


    """
    Extra credit portion for Part 2:
    This function implements the differentiable perceptron learning rule. It returns
    the label assigned to the image.
    """
    def softmax(self, image):
        numerator = np.exp(np.dot(self.weights, image))
        denominator = np.sum(np.exp(np.dot(self.weights, image)), axis = 0)
        return numerator/denominator


    """
    The update_weights function will update the weights (and biases if present) of the
    perceptron given a training image, its true label, the label assigned to it by
    the perceptron, and a precomputed learning rate "eta".

    If the true and assigned labels are the same, nothing happens.  Otherwise, the
    product of eta and the training_image is computed.  Then this product is added
    to the weight vector for the true class and subtracted from the weight vector for the
    misclassified class.

    If the perceptron has biases, eta will be added to the bias of the true class
    and subtracted from the bias of the misclassified class.
    """
    def update_weights(self, training_image, true_label, assigned_label, eta):
        # If the true and assigned labels are identical, there is nothing further to do.
        if true_label == assigned_label:
            return

        # Computes the update vector for the weight
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
    Given a set of training images, their true labels, the exponent of the denominator in
    the learning-rate function, whether or not the images are passed over in random order, and the number of epochs,
    the train function trains the perceptron.
    """
    def train(self, training_data, training_labels, learning_rate_exponent, hasRandomTrainingOrder, epochs):
        accuracy_by_epoch = np.zeros(epochs)
        np.random.seed(7382)

        # Pass over the training data and train in multiple epochs
        for i in range(epochs):
            # Compute the learning rate for this epoch
            num_epoch = i+1
            eta = self.compute_learning_rate(num_epoch, learning_rate_exponent)

            # This numpy vector will control whether the training data is
            # passed over in fixed, sequential or random order.
            training_order = np.arange(len(training_labels))
            if hasRandomTrainingOrder:
                np.random.shuffle(training_order)

            curEpoch_assigned_labels = np.zeros(len(training_labels), dtype=np.int32)

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

            accuracy_by_epoch[i] = helper.compute_overall_accuracy(training_labels, curEpoch_assigned_labels)

        return accuracy_by_epoch


    """
    This function computes the learning rate for a given epoch according to the
    formula (1/(num_epoch**learning_rate_exponent)) where num_epoch is the number of the
    current epoch (always >=1) and learning_rate_exponent is the exponent of the denominator,
    decided when the program is run from the command line in main.py.
    """
    def compute_learning_rate(self, num_epoch, learning_rate_exponent):
        return (1 / (num_epoch**learning_rate_exponent))


    """
    This function plots the perceptron's weights for each digit class.  The weights are
    a 10 x 1,024 matrix where the ith row is the weight vector for the ith digit class.
    Each row is plotted as a 32 x 32 image in a similar vein to the plots from part 1.
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
            ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)

        fig = plt.figure()

        # Plot likelihoods of first digit in pair
        for i in range(len(self.weights)):
            if i + 1 == len(self.weights):
                ax = plt.subplot(4,3,i+2)
            else:
                ax = plt.subplot(4, 3, i+1)
            add_plot(ax, np.reshape(self.weights[i], (32,32)))
            plt.title("Class {0}".format(i))

        # plt.suptitle("Learned Perceptron Weights", fontsize=16)

        # Used for good spacing
        plt.tight_layout()

        ## Save to file as PDF
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages("Perceptron_Weights.pdf") as pdf:
            pdf.savefig()

        plt.show()


"""
This function takes in a perceptron, a test dataset, and the dataset's labels
and uses the perceptron to classify the test dataset.  The labels assigned by the
perceptron are then returned.
"""
def classify_test_data(perceptron, test_data, test_labels):
    num_test_images = test_data.shape[1]
    assigned_labels = np.zeros(num_test_images, dtype=np.int32)

    for i in range(num_test_images):
        assigned_labels[i] = perceptron.classify(test_data[:,i])

    return assigned_labels
