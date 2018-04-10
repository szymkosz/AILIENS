# Import the necessary files and libraries
import numpy as np
import matplotlib.pyplot as plt
import helper

# Values of .1 to .5 and 5.2 to 6.4 for the laplacian constant yield the best overall
# accuracy on the test data set.  Digits 7 and 8 have 100% accuracy for values from .1 to .5
# and digits 0 and 8 have 100% accuracy for values from 5.2 to 6.4.

"""
This is the driver function for training a naive bayes classifier with the training data
and then classifying the test data.
"""
def run_naivebayes(training_data_tuple, test_data_tuple, laplace):
    print_min_max_tokens = True    ## Flag to print out the min and max posterior prob tokens to std out

    print("\n\n\nLaplacian Constant: ", laplace)

    training_data, training_data_by_class, training_labels = training_data_tuple
    test_data, test_data_by_class, test_labels = test_data_tuple

    likelihoods = compute_likelihoods(training_data_by_class, laplace)
    priors = compute_priors(training_data, training_data_by_class)
    assigned_labels, posteriors = maximum_a_posteriori(test_data, likelihoods, priors)

    overall_accuracy = helper.compute_overall_accuracy(test_labels, assigned_labels)
    print("Overall Accuracy on Test Data Set: " + str(overall_accuracy))

    confusion_matrix = helper.compute_confusion_matrix(test_labels, assigned_labels, posteriors.shape[0])
    print("Confusion Matrix:\n")
    print(confusion_matrix)
    print("")

    max_and_min_image_indices = max_and_min_posteriors(posteriors, test_data, test_labels)

    if print_min_max_tokens:
        for i in range(posteriors.shape[0]):
            curMax_index = max_and_min_image_indices[i, 0]
            curMin_index = max_and_min_image_indices[i, 1]

            max_image = test_data[:,curMax_index]
            print("Class %d maximum posterior test token:\n" % i)
            helper.print_image(max_image)
            print("")

            min_image = test_data[:,curMin_index]
            print("Class %d minimum posterior test token:\n" % i)
            helper.print_image(min_image)
            print("")

    digit_pairs = find_maximum_confusion_class_pairs(confusion_matrix)
    odds_ratios(likelihoods, digit_pairs)


"""
Computes the likelihoods of each pixel given each class and returns them as a
1024 x 10 numpy array where the jth column contains the likelihoods for the jth
class.
"""
def compute_likelihoods(images_by_class, laplace):
    likelihoods = np.empty((0,images_by_class[0].shape[0]))

    for k in range(len(images_by_class)):
        curImages = images_by_class[k]
        num_pixels = curImages.shape[0]
        num_class_images = curImages.shape[1]

        curLikelihoods = np.zeros(num_pixels)

        # Computes P(F(i/32,i%32) = 1 | class = k) over all 1,024 pixels for the current class k
        for i in range(num_pixels):
            num_observations = np.sum(curImages[i,:])
            curLikelihoods[i] = (num_observations + laplace) / (num_class_images + (2*laplace))

        likelihoods = np.vstack((likelihoods, curLikelihoods))

    likelihoods = likelihoods.T

    return likelihoods


"""
Computes the priors probabilites and returns them as a 10-dimensional numpy vector
where the ith entry is the priors probability for the ith class.
"""
def compute_priors(training_data, images_by_class):
    numClasses = len(images_by_class)
    priors = np.zeros(numClasses)
    num_training_images = training_data.shape[1]
    for i in range(numClasses):
        images_in_class = (images_by_class[i]).shape[1]
        priors[i] = images_in_class/num_training_images
    return priors


"""
Use maximum-a-posteriori (MAP) to assign labels to the test data given likelihoods
and priors probabilities (i.e. compute the sums over all 10 classes and assign the label
that corresponds to the maximum sum).

The test_data matrix has dimensions 1,024 x T where T is the total number of test images
and each column corresponds to the bitmap of a single test image.  The likelihoods are
a 1,024 x 10 numpy matrix where the entry in row i and column j is P(F(i/32, i%32) = 1 | class = j).
The priors are a 10-dimensional numpy array where the ith entry corresponds to P(class = i).

Returns a 2-tuple of the assigned labels for all test images and all the posterior probabilities
for each image in each class.  The details of the returned tuple are as follows:

assigned_labels:    Let T be the total number of test images.
(0th entry)         Then this entry is a 1D numpy array containing all T assigned labels.
                    The ith entry is the assigned label for the ith test image.

posteriors:         Let T be the total number of test images.
(1th entry)         Then this entry is a 10 x T numpy array where the ith row corresponds
                    to the ith class and the jth column contains the posterior probabilities
                    for the jth test image.
"""
def maximum_a_posteriori(test_data, likelihoods, priors):
    # Since the given likelihoods are P(Fij = 1 | class = k),
    # the likelihoods P(Fij = 0 | class = k) must be computed.
    opposite_likelihoods = (np.ones(likelihoods.shape) - likelihoods)

    posteriors = np.empty((0,likelihoods.shape[1]))
    num_test_images = test_data.shape[1]
    assigned_labels = np.zeros(num_test_images, dtype=np.int32)
    log_priors = np.log(priors)

    for i in range(num_test_images):
        # To get the likelihoods for this image, it is necessary to identify
        # the pixels set to 0 and the pixels set to 1 and then index the corresponding
        # rows of the corresponding likelihood matrices.
        curImage = test_data[:,i]
        indices_with_ones = np.equal(curImage, np.ones(curImage.shape))
        indices_with_zeros = np.equal(curImage, np.zeros(curImage.shape))

        # The likelihoods for this image are assembled by initializing a matrix of zeros,
        # adding the likelihoods P(F(i/32, i%32) = 1 | class = j) to the rows where pixel
        # (i/32, i%32) is set to 1 and adding the likelihoods P(F(i/32, i%32) = 0 | class = j) to the rows
        # where pixel (i/32, i%32) is set to 0.
        curImageLikelihoods = np.zeros(likelihoods.shape)
        curImageLikelihoods[indices_with_ones,:] = likelihoods[indices_with_ones,:]
        curImageLikelihoods[indices_with_zeros,:] = opposite_likelihoods[indices_with_zeros,:]

        # Compute the log sum
        curImage_log_likelihoods = np.log(curImageLikelihoods)
        curImagePosteriors = np.sum(curImage_log_likelihoods,axis=0) + log_priors
        posteriors = np.vstack((posteriors, curImagePosteriors))

        # Assign the class label based on the index of the highest posterior probability
        curImage_assigned_label = np.argmax(curImagePosteriors)
        assigned_labels[i] = curImage_assigned_label

    posteriors = posteriors.T

    return (assigned_labels, posteriors)


"""
Returns a 10 x 2 matrix of the column indices of the max and min posterior
probabilites within each class.

More precisely, the ith row contains the column indices of the test images
with the highest and lowest posterior probabilites for the ith class.  The first
column contains the column indices of the test images with the maximum posterior
probabilites, and the second column contains the column indices of the test images
with the minimum posterior probabilites.
"""
def max_and_min_posteriors(posteriors, test_data, true_labels):
    numClasses = posteriors.shape[0]
    max_min_post = np.zeros((numClasses , 2), dtype=np.int32)

    for i in range(numClasses):
        # Subset the class
        cur_idxs = np.asarray(np.where(true_labels == i))
        cur_idxs = cur_idxs.reshape((len(cur_idxs[0]),1))
        cur_posteriors = posteriors[i,cur_idxs]

        # Find the max and min indices within subset
        min_idx = np.argmin(cur_posteriors)
        max_idx = np.argmax(cur_posteriors)

        # Retrieve original indices (in range T)
        min_idx = cur_idxs[min_idx]
        max_idx = cur_idxs[max_idx]

        # Populate max_min_post array
        max_min_post[i,0] = max_idx
        max_min_post[i,1] = min_idx

    return max_min_post


"""
This function returns a list of four tuples, each tuple representing a pair of
digit types with the highest confusion rates, given the confusion matrix.  Each
tuple (i,j) represents the ith row and jth column of one of the 4 highest
confusion rates.

The diagonal entries of the confusion matrix are not considered.
"""
def find_maximum_confusion_class_pairs(confusion):
    number_of_pairs = 4

    if number_of_pairs > len(confusion):
        number_of_pairs = len(confusion)

    pairs = []

    # Assume square matrix
    n = len(confusion)
    flat_confusion = confusion.reshape(n*n,)

    ## Expecting the diagonal entries to have the top n max values
    num_values = number_of_pairs + n

    # Extract the flattened indices of the top n + number_of_pairs entries
    max_idx = np.argpartition(flat_confusion, -(num_values))[-(num_values):]

    # Sort them
    max_idx = max_idx[np.argsort(flat_confusion[max_idx])]

    # Extract the x and y coordinates
    pairs_idx = np.unravel_index(max_idx, confusion.shape) # 2-tuple of two arrays of x and y coordinates

    # Go through every returned index
    for i in reversed(range(num_values)):
        x = pairs_idx[0][i]
        y = pairs_idx[1][i]

        # If x == y, this entry is along the diagonal. Skip it.
        if x != y:
            pairs.append( (x, y) )

            if len(pairs) == number_of_pairs:
                break

    return pairs


"""
Plots the log likelihood maps and log odds ratio maps for the four pairs of digits
with the highest confusion rates
"""
def odds_ratios(likelihoods, digit_pairs):

    # Iterate over all digit pairs
    for pair in digit_pairs:
        # Call helper function to plot likelihoods of each
        #  digit in each pair and their respective odds ratio
        make_plots(likelihoods, pair)


"""
Helper function for plotting the log likelihoods and log odds ratios maps for a
single digit pair.
"""
def make_plots(likelihoods, digit_pair):
    if likelihoods.shape[0] == 1024:
        dims = (32, 32)
    else:
        dims = (70, 60)
    # Extract relevant likelihoods for this pair
    first_likelihoods = np.reshape(likelihoods[:,digit_pair[0]],dims)
    second_likelihoods = np.reshape(likelihoods[:,digit_pair[1]],dims)

    # Convert to log
    first_likelihoods = np.log(first_likelihoods)
    second_likelihoods = np.log(second_likelihoods)

    # odds_ratios = np.divide(second_likelihoods,first_likelihoods)
    odds_ratios = first_likelihoods - second_likelihoods

    # odds_ratios = np.log(odds_ratios)

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
    ax = plt.subplot(1,3,1)
    add_plot(ax, first_likelihoods)

    # Plot likelihoods of second digit in pair
    ax = plt.subplot(1,3,2)
    add_plot(ax, second_likelihoods)

    # Plot odds ratios for pair
    ax = plt.subplot(1,3,3)
    add_plot(ax, odds_ratios)

    # Used for good spacing
    plt.tight_layout()

    ## Save to file as PDF
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages("Confusion Pair ({0}, {1}).pdf".format(digit_pair[0], digit_pair[1])) as pdf:
        pdf.savefig()

    #plt.show()
