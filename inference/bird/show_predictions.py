## Code to visualize predictions

import torch

## import bird? 

## First load prediction: 
all_predictions = torch.load(prediction_file)

## Load dataset
bird_dataset = birds.BirdDataset(images, ann_file) 

## Load image
image = bird_dataset[idx]
prediction = all_predictions[idx]

## Pull some code to overlay the predictions on the image
#...
