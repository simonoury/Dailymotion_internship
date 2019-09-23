from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers
from inceptionv3_class_features import InceptionV3Embedder
import logging
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def get_images(video_name):
    os.system("ffmpeg -i {} -r  1 -f image2 image-%3d.png".format(video_name))
    data = []
    for filename in os.listdir():
        if filename.endswith(".png"):
            data.append(filename)
        else:
            continue
    data.sort()
    return data


def get_cluster_num (data, EPS):
    db = DBSCAN(eps=EPS, min_samples=1).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    return n_clusters_, n_noise_

def get_model():
    model = Sequential()
    model.add(Dense(1024, input_shape = (2048,), activation = 'relu'))
    model.add(Dense(512, activation = 'relu'))
    model.add(Dense(256, activation = 'relu'))
    model.add(Dense(64, activation = 'relu'))
    model.add(Dense(1, activation = 'linear'))
    model.compile(optimizer=optimizers.Adam(lr = 0.00001), loss='mean_squared_error')
    checkpoint_path = "model_AVA_withflip/cp-00020.ckpt"
    model.load_weights(checkpoint_path, by_name = False)
    return model

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    inception_v3 = InceptionV3Embedder()

    name_im = []

    for file in os.listdir():
        if file.endswith('.mp4'):
            video_name = file
    list_images = get_images(video_name)
    #os.remove(video_name)

    model = get_model()

    image_index_map = {}
    index_image_map = {}
    images_inceptionv3 = []
    counter = 0
    for name in list_images :
        print (name)
        img = cv2.imread(name)
        if img is not None:
            name_im.append(name)
            image_index_map[name]=counter
            index_image_map[counter]=name
            images_inceptionv3.append(inception_v3.predict(img))
            counter += 1

    images_inceptionv3 = np.vstack(images_inceptionv3)

    images = len(list_images)
    if images <= 50:
        EPS = 10
    if 50 < images <= 100:
        EPS = 12
    if 100 < images <= 150:
        EPS = 14
    if 150 < images <= 200:
        EPS = 15
    if 200 < images <= 250:
        EPS = 14
    if 250 < images <= 300:
        EPS = 18
    if 300 < images <= 350:
        EPS = 19
    if 350 < images <= 400:
        EPS = 20
    if images > 400:
        EPS = 22

    n_clusters, n_noise = get_cluster_num(images_inceptionv3, 10)
    print("Number of clusters: ", n_clusters)
    print("Noise points: ", n_noise)

    print("Number of images: ", images)
    print("Epsilon: ", '11 llalalalal')

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(images_inceptionv3)

    counter_score_map = {}
    dict_ = {}
    dict_hiscore = {}
    for index in range (len(kmeans.labels_)):
        c = kmeans.labels_[index]
        name = index_image_map[index]
        try:
            dict_[c].append(name)
        except:
            dict_[c] = [name]

    best_images = [None]*n_clusters
    best_scores = [0.0]*n_clusters

    counter = 0
    for i in range (n_clusters):
        name_im = dict_[i]
        print(name_im)
        for name in name_im:
            index = image_index_map[name]
            img = cv2.imread(name)
            fv = inception_v3.predict(img)
            fv = np.asarray(fv)
            input_vector = np.zeros(shape=(1,2048))
            input_vector[0,:]=fv
            score = model.predict(input_vector)
            counter +=1
            print ("Cluster:{}/{}".format(i+1,n_clusters))
            print ("name image: ", name)
            print ("score image: ", score)
            if score > best_scores[i]:
                best_scores[i]=score
                best_images[i]=name
            print("best image cluster: ", best_images[i])
            print("best score cluster: ", best_scores[i])
            print("count: {}/{} ".format(counter,len(kmeans.labels_)))
            print("____________________________________")

    for index in range (n_clusters):
        img = cv2.imread(best_images[index])
        cv2.imwrite("clusters/%s" %best_images[index], img)
        plt.imshow(img, interpolation = 'bicubic')
        plt.xticks([]), plt.yticks([])
