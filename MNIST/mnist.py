import idx_decompressor as idxd
import download_mnist as dm
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
import numpy as np


# Downloading and extracting mnist dataset
dm.get_mnist()
train_images = idxd.idx_decompress('train-images-idx3-ubyte')
train_labels = idxd.idx_decompress('train-labels-idx1-ubyte')
test_images = idxd.idx_decompress('t10k-images-idx3-ubyte')
test_labels = idxd.idx_decompress('t10k-labels-idx1-ubyte')

train_images = np.array(train_images, dtype=np.float32)
train_labels = np.array(train_labels, dtype=np.float32)
test_images = np.array(test_images, dtype=np.float32)
test_labels = np.array(test_labels, dtype=np.float32)

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

train_labels = to_categorical(train_labels, 10)
test_labels = to_categorical(test_labels, 10)

# Normalizing images
train_images = train_images/255
test_images = test_images/255

NUM_OF_EPOCHS = 10
BATCH_SIZE = 128

# Creating model
model = Sequential()

model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(2, 2))
model.add(Conv2D(16, (3, 3), activation='relu'))
model.add(MaxPooling2D(2, 2))
model.add(Flatten())
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=10, activation='softmax'))

model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x=train_images, y=train_labels, batch_size=BATCH_SIZE, epochs=NUM_OF_EPOCHS,
          validation_data=(test_images, test_labels))

model.save('mnist_model.h5')
