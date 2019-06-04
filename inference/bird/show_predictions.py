## Code to visualize predictions

import torch
from maskrcnn_benchmark.data.datasets import bird

## get files
root_dir = '/home/ammon/Documents/Scripts/maskrcnn-benchmark'
ann_file = root_dir + '/data/datasets/bird_annotation.csv'
image_dir = root_dir + '/data/datasets/bird/images'
prediction_file = root_dir + '/inference/bird/predictions0.pth'

## First load prediction: 
all_predictions = torch.load(prediction_file)

## Load dataset
bird_dataset = birds.BirdDataset(ann_file,images_dir)

## Load image
image = bird_dataset[idx]
prediction = all_predictions[idx]

## Pull some code to overlay the predictions on the image
#...
