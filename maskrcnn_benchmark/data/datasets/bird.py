# Custom dataset class for use in maskrcnn-benchmark
# written by Ammon Perkes May, 2019
# For questions, find me at github.com/aperkes

import torch
import torchvision

from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.structures.segmentation_mask import SegmentationMask

from PIL import Image
import csv, ast, os

## Birdsong dataset class
# Once complete add this to 
# maskrcnn_benchmark/data/datasets/__init__.py
# maskrcnn_benchmark/config/paths_catalog.py

# And for testing: 
# maskrcnn_benchmark/data/datasets/evaluation/__init__.py
class BirdDataset(torchvision.datasets.coco.CocoDetection):
    def __init__(
    self, ann_file, root,
    remove_images_without_annotations = False,transforms=None
    ):
        super(BirdDataset, self).__init__(root, ann_file)
        self.root = os.path.abspath(root)
        self.ann_file = os.path.abspath(ann_file) 
        self.ann_dict = {
            'c':1,
            'n':0}
        # probably should have some sterilization here...
        self.images = os.listdir(self.root)
        self.n_images = len(self.images)
        self.label_list, self.box_list = self.parse_annotations(ann_file)
        for i in range(len(self.images)):
            self.images[i] = self.root + '/' + self.images[i]
        self.transforms = transforms 
        self.id_to_img_map = list(range(self.n_images))
        # Check the data and compile some internal structure of data
    def parse_annotations(self,ann_file):
        label_list = [[]] * self.n_images
        box_list = [[]] * self.n_images
        with open(ann_file,'r') as f:
            reader = csv.reader(f)
            head = next(reader)
            for row in reader:
                r_index = int(row[0])
                row_labels = ast.literal_eval(row[4])
                label_list[r_index] = [self.ann_dict[l] for l in row_labels]
                box_list[r_index] = ast.literal_eval(row[3])
        return label_list, box_list

    def __getitem__(self,idx):
        # load the image as a PIL image
        image = Image.open(self.images[idx])
        boxes = self.box_list[idx]
        labels = self.label_list[idx]
        # and labels
        # I don't quite understand the label construction either
        labels = torch.tensor(labels)
        # e.g. boxes = [[0,0,10,10],[10,20,50,50],...,[x1,y1,x2,y2]]
        # create a boxlist from the boxes
        boxlist = BoxList(boxes, image.size, mode="xyxy")
        boxlist.add_field("labels",labels)

        ## I don't quite understand this part
        if self.transforms:
            image, boxlist = self.transforms(image,boxlist)

        return image, boxlist, idx

    ## Not sure why I need this, but I seem to need this...
    def __len__(self):
        return len(self.images)

    def get_img_info(self,idx):
        # This might not be maximally efficient, but I think it's ok
        image = Image.open(self.images[idx])
        img_height = image.height
        img_width = image.width
        # Get img_height and img_width. 
        # Used to split batches by aspect ration for efficiency.
        return {"height":img_height, "width": img_width}
