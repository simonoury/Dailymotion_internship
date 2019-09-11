from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
import numpy as np
import inceptionv3_class_features
import inceptionv3_class_classification
import logging
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import optimizers
import time

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

    start = time.time()
    video_names = []
    for videos in os.listdir():
        if videos.endswith(".mp4"):
            video_names.append(videos)
    logging.basicConfig(level=logging.INFO)
    inception_v3_fv = inceptionv3_class_features.InceptionV3Embedder()
    inception_v3 = inceptionv3_class_classification.InceptionV3Embedder()
    video_names = sorted(video_names)
    print(video_names)

    for video_name in video_names:

        print(video_name)
        name_im = []

        list_images = get_images(video_name)
        os.mkdir("results/%s" %video_name)
        #os.system("mv %s results_ffmpeg/%s" %(video_name, video_name))
        model = get_model()

        image_index_map = {}
        index_image_map = {}
        name_fv_map = {}
        images_inceptionv3 = []
        counter = 0
        for name in list_images :
            print (name)
            img = cv2.imread(name)
            if img is not None:
                name_im.append(name)
                image_index_map[name]=counter
                index_image_map[counter]=name
                fv = inception_v3_fv.predict(img)
                name_fv_map[name] = fv
                images_inceptionv3.append(fv)
                counter += 1

        images_inceptionv3_stack = np.vstack(images_inceptionv3)

        images = len(list_images)
        if images <= 50:
            EPS = 8
        if 50 < images <= 100:
            EPS = 10
        if 100 < images <= 150:
            EPS = 11
        if 150 < images <= 200:
            EPS = 12
        if 200 < images <= 250:
            EPS = 12
        if 250 < images <= 300:
            EPS = 13
        if 300 < images <= 350:
            EPS = 14
        if 350 < images <= 400:
            EPS = 15
        if 400 < images <= 450:
            EPS = 16
        if 450 < images <= 500:
            EPS = 16
        if 500 < images <= 550:
            EPS = 17
        if 550 < images:
            EPS = 18

        n_clusters, n_noise = get_cluster_num(images_inceptionv3_stack, EPS)
        print("Number of clusters: ", n_clusters)
        print("Noise points: ", n_noise)

        print("Number of images: ", images)
        print("Epsilon: ", EPS)

        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(images_inceptionv3_stack)

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
                fv = name_fv_map[name]
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

        clusters=[]
        for index in range (n_clusters):
            clusters.append(best_images[index])
            '''
            img = cv2.imread(best_images[index])
            cv2.imwrite("clusters/%s" %best_images[index], img)
            plt.imshow(img, interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])
            '''

        class_list = []

        images_list = os.listdir('clusters')

        ''' Classifies the images and retrieves highest score and correspondant class (out of 1000)'''
        for img_name in clusters:
            img = cv2.imread(img_name)
            fv = inception_v3.predict(img)
            imname_class_map1[count] = img_name
            count +=1
            i = 0
            hi_i = 0
            hi_num = 0
            num = 0
            for num in fv:
                if num > hi_num:
                    hi_num = num
                    hi_i = i
                i = i+1
            class_list.append(hi_i)

        '''Maps the number of the class to actual class'''
        for class_num in class_list:
            filename = 'inception_class.txt'
            f = open(filename, 'r')
            lines = f.readlines()
            print(lines[class_num])

        class_dict = {}
        hi_class_num = 0
        imname_class_map = {}
        count2 = 0
        for class_ in class_list:
            if class_ in class_dict:
                class_dict[class_] += 1
                imname_class_map[class_].append(imname_class_map1[count2])
                count2+=1
            else:
                class_dict[class_] = 1
                imname_class_map[class_] = [imname_class_map1[count2]]
                count2 += 1

            if hi_class_num < class_dict[class_]:
                hi_class = class_
                hi_class_num = class_dict[class_]
        print(hi_class, hi_class_num)
        print(imname_class_map[hi_class])

        maj_class=[]
        for name_image in imname_class_map[hi_class]:
            maj_class.append(name_image)

        model = get_model()
        score_image_map = {}
        rank_dict = {}
        score_imageClass_map = {}

        for image_name in clusters:
            if image_name.endswith('.png'):
                fv = name_fv_map[image_name]
                fv = np.asarray(fv)
                input_vector = np.zeros(shape=(1,2048))
                input_vector[0,:]=fv
                score = model.predict(input_vector)
                score_image_map[image_name] = score
        images_list = []

        print("\n TOP IMAGES: ")
        map = sorted(score_image_map.items(), reverse = True, key = lambda item: item[1])
        for key, val in map[:1]:
            print("%s: %s" %(key, val))
            images_list.append(key)
        top5 = images_list[:1]
        for name in top5:
            img = cv2.imread(name)
            cv2.imwrite("results/%s/%s" %(video_name, name), img)
            plt.imshow(img, interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])

        for image_name_class in maj_class:
            fv = name_fv_map[image_name_class]
            fv = np.asarray(fv)
            input_vector = np.zeros(shape=(1,2048))
            input_vector[0,:]=fv
            score_class = model.predict(input_vector)
            score_imageClass_map[image_name_class] = score_class
        images_list_class = []

        print("\n TOP IMAGES FROM MAJ CLASS")
        map_ = sorted(score_imageClass_map.items(), reverse = True, key = lambda item: item[1])
        for key_, value_ in map_[:5]:
            print("%s: %s" %(key_, value_))
            images_list_class.append(key_)
        top5_class = images_list_class[:5]
        for name in top5_class:
            img = cv2.imread(name)
            cv2.imwrite("results/%s/%s" %(video_name, name), img)
            plt.imshow(img, interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])


        for files in os.listdir():
            if files.endswith('.png'):
                os.remove(files)
        end = time.time()
    print("Run time:", end-start)
