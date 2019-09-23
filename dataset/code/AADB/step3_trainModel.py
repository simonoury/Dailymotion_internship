from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import optimizers
import pickle
import numpy as np

#function creates and returns the model
def create_model ():

    model = Sequential()

    model.add(Dense(1024, input_shape = (2048,), activation = 'relu'))
    model.add(Dense(512, activation = 'relu'))
    model.add(Dense(1, activation = 'linear'))

    model.compile(optimizer=optimizers.Adam(lr = 0.00001), loss='mean_squared_error')

    return model
if __name__ == "__main__":

    #load data from pickle as lists
    data_fv = pickle.load(open("fv_inceptionv3.p", "rb"))
    data_score = pickle.load(open("label_inceptionv3.p", "rb"))

    #creates checkpoint to save model
    checkpoint_path = "model_AADB/cp-{epoch:05d}.ckpt"
    cp_callback = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, period=3)

    #sets the seed to have the same random inputs
    seed = 0
    np.random.seed(seed)

    #divides our data in training and test parts (80%-20%)
    fv_train = []
    fv_test = []
    score_train = []
    score_test = []
    N = len(data_fv)

    indice_train=[]
    indice_test=[]

    for n in range (N):
        r = np.random.uniform(0.0, 1.0, size = None)
        if r < 0.8:
            indice_train.append(n)
            fv_train.append(data_fv[n])
            score_train.append(data_score[n])
        else:
            indice_test.append(n)
            fv_test.append(data_fv[n])
            score_test.append(data_score[n])

    pickle.dump(indice_train, open("indice_train.p", "wb"))
    pickle.dump(indice_test, open("indice_test.p", "wb"))
    pickle.dump(fv_test, open("fv_test.p", "wb"))
    pickle.dump(score_test, open("score_test.p", "wb"))

    #convert lists to arrays
    fv_train = np.vstack(fv_train)
    fv_test = np.vstack(fv_test)
    score_train = np.vstack(score_train)
    score_test = np.vstack(score_test)

    #builds, compiles, saves and runs the model
    model = create_model()
    model.summary()
    #model.save_weights(checkpoint_path.format(epoch=0)) callbacks = [cp_callback],

    model.fit(fv_train, score_train, validation_data=(fv_test, score_test),epochs = 50, batch_size = 16)
