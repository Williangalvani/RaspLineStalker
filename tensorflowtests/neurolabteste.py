import pickle
import numpy as np

outputs = (-1,0,1)

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



import numpy as np
import neurolab as nl
# Create train samples
input = np.random.uniform(-0.5, 0.5, (10, 2))
print input.shape
print input

target = ([trX,trY]).reshape(10, 1)
# Create network with 2 inputs, 5 neurons in input layer and 1 in output layer
net = nl.net.newff([[-0.5, 0.5], [-0.5, 0.5]], [5, 1])
# Train process
print net.train(input, target, show=15)
#Epoch: 15; Error: 0.150308402918;
#Epoch: 30; Error: 0.072265865089;
#Epoch: 45; Error: 0.016931355131;
#The goal of learning is reached
#>>> # Test
print net.sim([[0.2, 0.1]]) # 0.2 + 0.1
#array([[ 0.28757596]])