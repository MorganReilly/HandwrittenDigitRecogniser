# Adapted from keras-mnist-nn.ipynb
# G00303598 -- Morgan Reilly
# Emerging Technologies -- 2019

# Imports
import keras
import math
from keras.datasets import mnist
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D
from keras import backend as K
from keras.layers.normalization import BatchNormalization
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 

print("Keras Version " + keras.__version__)

batch_size = 128  # Number of batches
epochs = 10  # Epoch count
num_classes = 10  # Class count

# Load and prepare data set:
# We load the data with the mnist.load_data() function
# Store the data into arrays for test and train set, along with labels
# Cast the arrays as type -> float32
# input image dimensions
img_rows, img_cols = 28, 28

# Loading data from training and test sets along with labels
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

# If the data format for the images : channels first
if K.image_data_format() == 'channels_first':
    # Reshape the data then train and store
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)  # Store the input shape
# Not channels first    
else:
    # Reshape the data then strain and store
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)  # Store the input shape

X_train = X_train.astype('float32')  # Casting as type : float32
X_test = X_test.astype('float32')

X_train /= 255  # Original data is uint8 (0-255). Scale to range [0,1]
X_test /= 255

# Print to verify
print('x_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = keras.utils.to_categorical(Y_train, num_classes)
Y_test = keras.utils.to_categorical(Y_test, num_classes)

# Build the model
# This model is a Convolutional2D model
# Convolutional 2D neural networkds apply a series of learnable filters to the input image.
# A conv. layer is defined by the filter size, number of filters applied and the stride.
# The input and output of the conv. layer each have 3 dimensions (width, height and number of channels), starting with input image (width, height, RGB).
# The width and height of the output can be adjusted by using a stride > 1 or with a max-pooling operation.
model = Sequential()  # New sequential model (linear stack of layers)

model.add(Conv2D(12, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))

model.add(Conv2D(24, (3, 3), activation='relu',
                 use_bias=False, padding='same'))
model.add(BatchNormalization(center=True, scale=False))
model.add(Dense(128, activation='relu'))

model.add(Conv2D(36, (6, 6), activation='relu',
                 use_bias=False, padding='same', strides=2))
model.add(BatchNormalization(center=True, scale=False))
model.add(Dense(128, activation='relu'))

model.add(Conv2D(48, (6, 6), activation='relu',
                 use_bias=False, padding='same', strides=2))
model.add(BatchNormalization(center=True, scale=False))
model.add(Dense(128, activation='relu'))

model.add(Flatten())

model.add(Dense(200, use_bias=False))
model.add(BatchNormalization(center=True, scale=False))
model.add(Dense(128, activation='relu'))

model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))

model.compile(optimizer=keras.optimizers.Adam(lr=0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# print model layers
model.summary()


# Add a Learning Rate Scheduler
# This starts the learning rate fast then decays exponentially.
# It sets how much the model will adjust and change in response to error produced
# The learning rate identifies the speed of the learning process for each neuron. 
#  The value will be computed between 0 and 1. This multiplies with the error that each outputted value produces.
# Learning rate decay function
def learningrate_decay(epoch):
    return 0.01 * math.pow(0.666, epoch)


# learning rate schedule callback
learningrate_decay_callback = keras.callbacks.callbacks.LearningRateScheduler(learningrate_decay, verbose=True)

# Try to load the model
try:
    # Load json file and create new model
    json_to_open = open('model.json', 'r')
    loaded_json_model = json_to_open.read()
    json_to_open.close()
    model = model_from_json(loaded_json_model)

    # Load weights into new model
    model.load_weights("model.h5")
    print("Loaded from disk")
except:
    print("ERROR: Could Not Load Model")
    print("Creating New Model")
    model_history = model.fit(X_train, Y_train, batch_size, epochs, verbose=1,
                              validation_data=(X_test, Y_test), callbacks=[learningrate_decay_callback],
                              workers=0)

    # Adapted from: https://machinelearningmastery.com/save-load-keras-deep-learning-models/#
    # Serialize model to JSON.
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    # Serialize weights to HDF5
    model.save_weights("model.h5")
    print("Model saved sucessfully")
