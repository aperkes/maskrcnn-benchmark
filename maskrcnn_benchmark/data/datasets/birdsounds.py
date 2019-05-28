# Custom dataset class for use in maskrcnn-benchmark
# written by Ammon Perkes May, 2019
# For questions, find me at github.com/aperkes

import torch
import torchvision

from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.structures.segmentation_mask import SegmentationMask

from PIL import Image

## Birdsong dataset class
# Once complete add this to 
# maskrcnn_benchmark/data/datasets/__init__.py
# maskrcnn_benchmark/config/paths_catalog.py

# And for testing: 
# maskrcnn_benchmark/data/datasets/evaluation/__init__.py
class birdsoundDataset(object):
    def __init__(self, ann_file, spec_dir):
        self.spec_dir = spec_dir

        
        self.annotations = ...
        # probably should have some sterilization here...
        self.images = os.listdir(spec_dir)
        
        # Check the data and compile some internal structure of data
                 
    def __getitem__(self,idx):
        # load the image as a PIL image
        image = Image.open(self.spec_dir + '/' + self.images[idx])
        boxes = [[]] ##from annotation files...
        # and labels
        # I don't quite understand the label construction either
        labels = torch.tensor([10,20])
        # e.g. boxes = [[0,0,10,10],[10,20,50,50],...,[x1,y1,x2,y2]]
        # create a boxlist from the boxes
        boxlist = BoxList(boxes, image.size, mode="xyxy")
        boxlist.add_field("labels",labels)

        ## I don't quite understand this part
        if self.transforms:
            image, boxlist = self.transforms(image,boxlist)

        return image, boxlist, idx

    def get_img_info(self,idx):
        # Get img_height and img_width. 
        # Used to split batches by aspect ration for efficiency.
        return {"height":img_height, "width": img_width}
