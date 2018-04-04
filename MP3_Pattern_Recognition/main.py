"""
-------------------------------------------------------------------------------
Should there be a command-line argument for learning-rate decay function?





This is the driver file for training a naive bayes classifier or perceptron with the training data
and then classifying the test data.

To train and classify with a naive bayes classifier with particular hyperparameters,
run the following command:

python main.py <bayes> <laplace>

where:
<bayes>     = "bayes" or "naivebayes" (ignoring case)
<laplace>   = The laplacian smoothing constant to use for computing the likelihoods

To train and classify with a perceptron with particular hyperparameters, run the
following command:

python main.py <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>

where:
<perceptron>                = "perceptron" (ignoring case)
<hasBias>                   = 0 if the perceptron shouldn't have biases, 1 if it should
<weightsAreRandom>          = 0 if the perceptron's weights (and biases if they are present)
                            : should be initialized to zero, 1 if they should be initialized randomly
<hasRandomTrainingOrder>    = 0 if the order of the training examples should be fixed
                            : between epochs, 1 if it should be random between epochs
<epochs>                    = number of epochs (passes) over the training data during the training phase
-------------------------------------------------------------------------------
"""

#import numpy as np
import sys
from parser import parser
import naivebayes
import perceptron


if __name__ == "__main__":
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
                        + "\"python %s <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>\"" % sys.argv[0]

    assert len(sys.argv) >= 3, incorrectUsageError

    training_data_filename = "Data/digitdata/optdigits-orig_train.txt"
    test_data_filename = "Data/digitdata/optdigits-orig_test.txt"

    training_data_tuple = parser(training_data_filename)
    test_data_tuple = parser(test_data_filename)

    if sys.argv[1].lower() == "bayes" or sys.argv[1].lower() == "naivebayes":
        # Check the validity of the command-line arguments
        assert len(sys.argv) == 3, incorrectUsageError

        # Run code for training and classifying with naive bayes classifier
        naivebayes.run_naivebayes(training_data_tuple, test_data_tuple, int(sys.argv[2]))

    elif sys.argv[1].lower() == "perceptron":
        # Check that the number of command-line arguments is correct
        assert len(sys.argv) == 6, incorrectUsageError

        # Parse the boolean parameters into booleans and evaluate their validity
        parsedBooleans = []
        for i in range(2,5):
            parsedValue = int(sys.argv[i])
            assert parsedValue == 0 or parsedValue == 1, "INVALID ARGUMENT ERROR: " \
                                                       + "<hasBias>, <weightsAreRandom>, and <hasRandomTrainingOrder> " \
                                                       + "must be 0 or 1!"
            parsedBooleans.append(parsedValue == 1)

        # Run code for training and classifying with perceptron
        perceptron.run_perceptron(training_data_tuple, test_data_tuple, parsedBooleans[0], parsedBooleans[1], parsedBooleans[2], int(sys.argv[5]))

    else:
        sys.exit("INVALID ARGUMENT ERROR: The third argument must be \"bayes\", \"naivebayes\", or \"perceptron\" (ignoring case)!")

"""
ar = np.array([[1,1,1,2],[0,2,1,-1]])

print(ar.shape,np.sum(ar, axis=1),np.argmax(ar,axis=1))

training_data, training_data_by_class, training_labels = loader.parser("Data/digitdata/optdigits-orig_train.txt")

image = training_data[:,0]

print(image.shape)
image = image.reshape((32,32))
print(image.shape)

for i in range(32):
    line = ""
    for j in range(32):
        line += str(image[i,j])

    print(line)

print(training_data.shape)
print(training_labels)
print(training_labels.shape)

print(training_data_by_class)
print(len(training_data_by_class))

sum = 0

for i in range(len(training_data_by_class)):
    print(training_data_by_class[i])
    print(training_data_by_class[i].shape)

    sum += training_data_by_class[i].shape[1]

print(sum)

image2 = training_data_by_class[0][:,0]

print(image2.shape)
image2 = image2.reshape((32,32))
print(image2.shape)

for i in range(32):
    line = ""
    for j in range(32):
        line += str(image2[i,j])

    print(line)
"""

# a = np.array((),dtype=np.int64)
# b = np.asarray([1,2,3], dtype=np.int64)
# c = np.asarray([4,5,6], dtype=np.int64)
# # print(a.shape)
# # print(b.shape)
# # np.reshape(b, (3,1))
# # np.reshape(c, (3,1))
# #
# vec = np.hstack((a,b))
# # # vec.reshape((3,1))
# print(vec)
# print(np.vstack((b,c)))
# # print(np.concatenate((vec,c),1))
