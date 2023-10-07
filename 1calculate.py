import os
import cv2
from PIL import Image
import numpy as np
import math

path = "./images/"

# plant_phenotype
def Rotate2(pt, alpha):
    x1 = pt[0]
    y1 = pt[1]
    x2 = x1 * math.cos(alpha) - y1 * math.sin(alpha)
    y2 = x1 * math.sin(alpha) + y1 * math.cos(alpha)
    return x2, y2


def rotateContour(img, contour, center, alpha):
    alpha = (alpha - 90) / 180 * math.acos(-1.0)
    c = center
    image = np.zeros_like(img)
    n = contour.shape[0]
    list_x = []
    list_y = []
    for i in range(n):
        x1 = contour[i][0][0]
        y1 = contour[i][0][1]
        x2, y2 = Rotate2((x1 - c[0], y1 - c[1]), alpha)
        x2 += c[0]
        y2 += c[1]
        list_x.append(x2)
        list_y.append(y2)
        # for dy in range(-1, 2):
        #     for dx in range(-1, 2):
        #         image[int(y2) + dy][int(x2) + dx] = 255
    length = max(list_x) - min(list_x)
    width = max(list_y) - min(list_y)
    if width > length:
        length, width = width, length
    return length, width


def findLongestContour(contours):
    n = len(contours)
    ans = 0
    max_val = 0
    for i in range(n):
        contour = contours[i]
        if contour.shape[0] > max_val:
            max_val = contour.shape[0]
            ans = i
    return ans


for fn in os.listdir(path):
    path_fn = path + fn
    img = Image.open(path_fn)  # 通过操作系统内置的PIL打开图片
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thres, img_bin = cv2.threshold(img_gray, 130, 255, cv2.THRESH_BINARY_INV)
    rows, cols = img_bin.shape[:2]

    img_bin[0:100, 0:] = 0
    img_bin[rows - 100:rows, 0:] = 0
    img_bin[0:, 0:100] = 0
    img_bin[0:, cols - 100:cols] = 0
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_draw = img.copy()
    cv2.drawContours(img_draw, contours, -1, (0, 255, 0), 2)

    # imgs = np.hstack([img, img_draw])

    kc = 4 / 311

    index = findLongestContour(contours)
    longestContour = contours[index]

    img_draw = img.copy()
    ellipse = cv2.fitEllipse(longestContour)
    cv2.ellipse(img_draw, ellipse, (0, 255, 0), 2)

    # print(ellipse[2])
    # center = (ellipse[0][0], ellipse[0][1])
    # angle = ellipse[2]
    #
    # h, w = img.shape[:2]
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # rotated = cv2.warpAffine(img, M, (w, h),
    #                          flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    length, width = rotateContour(img_gray, longestContour, ellipse[0], ellipse[2])
    cv2.namedWindow('img_draw', cv2.WINDOW_FREERATIO)
    cv2.imshow('img_draw', img_draw)
    # cv2.namedWindow('rotated', cv2.WINDOW_FREERATIO)
    # cv2.imshow('rotated', rotated)

    print(fn)
    # print('长轴为', max(ellipse[1]) * kc)
    # print('短轴为', min(ellipse[1]) * kc)
    print('长为', length * kc, "cm")
    print('宽为', width * kc, "cm")
    print('周长为', cv2.arcLength(longestContour, True) * kc, "cm")
    print('面积为', cv2.contourArea(longestContour) * kc * kc, "square cm")

    key = cv2.waitKey(0)
    if key == 27:
        break
