import numpy as np

def loadFile(fileName):
    file = open(fileName, 'r')
    images = np.empty((0,1024))
    # print(images.shape)
    labels = []
    while True:
        try:
            curImage = np.array(())
            for i in range(32):
                line = np.asarray([ int(elem) for elem in list( file.readline() )[:-1] ])
                curImage = np.hstack((curImage, line))
                # print(line)
            images = np.vstack((images,curImage))
            line = list(file.readline())
            labels.append(int(line[1]))
            # print(images)
            # print(labels)
        except:
            break
    labels = np.asarray(labels)

    return (images, labels)
