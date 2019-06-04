## Another script to convert old annotation into json
# Also handy because it acts as the format for coco json: 
import sys, json
import bird

ann_file = sys.argv[1]

data = {
    "info":{},
    "licenses":[],
    "images":[],
    "annotations":[],
    "categories":[]
}

data["info"] = {
    "description": "Cowbird Song Annotations",
    "url": None,
    "version":"1.0",
    "year":2019,
    "contributor":"aperkes",
    "date_created":"2019/01/01"
}


