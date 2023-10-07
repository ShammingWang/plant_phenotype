import detectron2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

# import PointRend project
import sys
sys.path.insert(1, "detectron2_dc/projects/PointRend")
import point_rend

import os
import cv2
from os import listdir
from os.path import isfile, join

cfg = get_cfg()
point_rend.add_pointrend_config(cfg)
cfg.merge_from_file(
    "detectron2_dc/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_R_50_FPN_3x_coco.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
cfg.MODEL.POINT_HEAD.NUM_CLASSES = 2

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9
cfg.MODEL.WEIGHTS = "./output/bean/model_final.pth"
cfg.MODEL.DEVICE = 'cpu'  # 使用CPU进行预测

predictor = DefaultPredictor(cfg)

imgPath = './bean/val/'
maskPath = './output_bean/'
x = listdir(imgPath)
onlyfiles = [f for f in listdir(imgPath) if isfile(join(imgPath, f)) and f.endswith(".jpg")]

for iter in range(len(onlyfiles)):

    fileName = imgPath + onlyfiles[iter]
    print('fileName: ', fileName)
    newDir = os.path.splitext(onlyfiles[iter])[0]
    os.system("mkdir output_bean/" + newDir)
    maskDir = maskPath + newDir + '/'
    print('maskDir: ', maskDir)

        im = cv2.imread(fileName)
        outputs = predictor(im)  # 进行预测

        # print(str(outputs["instances"].pred_boxes))
        # print(str(outputs["instances"].pred_keypoints))

        masks = outputs["instances"].to("cpu").pred_masks
        masks = np.asarray(masks)

    for idx, mask in enumerate(masks):
        maskName = maskDir + "sub_" + str(idx) + ".png"
        print('maskName: ', maskName)
        cv2.imwrite(maskName, mask * 255)
