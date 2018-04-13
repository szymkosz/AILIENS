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
    images, labels = loadFile(fileName)
    images_by_class = organize_by_class(images, labels, 10)

    return (images, images_by_class, labels)

def face_parser(dataFileName, labelFileName):
    images = load_face_data(dataFileName)
    labels = load_face_labels(labelFileName)
    images_by_class = organize_by_class(images, labels, 2)
    return (images, images_by_class, labels)


"""
The loadFile function is a helper function for parser responsible for
parsing the file for the images and classification labels.  See the details of the
first two returned entries in the documentation of parser to understand what this
function returns.
"""
def loadFile(fileName):
    file = open(fileName, 'r')
    images = np.empty((0,1024), dtype=np.int32)
    # print(images.shape)
    labels = []
    while True:
        try:
            curImage = np.array((), dtype=np.int32)
            for i in range(32):
                line = np.asarray([ int(elem) for elem in list( file.readline() )[:-1] ], dtype=np.int32)
                curImage = np.hstack((curImage, line))
                # print(line)
            images = np.vstack((images,curImage))
            line = list(file.readline())
            labels.append(int(line[1]))
            # print(images)
            # print(labels)
        except:
            break
    images = images.T
    labels = np.asarray(labels, dtype=np.int32)

    return (images, labels)


"""
The organize_by_class function is a helper function for parser responsible for
separating the images by their class labels.  See the details of the
third returned entry in the documentation of parser to understand what this
function returns.
"""
def organize_by_class(images, labels, numClasses):
    images_by_class = []
    num_images = labels.shape[0]

    for i in range(numClasses):
        curClass = np.empty((0,images.shape[0]), dtype=np.int32)

        for j in range(num_images):
            if labels[j] == i:
                curClass = np.vstack((curClass, images[:,j]))

        curClass = curClass.T
        images_by_class.append(curClass)

    return images_by_class

def load_face_data(fileName):
    file = open(fileName, 'r')
    images = np.empty((0,4200), dtype=np.int32)
    while True:
        try:
            curImage = np.array((), dtype=np.int32)
            for i in range(70):
                line = np.asarray(list(file.readline())[:-1])
                line = np.where(line == '#', np.ones(line.shape, dtype=np.int32), np.zeros(line.shape, dtype=np.int32))
                curImage = np.hstack((curImage, line))
            images = np.vstack((images,curImage))
        except:
            break
    images = images.T
    return images

def load_face_labels(fileName):
    file = open(fileName, 'r')
    labels = []
    i = 0
    while True:
        try:
            line = list(file.readline())
            labels.append(int(line[0]))
        except:
            break

    labels = np.asarray(labels, dtype=np.int32)
    
    return labels
