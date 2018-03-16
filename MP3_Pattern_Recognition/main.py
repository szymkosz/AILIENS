# import loader
import numpy as np

# loader.loadFile("Data/digitdata/optdigits-orig_train.txt")

a = np.array((),dtype=np.int64)
b = np.asarray([1,2,3], dtype=np.int64)
c = np.asarray([4,5,6], dtype=np.int64)
print(a.shape)
print(b.shape)

vec = np.hstack((a,b))
print(vec)
print(np.hstack((vec,c)))
