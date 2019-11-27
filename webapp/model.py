# G00303598 -- Morgan Reilly
# Emerging Technologies -- 2019

# -- Imports --
import keras
import math
from keras.datasets import mnist
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, BatchNormalization
from keras import backend as K

print("Keras Version " + keras.__version__)

# Batch size => Number of samples to be propagated through network [https://stats.stackexchange.com/a/153535]
# Epoch size => Number of times all training vectors are used to update weights
# Class size => 0 - 9 digits = 10 classes
batch_size = 128
epochs = 10
num_classes = 10

# -- Image Dimension --
# Row / Column => 28 pixels
img_rows, img_cols = 28, 28

# -- Split Data --
# (x / y train data set)
# (x / y test data set)
# Load with => mnist.load_data()
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# -- Check Format of Image Data --
# IF:
# image_data_format => Order of dimensions [https://keras.io/layers/pooling/]
# channels_first => (batch size, feature, step) [https://keras.io/layers/pooling/]
# Reshape train data set => (shape, 1, rows, cols)
# Reshape test data set => (shape, 1, rows, cols)
# Store input shape => (1, rows, cols)
# ELSE:
# channels_last => (batch size, step, feature)
# Reshape train data => (shape, rows, cols, 1)
# Reshape test data => (shape, rows, cols, 1)
# store input shape => (rows, cols, 1)
if K.image_data_format() == 'channels_first':
    # Adapted from: https://keras.io/examples/mnist_cnn/
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)  # Store the input shape
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)  # Store the input shape

# -- Cast Data --
# Cast x_train data set as float32
# Cast x_test data set as float32
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# -- Scale Data --
# Divide by 255 to scale to range [0,1]
x_train /= 255
x_test /= 255

# -- Shape Verification --
# Print x train / test samples to verify re-scale
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# -- Convert Vector to Binary Matrix --
# Use with categorical crossentropy
# y train / test => Vector to be converted into matrix
# num_classes => Total number of classes
# https://keras.io/utils/
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# -- Create Model --
# Adapted from: @Keras Model
# https://colab.research.google.com/github/GoogleCloudPlatform/tensorflow-without-a-phd/blob/master/tensorflow-mnist-tutorial/keras_05_mnist_batch_norm.ipynb
#
# Sequential => Linear stack of layers
# https://keras.io/getting-started/sequential-model-guide/
#
# Conv2D => Apply spatial convolution over images
#   kernel_size => integer tuple/list of single integer, specifies 2D window
#   activation => relu [Rectified Linear Unit]
#   input_shape => 28*28 pixel image
#   use_bias => Boolean to use bias vector
#   padding => Applies extra pixels to image
#   strides => New layer map will have size equal to previous layer divided by strides
#   https://machinelearningmastery.com/padding-and-stride-for-convolutional-neural-networks/
#   https://keras.io/layers/convolutional/
#
# BatchNormalization => Address how neuron outputs are distributed to activation function
#   center => beta offset normalized to tensor
#   scale => Multiply by gamma
#   https://keras.io/layers/normalization/
#   https://codelabs.developers.google.com/codelabs/cloud-tensorflow-mnist/index.html?index=..%2F..index#12
#
# Dense => Linear operation on layers input vector
#
# Flatten => Flatten cube of data into vector that can be consumed by Dense layer
#
# Dense (Final) => Apply softmax transformation
#   Normalizes vector: Output probability range [0-1]
model = Sequential()
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

# -- Compile Model --
# Optimizer:
#   Adam => Method for Stochastic Optimization https://arxiv.org/abs/1412.6980v8
# Loss:
#   One of two parameters required to compile a model
#   categorical_crossentropy => https://keras.io/losses/
# Metrics:
#   https://keras.io/metrics/
#   Function used to judge performance of model
#   accuracy => Tensor value representing mean of output array across all data-points
# Print model layers
model.compile(optimizer=keras.optimizers.Adam(lr=0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# -- Summarise Model --
# Displays model info
# https://keras.io/models/about-keras-models/
model.summary()


# -- Learning Rate Scheduler --
# Start learning rate fast then decay exponentially.
# Set how much the model will adjust and change in response to error produced.
# Learning rate identifies speed of learning process for each neuron.
# The value will be computed between 0 and 1.
# Multiply with the error produced by each outputted value.
def learningrate_decay(epoch):
    return 0.01 * math.pow(0.666, epoch)


# -- Load Model --
# Try to:
# Load JSON && store response
# Read JSON && store response
# Create model from JSON => model_from_json(loaded_json) [Architecture]
# Load weights => Apply to model
# Print success message
#
# Otherwise do:
# Print failure message && subsequent response
# Set Learning rate callback
# Train new model && store
# Serialize to JSON [Architecture]
# Write file
# Save model [Weights & Biases]
try:
    json_to_open = open('model.json', 'r')
    loaded_json_model = json_to_open.read()
    json_to_open.close()
    model = model_from_json(loaded_json_model)
    model.load_weights("model.h5")
    print("Model Load Successful")
except:
    # Adapted from: https://machinelearningmastery.com/save-load-keras-deep-learning-models/#
    print("ERROR: Model Load Failed Successfully")
    print("Generate New Model")
    learningrate_decay_callback = keras.callbacks.LearningRateScheduler(learningrate_decay, verbose=True)
    model = model.fit(x_train, y_train, batch_size, epochs, verbose=1,
                      validation_data=(x_test, y_test), callbacks=[learningrate_decay_callback],
                      workers=0)
    model_json = model.model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.model.save_weights("model.h5")
    print("Model saved successfully")
