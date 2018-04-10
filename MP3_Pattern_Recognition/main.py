"""
-------------------------------------------------------------------------------
This is the driver file for training a naive bayes classifier or perceptron with the training data
and then classifying the test data.

To train and classify with a naive bayes classifier and a particular laplacian smoothing constant,
run the following command:

python main.py <bayes> <laplace> <face>

where:
<bayes>     = "bayes" or "naivebayes" (ignoring case)
<laplace>   = The laplacian smoothing constant to use for computing the likelihoods
<face>      = "face" (ignoring case) if the face data should be used.  Omit this
            : argument to use the digit data.


To train and classify with a perceptron (differentiable or non-differentiable)
with particular parameters, run the following command:

python main.py <perceptron> <differentiable> <learning_rate_power> <epochs>

where:
<perceptron>                = "perceptron" (ignoring case)
<differentiable>            = "differentiable" (ignoring case) if the differentiable
                            : perceptron should be used.  Omit this argument if
                            : the non-differentiable perceptron should be used.
<learning_rate_power>       = The value of the exponent in the learning rate function (1/(num_epoch**learning_rate_power))
<epochs>                    = number of epochs (passes) over the training data during the training phase


To reproduce the best empirical results discovered for either the differentiable or
non-differentiable perceptron, run the following command:

python main.py <perceptron> <differentiable> <best>

where:
<perceptron>                = "perceptron" (ignoring case)
<differentiable>            = "differentiable" (ignoring case) if the differentiable
                            : perceptron should be used.  Omit this argument if
                            : the non-differentiable perceptron should be used.
<best>                      = "best" (ignoring case)
-------------------------------------------------------------------------------
"""

#import numpy as np
import sys
from loader import parser
from loader import face_parser
import naivebayes
import perceptron

if __name__ == "__main__":
    """
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
                        + "\"python %s <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>\"" % sys.argv[0]
    """
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
                        + "\"python %s <perceptron> <learning_rate_power> <epochs>\"" % sys.argv[0]

    assert len(sys.argv) >= 3, incorrectUsageError

    face = False

    try:
        if sys.argv[3].lower() == "face":
            face = True
    except:
        face = False


    training_data_filename = "Data/digitdata/optdigits-orig_train.txt"
    test_data_filename = "Data/digitdata/optdigits-orig_test.txt"

    face_training_data_filename = "Data/facedata/facedatatrain.txt"
    face_training_data_labels_filename = "Data/facedata/facedatatrainlabels.txt"
    face_testing_data_filename = "Data/facedata/facedatatest.txt"
    face_testing_data_labels_filename = "Data/facedata/facedatatestlabels.txt"


    if face:
        training_data_tuple = face_parser(face_training_data_filename, face_training_data_labels_filename)
        test_data_tuple = face_parser(face_testing_data_filename, face_testing_data_labels_filename)
    else:
        training_data_tuple = parser(training_data_filename)
        test_data_tuple = parser(test_data_filename)

    if sys.argv[1].lower() == "bayes" or sys.argv[1].lower() == "naivebayes":
        # Check the validity of the command-line arguments
        assert len(sys.argv) in [3,4], incorrectUsageError

        # Run code for training and classifying with naive bayes classifier
        naivebayes.run_naivebayes(training_data_tuple, test_data_tuple, float(sys.argv[2]))

        # # Used for testing different Laplacian constants
        # from numpy import arange
        # for i in arange(0,10,0.1):
        #     naivebayes.run_naivebayes(training_data_tuple, test_data_tuple, i)

    elif sys.argv[1].lower() == "perceptron":
        if sys.argv[2].lower() == "differentiable":
            # Check that the number of command-line arguments is correct
            assert len(sys.argv) >= 4, incorrectUsageError

            if sys.argv[3].lower() == "best":
                # Run code for reproducing the best empirical results
                # discovered for the differentiable perceptron
                perceptron.reproduce_best_results(training_data_tuple, test_data_tuple, True)
            else:
                # Check that the number of command-line arguments is correct
                assert len(sys.argv) == 5, incorrectUsageError

                # Run code for training and classifying with perceptron
                perceptron.run_perceptron(training_data_tuple, test_data_tuple, True, int(sys.argv[3]), int(sys.argv[4]))

        elif sys.argv[2].lower() == "best":
            # Run code for reproducing the best empirical results
            # discovered for the non-differentiable perceptron
            perceptron.reproduce_best_results(training_data_tuple, test_data_tuple, False)
        else:
            # Check that the number of command-line arguments is correct
            assert len(sys.argv) == 4, incorrectUsageError

            # Run code for training and classifying with perceptron
            perceptron.run_perceptron(training_data_tuple, test_data_tuple, False, int(sys.argv[2]), int(sys.argv[3]))

    else:
        sys.exit("INVALID ARGUMENT ERROR: The third argument must be \"bayes\", \"naivebayes\", \"perceptron\", or \"face\" (ignoring case)!")
