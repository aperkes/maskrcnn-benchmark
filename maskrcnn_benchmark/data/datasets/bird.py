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
        # probably should have some sterilization here...
        self.images = os.listdir(self.root)
        self.n_images = len(self.images)
        for i in range(len(self.images)):
            self.images[i] = self.root + '/' + self.images[i]
        self.transforms = transforms 
        self.id_to_img_map = list(range(self.n_images))
        self.json_category_id_to_contiguous_id = {1:1,2:2}
        self.contiguous_category_id_to_json_id = {1:1,2:2}
        # Check the data and compile some internal structure of data

    def __getitem__(self,idx):
        img, anno = super(BirdDataset, self).__getitem__(idx)

        # filter crowd annotations (doesn't apply to bird Dataset)
        anno = [obj for obj in anno if obj["iscrowd"] == 0]

        # load the image as a PIL image
        boxes = [obj["bbox"] for obj in anno]
        boxes = torch.as_tensor(boxes).reshape(-1, 4) # in case of no boxes
        target = BoxList(boxes, img.size, mode="xywh").convert("xyxy")

        classes = [obj["category_id"] for obj in anno]
        #print(classes)
        # Don't think I need this bit (and it's not coded)
        #classes = [self.json_category_id_to_contiguous_id[c] for c in classes]
        classes = torch.tensor(classes)
        target.add_field("labels", classes)
        
        if anno and "segmentation" in anno[0]:
            masks = [obj["segmentation"] for obj in anno]
            masks = SegmentationMask(masks, img.size, mode='poly')
            target.add_field("masks", masks)

        target = target.clip_to_image(remove_empty=True)

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        #print('pulling img',idx)
        #print(target)
        return img, target, idx

    def get_img_info(self,idx):
        # This might not be maximally efficient, but I think it's ok
        image = Image.open(self.images[idx])
        img_height = image.height
        img_width = image.width
        # Get img_height and img_width. 
        # Used to split batches by aspect ration for efficiency.
        return {"height":img_height, "width": img_width}
