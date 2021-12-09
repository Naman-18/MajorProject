from keras.applications import vgg16
from keras.preprocessing.image import load_img,img_to_array
from keras.models import Model
from keras.applications.imagenet_utils import preprocess_input
 
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
def imageSimilarity(files,prodDict):
    importedImages = []
    imgs_model_width, imgs_model_height = 224, 224
    vgg_model = vgg16.VGG16(weights='imagenet')
    feat_extractor = Model(inputs=vgg_model.input,outputs=vgg_model.get_layer("fc2").output)
    for i in files:
        t1 = load_img(i, target_size=(imgs_model_width, imgs_model_height))
        numpy_image = img_to_array(t1)
        image_batch = np.expand_dims(numpy_image, axis=0)
        importedImages.append(image_batch)
    images = np.vstack(importedImages)
    processed_imgs = preprocess_input(images.copy())
    imgs_features = feat_extractor.predict(processed_imgs)
    cosSimilarities = cosine_similarity(imgs_features)
    cos_similarities_df = pd.DataFrame(cosSimilarities, columns=files, index=files)
    cos_similarities_df.head()
    sortedRes = []
    finalRes  = []
    for i in range(1,len(files)):
        sortedRes.append([cos_similarities_df[files[0]][files[i]],prodDict[files[i]]])
    sortedRes.sort(reverse=True)
    for i in range(0,8):
        finalRes.append(sortedRes[i][1])
    return finalRes