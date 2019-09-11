from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions
import numpy as np
import cv2

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
