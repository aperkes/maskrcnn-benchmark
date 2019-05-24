# Custom dataset class for use in maskrcnn-benchmark
# written by Ammon Perkes May, 2019
# For questions, find me at github.com/aperkes

import torch
import torchvision

from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.structures.segmentation_mask import SegmentationMask


## Birdsong dataset class
# Once complete add this to 
# maskrcnn_benchmark/data/datasets/__init__.py
# maskrcnn_benchmark/config/paths_catalog.py

# And for testing: 
# maskrcnn_benchmark/data/datasets/evaluation/__init__.py
class birdsoundDataset(object):
    def __init__(self, ann_file, spec_dir):
        # Check the data and compile some internal structure of data
         
    def __getitem__(self,idx):
# load the image as a PIL image
        image = ...

        return image, boxlist, idx

    def get_img_info(self,idx):
        # Get img_height and img_width. 
        # Used to split batches by aspect ration for efficiency.
        return {"height":img_height, "width": img_width}
