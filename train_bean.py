# Some basic setup:
# Setup detectron2 logger
from detectron2.utils.logger import setup_logger

setup_logger()

# import some common libraries
import os
# from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog

from detectron2.data.datasets import register_coco_instances

# register_coco_instances("bean", {}, "./bean/bean_test.json", "./bean")
register_coco_instances("bean_train", {}, "./bean/train/coco_train.json", "./bean/train")
register_coco_instances("bean_val", {}, "./bean/val/coco_val.json", "./bean/val")
# 注册coco数据集

# shamming
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator

# import PointRend project
import sys

sys.path.insert(1, "detectron2_dc/projects/PointRend")
import point_rend


class MyTrainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        return COCOEvaluator(dataset_name, cfg, True, output_folder)


cfg = get_cfg()
point_rend.add_pointrend_config(cfg)

cfg.merge_from_file(
    "detectron2_dc/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_R_50_FPN_3x_coco.yaml")
cfg.DATASETS.TRAIN = ("bean_train",)
cfg.DATASETS.TEST = ("bean_val", )
MetadataCatalog.get("bean_train").set(thing_classes=["_background_", "leaf"])  # 人为的添加一类作为背景类

cfg.DATALOADER.NUM_WORKERS = 0  # 不使用多线程
cfg.MODEL.WEIGHTS = "./pre_train/model_final_edd263_pointrend_r50_3lr.pkl"  # 加载预训练模型
cfg.MODEL.MASK_ON = True
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 10  # 300 iterations seems good enough for this toy dataset; you will need to train longer
# for a practical dataset
cfg.SOLVER.WARMUP_ITERS = 300
cfg.SOLVER.STEPS = (1000, )  # do not decay learning rate
cfg.SOLVER.GAMMA = 0.05

cfg.INPUT.FORMAT = "RGB"

cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128  # faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # only has one class (ballon). (see
# https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.MODEL.POINT_HEAD.NUM_CLASSES = 2
# NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1

cfg.TEST.EVAL_PERIOD = 200

cfg.OUTPUT_DIR = "./output/bean_test"
cfg.MODEL.DEVICE = 'cpu'  # 设置用cpu进行训练

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

trainer = MyTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()
