import numpy as np

"""
Computes the likelihoods of each pixel given each class and returns them as a
1024 x 10 numpy array where the jth column contains the likelihoods for the jth
class.
"""
def compute_likelihoods(images_by_class, laplace):
    likelihoods = np.empty((0,1024))

    for k in range(len(images_by_class)):
        curImages = images_by_class[k]
        num_class_images = curImages.shape[1]

        curLikelihoods = []

        for i in range(curImages.shape[0]):
            num_observations = np.sum(curImages[i,:])

            likelihood = (num_observations + laplace) / (num_class_images + (2*laplace))
            curLikelihoods.append(likelihood)

        curLikelihoods = np.asarray(curLikelihoods)
        likelihoods = np.vstack((likelihoods, curLikelihoods))

    likelihoods = likelihoods.T

    return likelihoods


"""
Computes the priors probabilites and returns them as a 10-dimensional numpy vector
where the ith entry is the priors probability for the ith class.
"""
def compute_priors(training_data, images_by_class):
    priors = np.zeros(10)
    num_training_images = len(training_data)
    for i in range(10):
        images_in_class = len(images_by_class[i])
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

    posteriors = np.empty((0,10))
    assigned_labels = []
    num_test_images = test_data.shape[1]
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
        curImagePosteriors = np.sum(curImage_log_likelihoods,axis=1) + log_priors
        posteriors = np.vstack((posteriors, curImagePosteriors))

        # Assign the class label based on the index of the highest posterior probability
        curImage_assigned_label = np.argmax(curImagePosteriors)
        assigned_labels.append(curImage_assigned_label)

    assigned_labels = np.asarray(assigned_labels)
    posteriors = posteriors.T

    return (assigned_labels, posteriors)

"""
Computes the confusion matrix given the true labels of the test images and
their assigned labels.
"""
def compute_confusion_matrix(true_labels, assigned_labels):
    confusion = np.zeros((len(true_labels),len(assigned_labels)))
    for i in range(len(true_labels)):
        for j in range(len(assigned_labels)):
            confusion[ true_labels[i] , assigned_labels[j] ] += 1

    for i in range(len(confusion)):
        confusion[i,:] /= np.sum(confusion[i,:])

    return confusion


"""
Returns a 10 x 2 matrix of the column indices of the max and min posterior
probabilites within each class.

More precisely, the ith row contains the column indices of the test images
with the highest and lowest posterior probabilites for the ith class.  The first
column contains the column indices of the test images with the maximum posterior
probabilites, and the second column contains the column indices of the test images
with the minimum posterior probabilites.
"""
def max_and_min_posteriors(posteriors):
    max_min_post = np.zeros((10,2))
    max_min_post[:,0] = np.argmax(posteriors, axis=1)
    max_min_post[:,1] = np.argmin(posteriors, axis=1)

    return max_min_post


def find_maximum_confusion_class_pairs(confusion):
    number_of_pairs = 4
    pairs = []

    # Assume square matrix
    n = len(confusion)
    flat_confusion = confusion.reshape(n*n,)

    ## Expecting the diagonal entries to have the top n max values
    num_values = number_of_pairs + n

    # Extract the flattened indices of the top n + number_of_pairs entries
    max_idx = np.argpartition(flat_confusion, -(num_values))[-(num_values):]

    # Sort them
    max_idx = max_idx[np.argsort(flat_confusion[ind])]

    # Extract the x and y coordinates
    pairs_idx = np.unravel_index(max_idx, confusion.shape) # 2-tuple of two arrays of x and y coordinates

    # Go through every returned index
    for i in reversed(range(num_values)):
        x = pairs_idx[0][i]
        y = pairs_idx[1][i]

        # If x == y, this entry is along the diagonal. Skip it.
        if x != y and len(pairs) != number_of_pairs:
            pairs.append( (x, y) )

    return pairs


"""
Plots the log likelihood maps and log odds ratio maps for the four pairs of digits
with the highest confusion rates.
"""
def odds_ratios(likelihoods, digit_pair):
    pass

def make_plots(likelihoods, digit_pair):
    pass
