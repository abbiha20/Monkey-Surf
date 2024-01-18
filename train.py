import cv2
import pandas as pd
import time
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from keras.utils import to_categorical
from PIL import Image

global df

df = pd.DataFrame(columns=['Image', 'Action'])


def create_and_resize_window():
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 300, 350)


def capture_do_nothing():
    global df
    camera = cv2.VideoCapture(0)
    exit = False
    create_and_resize_window()
    while not exit:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        count = 0
        if cv2.waitKey(1) & 0xFF == ord('s'):
            while count != 1500:
                im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(im)
                im_pil = im_pil.resize((100, 100))
                im_np = np.array(im_pil)
                append_to_df(im_np, 0)
                count += 1
                return_value, image = camera.read()
                cv2.imshow('image', image)
                cv2.waitKey(1)
            exit = True
    camera.release()
    cv2.destroyAllWindows()


def capture_jump():
    global df
    camera = cv2.VideoCapture(0)
    exit = False
    create_and_resize_window()
    while not exit:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        count = 0
        if cv2.waitKey(1) & 0xFF == ord('s'):
            while count != 1500:
                im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(im)
                im_pil = im_pil.resize((100, 100))
                im_np = np.array(im_pil)
                append_to_df(im_np, 1)
                count += 1
                return_value, image = camera.read()
                cv2.imshow('image', image)
                cv2.waitKey(1)
            exit = True
    camera.release()
    cv2.destroyAllWindows()


def append_to_df(image, action):
    global df
    df = pd.concat([df, pd.DataFrame({'Image': [image], 'Action': [int(action)]})], ignore_index=True)


def prepare_dataset():
    global df
    df = df.sample(frac=1).reset_index(drop=True)
    X = df['Image']
    Y = df['Action']
    x = np.array(X.tolist())
    x = (x.astype(float) - 128) / 128
    x = np.reshape(x, (X.shape[0], 100, 100, 3))
    y = to_categorical(Y)
    return x, y


def load_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='relu', input_shape=(100, 100, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.8))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train(model, X, y):
    model.fit(X, y, batch_size=64, epochs=1, shuffle=True)


def save_model(model):
    model.save_weights('weights.h5')


if __name__ == '__main__':
    capture_do_nothing()
    time.sleep(1)
    capture_jump()
    time.sleep(1)
    X, y = prepare_dataset()
    model = load_model()
    train(model, X, y)
    save_model(model)
