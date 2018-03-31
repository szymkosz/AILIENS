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
    pass

"""
Use maximum-a-posteriori (MAP) to assign labels to the test data given likelihoods
and priors probabilities (i.e. compute the sums over all 10 classes and assign the label
that corresponds to the maximum sum)

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
    pass


"""
Computes the confusion matrix given the true labels of the test images and
their assigned labels.
"""
def compute_confusion_matrix(true_labels, assigned_labels):
    pass


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
    pass


def find_maximum_confusion_class_pairs(confusion):
    pass

"""
Plots the log likelihood maps and log odds ratio maps for the four pairs of digits
with the highest confusion rates.
"""
def odds_ratios(likelihoods, digit_pair):
    pass

def make_plots(likelihoods, digit_pair):
    pass
