__author__ = 'will'





outputs = [-1, 0, 1]


import pickle
import numpy as np

data = pickle.load( open( "trainingdata.p", "rb" ) )
n_images = len(data)
test, training = data[0:n_images/3], data[n_images/3:]


def get_trainint_data(one_hot=True):

    trX = np.array([np.reshape(a[2],a[2].shape[0]**2) for a in training])

    if one_hot:
        trY = np.zeros((len(training),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]
        for i, data in enumerate(training):
            trY[i][data[0] + 1] = 1
    else:
        trY = np.zeros((len(training),1),dtype=np.int8) #[onehot(a[0]) for a in training]
        for i, data in enumerate(training):
            trY[i][0] = data[0]

    return trX, trY

def get_test_data(one_hot=True):
    teX = np.array([np.reshape(a[2],a[2].shape[0]**2) for a in test])

    if one_hot:
        teY = np.zeros((len(test),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]
        for i, data in enumerate(test):
            teY[i][data[0] + 1] = 1
    else:
        teY = np.zeros((len(test),1),dtype=np.int8) #[onehot(a[0]) for a in training]
        for i, data in enumerate(test):
            teY[i][0] = data[0]

    return teX,teY




