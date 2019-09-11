from step3_trainModel import create_model
from step2_processDataset import get_image, get_data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers
import numpy as np
import cv2
import pickle
from matplotlib import pyplot as plt

if __name__ == "__main__":

    NO = pickle.load(open("index_ava.p", "rb"))
    image_test = pickle.load(open("images_test.p", "rb"))
    label_test = pickle.load(open("label_test.p", "rb"))

    NO = np.vstack(NO)
    image_test = np.vstack(image_test)
    label_test = np.vstack(label_test)

    #model = create_model()
    model = Sequential()

    model.add(Dense(1024, input_shape = (2048,), activation = 'relu'))
    model.add(Dense(512, activation = 'relu'))
    model.add(Dense(1, activation = 'linear'))

    model.compile(optimizer=optimizers.Adam(lr = 0.00001), loss='mean_squared_error')

    checkpoint_path = "model_AADB/cp-00048.ckpt"
    model.load_weights(checkpoint_path, by_name = False)

    for index in range (10):
        score = model.predict(image_test[NO[index]])
        No, img_id, meanscore = get_data(NO[index][0])
        img = cv2.imread('images/%s.jpg' %img_id)

        if score < 2.5:

            cv2.imwrite("low_score_modelAADB/image_{}_{}.jpg".format(score[0][0], meanscore), img)
            plt.imshow(img, interpolation = 'bicubic')
            plt.title('score prediction: {} original: {}'.format(score,label_test[index]))
            plt.xticks([]), plt.yticks([])

        elif score > 2.5:
            cv2.imwrite("high_score_modelAADB/image_{}_{}.jpg".format(score[0][0], meanscore), img)
            plt.imshow(img, interpolation = 'bicubic')
            plt.title('score prediction: {} original: {}'.format(score,meanscore))
            plt.xticks([]), plt.yticks([])
