# -*- coding: utf-8 -*-
"""last.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XiEDt6dHhocCXKsdllD81WF2YF3wQk6O
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot
from sklearn.model_selection import train_test_split

df = pd.read_csv('fer2013_edited.csv')
df.head()

df.emotion.unique()

label_to_text = {0:'anger', 2:'fear', 3:'happiness', 4:'sadness'}

img_array = df.pixels.apply(lambda x : np.array(x.split(' ')).reshape(48,48,1).astype('float32'))

img_array = np.stack(img_array,axis=0)

labels = df.emotion.values

X_train,X_test,y_train,y_test = train_test_split(img_array,labels,test_size=.1)

X_train.shape,y_train.shape,X_test.shape,y_test.shape

X_train = X_train/255
X_test = X_test/255

# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(48, 48, 1)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(2,2),
    #
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(2,2),
    #
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(2,2),
    #
    tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1000, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

# Train the model with batch normalization and early stopping
history = model.fit(X_train, y_train, epochs=20, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_acc)







