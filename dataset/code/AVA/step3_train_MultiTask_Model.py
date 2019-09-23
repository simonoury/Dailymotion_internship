from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.layers import Dense, Flatten, Dropout, AveragePooling2D, GlobalAveragePooling2D, Input
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers
from tensorflow.keras.metrics import top_k_categorical_accuracy
import pickle
import numpy as np

def top_1_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k =1)

def create_model ():

    model_input = Input(shape=(2048,))

    x = Dense(1024, activation = 'relu')(model_input)
    x = Dropout(0.3)(x)
    x = Dense(1024, activation = 'relu')(x)
    x = Dropout(0.3)(x)

    y1 = Dense(512, activation = 'relu')(x)
    y1 = Dropout(0.3)(y1)
    y1 = Dense(66, activation = 'softmax', name='classification')(y1)

    y2 = Dense(1024, activation = 'relu')(x)
    y2 = Dense(512, activation = 'relu')(y2)
    y2 = Dense(256, activation = 'relu')(y2)
    y2 = Dense(64, activation = 'relu')(y2)
    y2 = Dense(1, activation = 'linear', name= 'score')(y2)

    model = Model(inputs=model_input, outputs= [y1, y2])

    model.compile(loss = {'classification':'binary_crossentropy', 'score': 'mean_squared_error'}, optimizer=optimizers.Adam(lr = 0.00001), metrics={'classification': top_1_accuracy, 'score': 'mae'})

    return model

if __name__ == "__main__":

    data_image = pickle.load(open("data_images.p", "rb"))
    data_tag1 = pickle.load(open("data_tags1.p", "rb"))
    data_labels = pickle.load(open("data_labels.p", "rb"))
    data_tag2 = pickle.load(open("data_tags2.p", "rb"))

    checkpoint_path = "model_AVA_classification_withflip2/cp-{epoch:05d}.ckpt"
    cp_callback = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, period = 5)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
    print('# DEBUG: 1')

    seed = 0
    np.random.seed(seed)

    image_train = []
    image_test = []

    label_test=[]
    label_train=[]
    index_data = []

    tags_ = np.zeros([len(data_tag1), 66])

    for i in range (len(data_tag1)):
        tags_[i, data_tag1[i]-1] = 1
        tags_[i, data_tag2[i]-1] = 1

    tags_train = []
    tags_test = []


    for x in range (510016):
        r = np.random.uniform(0.0, 1.0, size = None)
        if r < 0.8:
            index_data.append(x)
            image_train.append(data_image[x])
            tags_train.append(tags_[x][:])
            label_train.append(data_labels[x])
        else:
            index_data.append(x)
            image_test.append(data_image[x])
            tags_test.append(tags_[x][:])
            label_test.append(data_labels[x])

    print('# DEBUG: 2')


    tags_train = np.vstack(tags_train)
    tags_test = np.vstack(tags_test)
    image_train = np.vstack(image_train)
    image_test = np.vstack(image_test)
    label_test = np.vstack(label_test)
    label_train = np.vstack(label_train)

    print('# DEBUG: 3')
    model = create_model()
    model.summary()

    print('# DEBUG: 4')

    model.save_weights(checkpoint_path.format(epoch=0))

    print('# DEBUG: 5')

    model.fit(image_train, [tags_train,label_train], validation_data=(image_test, [tags_test, label_test]), callbacks = [cp_callback,es], epochs = 200, batch_size = 128)

    print('# DEBUG: 6')

    pickle.dump(index_data, open("index_ava.p", "wb"))
    pickle.dump(image_test, open("image_test.p", "wb"))
    pickle.dump(tags_test, open("tag1_test.p", "wb"))
    pickle.dump(label_test, open("label_test.p", "wb"))
