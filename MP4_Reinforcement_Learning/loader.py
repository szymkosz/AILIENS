import numpy as np

TRAINING_OUTPUT_FILENAME = "training_results.npz"


"""
The parser function takes in the name of a file containing the states and actions
of an expert Pong game and returns a 2-tuple of the game states and the expert's
corresponding actions.  The details of the returned tuple are as follows:

states (0th entry): Let T be the total number of game states in the file represented
                    by "fileName".  Then this entry is a T x 5 numpy array
                    where every row contains ball_x, ball_y, velocity_x, velocity_y,
                    and paddle_y in this order for an individual game state.

actions:            Let T be the total number of game states in the file represented
(1th entry)         by "fileName".  Then this entry is a T-dimensional numpy vector
                    such that the ith entry contains the expert's action in the ith
                    game state.  This entry is 0 if the expert moves the paddle down,
                    1 if the expert doesn't move the paddle, and 2 if the expert moves
                    the paddle up.
"""
def parser(fileName):
    return loadFile(fileName)


"""
The loadFile function is a helper function for parser responsible for
parsing the file for the game states and the expert's corresponding actions.
See the details of the two returned entries in the documentation of parser to
understand what this function returns.
"""
def loadFile(fileName):
    file = open(fileName, 'r')
    data = np.empty((0,6), dtype=np.float64)

    while True:
        try:
            line = np.asarray((file.readline()[:-1]).split(' '), dtype=np.float64)
            data = np.vstack((data,line))
        except:
            break

    states = data[:,:-1]
    actions = data[:,-1]
    return (states, actions)


"""
This function takes in a list of weights and a list of biases and saves them to
a .npz file.  The ith entry of both of these lists corresponds to the 2D numpy
matrix of weights and numpy vector of biases respectively of the ith layer of
the neural network.

The save_training_results_to_file and load_training_results_from_file functions
are used to efficiently store and retrieve the weights and biases of the neural
network after they are obtained through training.
"""
def save_training_results_to_file(weights, biases, fileName=TRAINING_OUTPUT_FILENAME):
    reshaped_weights = []
    weight_shapes = []

    for matrix in weights:
        reshaped_weights.append(matrix.flatten())
        weight_shapes.append(matrix.shape)

    np.savez(fileName, weights=reshaped_weights, weight_shapes=weight_shapes, biases=biases)


"""
This function loads a list of weights and a list of biases from a .npz file
and returns them.  The ith entry of both of these lists corresponds to the 2D numpy
matrix of weights and numpy vector of biases respectively of the ith layer of
the neural network.

The save_training_results_to_file and load_training_results_from_file functions
are used to efficiently store and retrieve the weights and biases of the neural
network after they are obtained through training.
"""
def load_training_results_from_file(fileName=TRAINING_OUTPUT_FILENAME):
    data = np.load(fileName)
    original_weights = []

    for matrix, shape in zip(data['weights'], data['weight_shapes']):
        original_weights.append(matrix.reshape(tuple(shape)))

    return (original_weights, data['biases'])
