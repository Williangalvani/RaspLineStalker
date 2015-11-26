import tensorflow as tf
import numpy as np
import input_data
import pickle


outputs = [-1,0,1]
size = 28*28


def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def model(X, w_h, w_h2, w_o):
    h = tf.nn.sigmoid(tf.matmul(X, w_h)) # this is a basic mlp, think 2 stacked logistic regressions
    h2 = tf.nn.sigmoid(tf.matmul(h, w_h2))
    return tf.matmul(h2, w_o) # note that we dont take the softmax at the end because our cost fn does that for us

#
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# trX, trY, teX, teY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
#
#
# print trX.shape
# print trY.shape
# print teX.shape
# print teY.shape
#

data = pickle.load( open( "trainingdata.p", "rb" ) )
n_images = len(data)
training, test = data[0:n_images/2], data[n_images/2:]


trX = np.array([np.reshape(a[2],28*28) for a in training])
trY = np.zeros((len(training),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]

for i, data in enumerate(training):
    trY[i][data[0] + 1] = 1


teX = np.array([np.reshape(a[2],28*28) for a in test])
teY = np.zeros((len(test),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]

for i, data in enumerate(test):
    teY[i][data[0] + 1] = 1
#
# print trX.shape
# print trY.shape
# print teX.shape
# print teY.shape



outputs = 3


X = tf.placeholder("float", [None, size])
Y = tf.placeholder("float", [None, outputs])

w_h =  init_weights([size, 625]) # create symbolic variables
w_h2 = init_weights([625, 625]) # create symbolic variables
w_o =  init_weights([625, outputs])

py_x = model(X, w_h,w_h2, w_o)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y)) # compute costs
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost) # construct an optimizer
predict_op = tf.argmax(py_x, 1)


sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

for i in range(50):
    for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
        sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})

    print i, np.mean(np.argmax(teY, axis=1) ==  sess.run(predict_op, feed_dict={X: teX, Y: teY}))

