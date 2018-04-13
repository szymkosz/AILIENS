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
