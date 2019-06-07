## Another script to convert old annotation into json
# Also handy because it acts as the format for coco json: 
import sys, json
import oldBird

ann_file = sys.argv[1]
spec_dir = sys.argv[2]

old_database = oldBird.BirdDataset(ann_file,spec_dir)
n_images = old_database.n_images

data = {
    "info":{},
    "licenses":[{}] * n_images,
    "images":[{}] * n_images,
    "annotations":[{}] * annotations,
    "categories":[{}] * n_categories
}

data["info"] = {
    "description": "Cowbird Song Annotations",
    "url": None,
    "version":"1.0",
    "year":2019,
    "contributor":"aperkes",
    "date_created":"2019/01/01"
}

data["categories"]: [
    {"supercategory":"background","id":1,"name":"noise"},
    {"supercategory":"cowbird","id":2,"name":"vocalization"}
]

ann_count = 0
for i in range(n_images):
    image, _, idx = old_database[i]
    labels = old_database.label_list[i]
    boxes = old_database.box_list[i]
    data["licenses"][i] = {
        "url": None,
        "id": idx,
        "name": "Property of Schmidt/Kostas"

    data["images"][i] = {
        "license":i,
        "file_name":old_database.images[i],
        "coco_url":None,
        "height":image.height,
        "width":image.width,
        "date_captured":"2019",
        "flickr_url":None,
        "id":idx
    }

    n_annotations = len(labels)
    for a in range(n_annotations):
        [x1,y1,x2,y2] = boxes[a]
        width = x2 - x1
        height = y2 - y1
        ann = {
            "segmentations":[[]],
            "area": width * height,
            "iscrowd":0,
            "image_id": idx,
            "bbox":[x1,y1,width,height],
            "category_id":labels[a] + 1
            "id": ann_count
        },
        ann_count += 1
        data["annotations"].append(ann)
        
with open('output.json', 'w') as outfile:
    json.dump(data,outfile)
json.dump(data)
