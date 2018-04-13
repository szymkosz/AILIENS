import numpy as np

"""
The parser function takes in the name of a file containing digit data
and returns a 3-tuple of the digit images, digit images organized by class label,
and the class labels.  The details of the returned tuple are as follows:

images (0th entry): Let T be the total number of images in the file represented
                    by "fileName".  Then this entry is a 1,024 x T numpy array
                    where every column is the bitmap of an individual image.

images_by_class:    Let n_k be the number of images in the file labeled as class k.
(1th entry)         Then this entry is a list such that the kth entry is a 1,024 x n_k
                    numpy array where every column is the bitmap of an individual image
                    belonging to class k.

labels (2th entry): Let T be the total number of images in the file represented
                    by "fileName".  Then this entry is a 1D numpy array containing
                    all T classification labels.  The ith entry is the label for
                    the ith image in the file.
"""
def parser(fileName):
    return loadFile(fileName)

"""
The loadFile function is a helper function for parser responsible for
parsing the file for the images and classification labels.  See the details of the
first two returned entries in the documentation of parser to understand what this
function returns.
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




training_output_filename = "training_results.npz"

def save_training_results_to_file(weights, biases):
    reshaped_weights = []
    weight_shapes = []

    for matrix in weights:
        reshaped_weights.append(matrix.flatten())
        weight_shapes.append(matrix.shape)

    np.savez(training_output_filename, weights=reshaped_weights, weight_shapes=weight_shapes, biases=biases)

def load_training_results_from_file():
    data = np.load(training_output_filename)

    original_weights = []
    print(data['weights'])
    print("These are shapes")
    print(data['weight_shapes'])

    for s in data['weight_shapes']:

    for matrix, shape in (data['weights'], data['weight_shapes']):
        print(matrix)
        print("This is a shape")
        print(shape)
        original_weights.append(matrix.reshape(tuple(shape)))

    return (original_weights, data['biases'])

w = np.arange(9).reshape(3,3)
w2 = np.arange(15).reshape(3,5)
print(w)
print(w2)

weights = [w, w2]
biases = [np.arange(20), np.arange(5)]

print(weights)
print(biases)
save_training_results_to_file(weights, biases)
orig_weights, orig_biases = load_training_results_from_file()
print(orig_weights, orig_biases)
"""
print(data.files)
print(data['weights'])
print(data['weight_shapes'])
print(data['biases'])
"""
