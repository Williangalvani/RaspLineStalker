__author__ = 'will'
import random

from sklearn import datasets, cross_validation, metrics
from sklearn import preprocessing

import skflow
import pickle
import numpy as np

outputs = 1

from get_robot_data import *

trX,trY = get_trainint_data(one_hot=False)
teX,teY = get_test_data(one_hot=False)

random.seed(42)

# Scale data to 0 mean and unit std dev.
scaler = preprocessing.StandardScaler()
#trX = scaler.fit_transform(trX)
#teX = scaler.fit_transform(teX)
# Split dataset into train / test
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y,
#     test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = trX, teX, trY, teY


# Build 2 layer fully connected DNN with 10, 10 units respecitvely.
regressor = skflow.TensorFlowDNNRegressor(  steps=1000, hidden_units=[500,500,500,500,500], learning_rate=0.1, batch_size=1,optimizer="Adagrad")

# Fit and predict
regressor.fit(X_train, y_train)

size = len(X_test)

options = random.sample(xrange(size),200)

erroacumulado = 0
erroreto = 0
for option in options:
    x, y = X_test[option:option+1], y_test[option:option+1]
    pred= regressor.predict(x)
    erro = pred[0][0] - y[0][0]
    erroacumulado+= abs(erro/200.0)
    erroreto+=abs(y[0][0])/200.0
    #print "predicted: ", pred, " was: ", y, " error is ", erro, " acumulado: ", erroacumulado

#print erroacumulado, erroreto
    #score = metrics.mean_squared_error(regressor.predict(x),y)


    #print("MSE: %f" % score)


def get_velocity(img):
    img = np.array([np.reshape(img,img.shape[0]**2)],dtype=np.float64)
    #img = scaler.fit_transform(img)
    ret =  regressor.predict(img)[0][0]
    print ret
    return ret
