import tensorflow as tf
import numpy as np
import input_data
import pickle

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def model(X, w_h, w_h2, w_o, p_drop_input, p_drop_hidden): # this network is the same as the previous one except with an extra hidden layer + dropout
    X = tf.nn.dropout(X, p_drop_input)
    h = tf.nn.relu(tf.matmul(X, w_h))

    h = tf.nn.dropout(h, p_drop_hidden)
    h2 = tf.nn.relu(tf.matmul(h, w_h2))

    h2 = tf.nn.dropout(h2, p_drop_hidden)

    return tf.matmul(h2, w_o)

#
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# trX, trY, teX, teY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
#

outputs = [-1, 0, 1]


data = pickle.load( open( "trainingdata.p", "rb" ) )
n_images = len(data)
test, training = data[0:n_images/3], data[n_images/3:]


trX = np.array([np.reshape(a[2],28*28) for a in training])
trY = np.zeros((len(training),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]

for i, data in enumerate(training):
    trY[i][data[0] + 1] = 1


teX = np.array([np.reshape(a[2],28*28) for a in test])
teY = np.zeros((len(test),len(outputs)),dtype=np.uint8) #[onehot(a[0]) for a in training]

for i, data in enumerate(test):
    teY[i][data[0] + 1] = 1


print trX.shape
print trY.shape
print teX.shape
print teY.shape


for i in trY:
    print i
outputs = 3

X = tf.placeholder("float", [None, 784])
Y = tf.placeholder("float", [None, outputs])

w_h = init_weights([784, 625])
w_h2 = init_weights([625, 625])
w_o = init_weights([625, outputs])

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
predict_op = tf.argmax(py_x, 1)

sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

for i in range(100):
    for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
        sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end],
                                      p_keep_input: 0.8, p_keep_hidden: 0.5})
    print i, np.mean(np.argmax(teY, axis=1) ==
                     sess.run(predict_op, feed_dict={X: teX, Y: teY,
                                                     p_keep_input: 1.0,
                                                     p_keep_hidden: 1.0}))

print list(sess.run(predict_op, feed_dict={X: teX, Y: teY, p_keep_input: 1.0, p_keep_hidden: 1.0}))
#for i in range(1000):
#    print sess.run(predict_op, feed_dict={X: teX[1:1+1], Y: teY, p_keep_input: 1.0, p_keep_hidden: 1.0})