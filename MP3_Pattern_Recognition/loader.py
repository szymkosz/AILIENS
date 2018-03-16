import numpy as np

def loadFile(fileName):
    file = open(fileName, 'r')
    images = np.array()
    labels = []
    while True:
    for j in range(5):
        curImage = np.array()
        for i in range(32):
            line = [ int(elem) for elem in list( file.readline() )[:-1] ]
            curImage = np.hstack(curImage, line)
        line = list(file.readline())

        labels.append(line[1])
