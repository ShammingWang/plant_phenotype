import detectron2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

import os
import cv2
from os import listdir
from os.path import isfile, join

cfg = get_cfg()

# import PointRend project
import sys

sys.path.insert(1, "detectron2_dc/projects/PointRend")
import point_rend

point_rend.add_pointrend_config(cfg)
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
# cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/pointrend_rcnn_R_50_FPN_3x.yaml"))
cfg.merge_from_file(
    "detectron2_dc/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_R_50_FPN_3x_coco.yaml")
# config_file = pkg_resources.resource_filename(__name__, './pointrend_rcnn_R_50_FPN_3x_coco.yaml')
# cfg.merge_from_file(config_file)

cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.MODEL.POINT_HEAD.NUM_CLASSES = 2

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.WEIGHTS = "./output/bean/model_final.pth"
cfg.MODEL.DEVICE = 'cpu'
predictor = DefaultPredictor(cfg)
im = cv2.imread("./bean/train/plant_005.png.jpg")
outputs = predictor(im)

from detectron2.data.datasets import register_coco_instances
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

import cv2

# register_coco_instances("bean_train", {}, "./bean/train/coco_train.json", "./bean/train")
# MetadataCatalog.get("bean_train").set(thing_classes=["_background_", "leaf"])

# We can use `Visualizer` to draw the predictions on the image.
# v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[-1]), scale=1.2)
v = Visualizer(im[:, :, ::-1], MetadataCatalog.get("bean_train"), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2.imshow("visualize", out.get_image()[:, :, ::-1])
cv2.waitKey(0)
