from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K
from keras.optimizers import SGD
import numpy as np
import cv2



class LeNet:
    def __init__(self, width, height, depth, classes, weightsPath):
        img_rows, img_cols = 28, 28
        num_classes = 10
        self.inputsize=(img_rows, img_cols)

        if K.image_data_format() == 'channels_first':
            input_shape = (1, img_rows, img_cols)
        else:
            input_shape = (img_rows, img_cols, 1)

        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        # if weightsPath is specified load the weights
        model.load_weights(weightsPath)

        opt = SGD(lr=0.01)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
        self.model=model

    def predict(self,image_in):
        image=image_in.copy()
        if len(image.shape)>2:
            h,w,c=image.shape
            if c>1:
                image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        if image.shape != (self.inputsize):
            image=cv2.resize(image,self.inputsize)

        min_val,max_val,min_pos,max_pos=cv2.minMaxLoc(image)
        if max_val>1:
            image=image.astype(np.float)/255.0

        image=image.reshape(1, self.inputsize[0],self.inputsize[1], 1)
        probs= self.model.predict(image)
        prediction = probs.argmax(axis=1)
        return prediction
