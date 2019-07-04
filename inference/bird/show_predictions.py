## Code to visualize predictions

import torch
from maskrcnn_benchmark.data.datasets import bird
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

## get files
root_dir = '/home/ammon/Documents/Scripts/maskrcnn-benchmark'
ann_file = root_dir + '/maskrcnn_benchmark/data/datasets/bird/bird_annotations.json'
image_dir = root_dir + '/maskrcnn_benchmark/data/datasets/bird/images'
prediction_file = root_dir + '/inference/bird/predictions.pth'

## First load prediction: 
all_predictions = torch.load(prediction_file)

## Load dataset 
bird_dataset = bird.BirdDataset(ann_file,image_dir)

## Load image, with its targets and predictions
try:
    i = sys.argv[1]
except:
    i = 0

img,target,idx = bird_dataset[i]
target_boxes = target.bbox
predictions = all_predictions[i]

## I might need to do some checking here eventually...
predicted_boxes = predictions.bbox

fig,ax = plt.subplots()
#img = np.log(img)
ax.imshow(img,vmax = 10)


#Add Predicted Rectangles
for p in predicted_boxes:
    x0,y0,x1,y1 = p
    w = x1-x0
    h = y1-y0
    rect = patches.Rectangle((x0,y0),w,h,linewidth=1,edgecolor='r',facecolor='red',alpha=.20)
    ax.add_patch(rect)

#Add Target Rectangles
for t in target_boxes:
    x0,y0,x1,y1 = t
    w = x1-x0
    h = y1-y0
    rect = patches.Rectangle((x0,y0),w,h,linewidth=1,edgecolor='w',facecolor='none')
    ax.add_patch(rect)

plt.show()
#fig.savefig('test.png',dpi=150)
