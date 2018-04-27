import numpy as np

def loadFile(fileName):
    file = open(fileName, 'r')
    data = np.empty(1, dtype=np.float64)

    data = {}

    while True:
        try:
            line = file.readline()[:-1].split(' ')
            if not line: break

            ## Extract the labels
            if len(line) == 1 and line[0] != '':
                label = line[0]
                data[label] = []

                ## Extract each matrix
                line = list(file.readline()[:-1].split(' '))
                while len(line) != 1:
                    line = line[:-1],dtype=np.float64
                    data[label].append(line)
                    print(line)
                    line = list(file.readline()[:-1].split(' '))

                # data[label] = np.asarray(data[label], dtype=np.float64)

        except:
            break
    # for key in data.keys():
    #     print(key)
    #     print(data[key])
    return data
affine = "Data/check_affine.txt"
relu = "Data/check_relu.txt"
entropy = "Data/check_cross_entropy.txt"

# loadFile(affine)
from Data.affine import *

print(A)
