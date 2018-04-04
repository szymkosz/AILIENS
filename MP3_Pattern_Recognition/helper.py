# Import the necessary libraries
import numpy as np

"""
HELPER FUNCTIONS GO IN THIS FILE!
"""

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
Computes the overall accuracy on a test dataset given a numpy vector of the true
labels of the test images and a numpy vector of their assigned labels
"""
def compute_overall_accuracy(true_labels, assigned_labels):
    assert len(true_labels) == len(assigned_labels), "LENGTH NOT SAME ERROR: true labels " + \
                                                     "and assigned labels don't have same length!"
    return (np.sum(np.equal(true_labels, assigned_labels)) / len(true_labels))
