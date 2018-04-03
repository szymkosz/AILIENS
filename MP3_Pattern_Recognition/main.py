import parser as loader
import numpy as np

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
