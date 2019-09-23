from step3_trainModel import create_model
from step2_processDataset import get_image
import pickle
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers



if __name__ == "__main__":
    #retrieve data
    NO = pickle.load(open("indice_test.p", "rb"))
    fv_test = pickle.load(open("fv_test.p", "rb"))
    score_test = pickle.load(open("score_test.p", "rb"))

    NO = np.vstack(NO)
    fv_test = np.vstack(fv_test)
    score_test = np.vstack(score_test)

    for index in range(20):#NO.shape[0]):

        '''model = create_model()'''
        model = Sequential()

        model.add(Dense(1024, input_shape = (2048,), activation = 'relu'))
        model.add(Dense(512, activation = 'relu'))
        model.add(Dense(1, activation = 'linear'))

        model.compile(optimizer=optimizers.Adam(lr = 0.00001), loss='mean_squared_error')
        '''model'''
        checkpoint_path = "model_AVA/cp-00010.ckpt"
        model.load_weights(checkpoint_path, by_name = False)
        score = model.predict(fv_test[NO[index]])
        #print(score)
        #print(score_test[NO[index]])
        #print(NO[index])
        img, flipped_image = get_image(NO[index][0])
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if score < 5:
            cv2.imwrite("low_scores/image_{}_{}.jpg".format(score[0][0],score_test[index]),img)

            plt.imshow(img, interpolation = 'bicubic')
            plt.title('score prediction : {} original {}'.format(score,score_test[index]))
            plt.xticks([]), plt.yticks([])
            #plt.show()


        elif score > 5:
            cv2.imwrite("high_scores/image_{}_{}.jpg".format(score[0][0],score_test[index]),img)
