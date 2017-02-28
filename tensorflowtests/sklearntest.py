__author__ = 'will'
import numpy
import tensorflow as tf

from get_robot_data import *

trX, trY = get_trainint_data(one_hot=False)
teX, teY = get_test_data(one_hot=False)

X_train, X_test, y_train, y_test = trX, teX, trY, teY

X_train = numpy.array(X_train, dtype=np.int64)
y_train = (numpy.array(y_train, dtype=np.int64) + 1).flatten()
X_test = numpy.array(X_test, dtype=np.int64)
y_test = numpy.array(y_test, dtype=np.int64).flatten() + 1

feature_columns = [tf.contrib.layers.real_valued_column("", dimension=256)]

classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10],
                                            n_classes=3,
                                            model_dir="/tmp/iris_model")

classifier.fit(x=X_train,
               y=y_train,
               steps=2000)

accuracy_score = classifier.evaluate(x=X_test,
                                     y=y_test)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))


def predict_direction(img):
    img = np.array([np.reshape(img, img.shape[0] ** 2)], dtype=np.int64)
    ret = list(classifier.predict(img))[0] - 1
    return ret
