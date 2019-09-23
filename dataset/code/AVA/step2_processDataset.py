import pandas as pd
import gcsfs
import cv2
import pickle
import logging
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions
from matplotlib import pyplot as plt

df = pd.read_csv("/Users/s.oury/Code/thumbnails_selection/datasets/AVA/dataset_AVA_clear2.csv", index_col = None)

def get_data (row):
    data = df.loc[row, ["NO","img_ID","ratings_1","ratings_2","ratings_3","ratings_4","ratings_5","ratings_6","ratings_7","ratings_8","ratings_9","ratings_10", "tag_1", "tag_2"]]
    No=data["NO"]
    img_id=data["img_ID"]
    rating1=data["ratings_1"]
    rating2=data["ratings_2"]
    rating3=data["ratings_3"]
    rating4=data["ratings_4"]
    rating5=data["ratings_5"]
    rating6=data["ratings_6"]
    rating7=data["ratings_7"]
    rating8=data["ratings_8"]
    rating9=data["ratings_9"]
    rating10=data["ratings_10"]
    tag1=data["tag_1"]
    tag2=data["tag_2"]
    meanscore = (rating1*1+rating2*2+rating3*3+rating4*4+rating5*5+rating6*6+rating7*7+rating8*8+rating9*9+rating10*10)/(rating1+rating2+rating3+rating4+rating5+rating6+rating7+rating8+rating10)
    return No, img_id, meanscore, tag1, tag2

def get_image (img_id):
    img_ = cv2.imread('/Users/s.oury/Code/thumbnails_selection/datasets/AVA/images/%s.jpg' %img_id)
    img_flip = cv2.flip(img_, 1)
    return img_, img_flip


class InceptionV3Embedder:

  '''class implement image embedding based on tensorflow keras inception v3 model'''
  def __init__(self):

    '''class constructor'''
    self.reference_width = 299
    self.reference_height = 299
    self.base_model = InceptionV3(weights='imagenet',include_top=True, input_shape=(self.reference_width, self.reference_height, 3))
    self.model = Model(inputs=self.base_model.input, outputs=self.base_model.get_layer('avg_pool').output)

  def predict(self,img_raw):
    '''embedding raw input image into a 2048 feature vector
    img_raw: input raw images
    feature_vector: output feature vector'''
    img_raw = cv2.resize(img_raw, (self.reference_width, self.reference_height), interpolation = cv2.INTER_AREA)
    img = preprocess_input(img_raw)
    batch = np.zeros((1,self.reference_width,self.reference_width,3))
    batch[0,:,:,:] = img
    feature_vector = np.squeeze(self.model.predict(batch))
    return feature_vector


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    inception_v3 = InceptionV3Embedder()

    data_tag1 = []
    data_tag2 = []
    data_image = []
    data_label = []
    NO = []
    img_ID = []


    for x in range (255008):
        if x%100==0:
            print("sample {}/{}".format(x,255008))
        No, img_id, meanscore, tag1, tag2 = get_data(x)
        try:
            I = cv2.imread('images/%s.jpg' %img_id)
            if I is not None:

                img_ID.append(img_id)
                img_ID.append(img_id)

                data_tag1.append(tag1)
                data_tag1.append(tag1)

                data_tag2.append(tag2)
                data_tag2.append(tag2)

                img, flip_img = get_image(img_id)

                data_image.append(inception_v3.predict(img))
                data_image.append(inception_v3.predict(flip_img))

                data_label.append(meanscore)
                data_label.append(meanscore)

        except Exception as e:
            print(e)
            continue

    pickle.dump(data_tag1, open("data_tags1.p", "wb"))
    pickle.dump(data_tag2, open("data_tags2.p", "wb"))
    pickle.dump(data_image, open("data_images.p", "wb"))
    pickle.dump(data_label, open("data_labels.p", "wb"))
    pickle.dump(img_ID, open("image_IDs.p", "wb"))



    print("SUCCESS:")
    print("Tags1:")
    print(len(data_tag1))
    print(data_tag1[100])
    print("Tags2:")
    print(len(data_tag2))
    print(data_tag2[100])
    print("Images:")
    print(len(data_image))
    print(data_image[100])
    print("Labels:")
    print(len(data_label))
    print(data_label[100])
    print("Image_ID:")
    print(len(img_ID))
    print(img_ID[100])
