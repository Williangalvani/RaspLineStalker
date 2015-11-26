import tensorflow as tf
import numpy as np

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

xTrain = np.linspace(0.2, 0.8, 101).reshape([1, -1])
yTrain = (1/xTrain)

x = tf.placeholder(tf.float32, [1,None])
hiddenDim = 10

b = bias_variable([hiddenDim,1])
W = weight_variable([hiddenDim, 1])

b2 = bias_variable([1])
W2 = weight_variable([1, hiddenDim])

hidden = tf.nn.sigmoid(tf.matmul(W, x) + b)
y = tf.matmul(W2, hidden) + b2

# Minimize the squared errors.                                                                
loss = tf.reduce_mean(tf.square(y - yTrain))
step = tf.Variable(0, trainable=False)
rate = tf.train.exponential_decay(0.15, step, 1, 0.9999)
optimizer = tf.train.AdamOptimizer(rate)
train = optimizer.minimize(loss, global_step=step)

# Launch the graph                                                                            
sess = tf.Session()
sess.run(tf.initialize_all_variables())

for step in xrange(0, 40001):
    train.run({x: xTrain}, sess)
    if step % 500 == 0:
        print loss.eval({x: xTrain}, sess)

