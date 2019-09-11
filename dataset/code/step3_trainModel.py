from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers
import pickle
import numpy as np

def create_model ():

    model = Sequential()

    model.add(Dense(1024, input_shape = (2048,), activation = 'relu'))
    model.add(Dense(512, activation = 'relu'))
    model.add(Dense(256, activation = 'relu'))
    model.add(Dense(64, activation = 'relu'))
    model.add(Dense(1, activation = 'linear'))

    model.compile(optimizer=optimizers.Adam(lr = 0.00001), loss='mean_squared_error')

    return model

if __name__ == "__main__":

    data_image = pickle.load(open("data_images.p", "rb"))
    data_labels = pickle.load(open("data_labels.p", "rb"))

    checkpoint_path = "model_AVA_test/cp-{epoch:05d}.ckpt"
    cp_callback = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, period = 5)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    model = create_model()
    model.summary()

    seed = 0
    np.random.seed(seed)

    image_train = []
    image_test = []
    label_train = []
    label_test = []

    index_data = []

    for x in range (510016):
        r = np.random.uniform(0.0, 1.0, size = None)
        if r < 0.8:
            index_data.append(x)
            image_train.append(data_image[x])
            label_train.append(data_labels[x])
        else:
            index_data.append(x)
            image_test.append(data_image[x])
            label_test.append(data_labels[x])

    image_train = np.vstack(image_train)
    image_test = np.vstack(image_test)
    score_train  = np.vstack(label_train)
    score_test  = np.vstack(label_test)


    model.save_weights(checkpoint_path.format(epoch=0))

    model.fit(image_train, label_train, validation_data=(image_test, label_test), callbacks = [cp_callback,es], epochs = 30, batch_size = 32)

    '''
    pickle.dump(index_data, open("index_ava_withflip.p", "wb"))
    pickle.dump(image_test, open("image_test_withflip.p", "wb"))
    pickle.dump(label_test, open("label_test_withflip.p", "wb"))
    '''
