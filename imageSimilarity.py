import torch
import cv2
import numpy as np
from torch import  nn
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
      if sortedRes[i][0] > 0.6:
        finalRes.append(prodDict[sortedRes[i][1]])
    
    return finalRes
