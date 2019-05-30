# Custom dataset class for use in maskrcnn-benchmark
# written by Ammon Perkes May, 2019
# For questions, find me at github.com/aperkes

import torch
import torchvision

from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.structures.segmentation_mask import SegmentationMask

from PIL import Image
import csv, ast

## Birdsong dataset class
# Once complete add this to 
# maskrcnn_benchmark/data/datasets/__init__.py
# maskrcnn_benchmark/config/paths_catalog.py

# And for testing: 
# maskrcnn_benchmark/data/datasets/evaluation/__init__.py
class birdsoundDataset(object):
    def __init__(self, ann_file, spec_dir):
        self.spec_dir = os.path.abspath(spec_dir)
        self.ann_file = os.path.abspath(ann_file)
         
        self.ann_dict = {
            'c':1,
            'n':0}
        # probably should have some sterilization here...
        self.label_list, self.box_list = parse_annotations(ann_file)
        self.images = os.listdir(spec_dir)
        self.n_images = len(self.images)
        for i in range(len(self.images)):
            self.images[i] = spec_dir + '/' + self.images[i]
        
        # Check the data and compile some internal structure of data
    def parse_annotations(self,ann_file):
        label_list = [[]] * self.n_images
        box_list = [[]] + self.n_images
        with open(ann_file,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                r_index = int(row[0])
                row_labels = ast.literal_eval(row[4])
                label_list[r_index] = [self.ann_dict[l] for l in my_labels]
                box_list = ast.literal_eval(row[3])
        return label_list, box_list

    def __getitem__(self,idx):
        # load the image as a PIL image
        image = Image.open(self.spec_dir + '/' + self.images[idx])
        boxes = self.annotations.loc[idx]['Boxes_i'] ##from annotation files...
        labels = self.annotations.loc[idx]['Labels']
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
