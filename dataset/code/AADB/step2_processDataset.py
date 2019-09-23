import pandas as pd
import numpy as np
import pickle
import cv2
from matplotlib import pyplot as plt
import logging
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions


'''Exports data to a smaller CSV fille with Image_number, Image_name and the Mean_Score'''
data = pd.read_csv("dataset.csv", index_col = None)
first = data[["NO", "imgName", "meanScore"]]
export_csv = first.to_csv (r'/Users/s.oury/Code/thumbnails_selection/datasets/AADB/dataset_AADB_clear.csv', index = None, header = True)



'''2 functions that extract thge Image_name and the Mean_Score'''
def image_name(row):
    df = pd.read_csv('dataset_AADB_clear.csv', index_col = None)
    data = df.loc[row, ["NO", "imgName", "meanScore"]]
    number = data["NO"]
    imagename = data["imgName"]
    return imagename
def mean_score(row):
    df = pd.read_csv('dataset_AADB_clear.csv', index_col = None)
    data = df.loc[row, ["NO", "imgName", "meanScore"]]
    meanscore = data["meanScore"]
    return meanscore

'''Function reads Image with OpenCv2'''
def get_image (row):
    bgr_img = cv2.imread('datasetimages_originalsize/%s' %image_name(row))
    #rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    flip_image = cv2.flip(bgr_img, 1)
    return bgr_img, flip_image

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

    data_image = []
    data_label = []
    fv = []

    for x in range (data.shape[0]):
        print("sample {}/{}".format(x,data.shape[0]))
        rgb_img, flip_image = get_image(x)

        fv.append(inception_v3.predict(rgb_img))
        fv.append(inception_v3.predict(flip_image))

        data_label.append(mean_score(x))
        data_label.append(mean_score(x))

    pickle.dump(fv, open("fv_inceptionv3.p", "wb"))
    pickle.dump(data_label, open("label_inceptionv3.p", "wb"))

    print('fv vector:')
    print(len(fv))
    print('Score:')
    print(len(data_label))
