import matplotlib.pyplot as plt
# from typing_extensions import final
# from keras.applications import vgg16
# from keras.preprocessing.image import load_img,img_to_array
# from keras.models import Model
# from keras.applications.imagenet_utils import preprocess_input
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd

# def imageSimilarity(files,prodDict):
#     importedImages = []
#     imgs_model_width, imgs_model_height = 224, 224
#     vgg_model = vgg16.VGG16(weights='imagenet')
#     feat_extractor = Model(inputs=vgg_model.input,outputs=vgg_model.get_layer("fc2").output)
#     for i in files:
#         t1 = load_img(i, target_size=(imgs_model_width, imgs_model_height))
#         numpy_image = img_to_array(t1)
#         image_batch = np.expand_dims(numpy_image, axis=0)
#         importedImages.append(image_batch)
#     images = np.vstack(importedImages)
#     processed_imgs = preprocess_input(images.copy())
#     imgs_features = feat_extractor.predict(processed_imgs)
#     cosSimilarities = cosine_similarity(imgs_features)
#     cos_similarities_df = pd.DataFrame(cosSimilarities, columns=files, index=files)
#     cos_similarities_df.head()
#     sortedRes = []
#     finalRes  = []
#     for i in range(1,len(files)):
#         sortedRes.append([cos_similarities_df[files[0]][files[i]],prodDict[files[i]]])
#     sortedRes.sort(reverse=True)
    
#     for i in range(0,8):
#         # print(sortedRes[i][0])
#         finalRes.append(sortedRes[i][1])
#     return finalRes
import torch
import cv2
import numpy as np
import os
from torch import optim, nn
from torchvision import models, transforms
def cosine_similarity(list_1, list_2):
  return np.dot(list_1, list_2)/(np.linalg.norm(list_1)*np.linalg.norm(list_2))
class FeatureExtractor(nn.Module):
  def __init__(self, model):
    super(FeatureExtractor, self).__init__()
    self.features = list(model.features)
    self.features = nn.Sequential(*self.features)
    self.pooling = model.avgpool
    self.flatten = nn.Flatten()
    self.fc = model.classifier[:4]
  
  def forward(self, x):
    out = self.features(x)
    out = self.pooling(out)
    out = self.flatten(out)
    out = self.fc(out) 
    return out 
def TestImages(files,prodDict):
    model = models.vgg16(pretrained=True)
    new_model = FeatureExtractor(model)
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
    new_model = new_model.to(device)
    feat = []
    temp = []
    transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.CenterCrop(size = (224,224)),
    transforms.Resize(224),
    transforms.ToTensor()])
    for i in files:
        image_ = cv2.imread(i)
        image = cv2.cvtColor(image_, cv2.COLOR_BGR2RGB)
        img = transform(image)
        # print(img.shape)
        img = img.reshape(1, 3, 224, 224)
        img = img.to(device)
        with torch.no_grad():
            feature=new_model(img)
        feat.append(feature.cpu().detach().numpy().reshape(-1))
    features = np.array(feat)
    sortedRes = []
    finalRes  = []
    for i in range(1,len(files)):
        sortedRes.append([cosine_similarity(features[0],features[i]),files[i]])
    sortedRes.sort(reverse=True)
    for i in range(0,8):
        print(sortedRes[i][0])
        finalRes.append(prodDict[sortedRes[i][1]])
    # plt.imshow(files[0])
    return finalRes
