import cv2
import numpy as np
import math

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


def f1(x, y):
    return x + y  # ///// p1最小 p4 最大


def f2(x, y):
    return x - y  # \\\\\  p2 最大 p4 最小


def getSrcPts(img):
    rows, cols = img.shape[:2]
    dst = np.zeros((rows, cols), np.uint8)
    # dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    p1_x = cols
    p1_y = rows

    p2_x = 0
    p2_y = rows

    p3_x = cols
    p3_y = 0

    p4_x = 0
    p4_y = 0
    # ope = cv2.morphologyEx(ori, cv2.MORPH_OPEN, k)
    for i in range(rows):
        for j in range(cols):
            b, g, r = img[i, j]
            if b > 140 and r < 120:
                dst[i, j] = 255
                if f1(j, i) < f1(p1_x, p1_y):
                    p1_x = j
                    p1_y = i
                if f1(j, i) > f1(p4_x, p4_y):
                    p4_x = j
                    p4_y = i
                if f2(j, i) < f2(p3_x, p3_y):
                    p3_x = j
                    p3_y = i
                if f2(j, i) > f2(p2_x, p2_y):
                    p2_x = j
                    p2_y = i

    # k = np.ones((2, 2), np.uint8)
    # dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, k)

    # cv2.circle(img, (p1_x, p1_y), 2, (0, 0, 255), 2, 8, 0)
    # cv2.circle(img, (p2_x, p2_y), 2, (0, 0, 255), 2, 8, 0)
    # cv2.circle(img, (p3_x, p3_y), 2, (0, 0, 255), 2, 8, 0)
    # cv2.circle(img, (p4_x, p4_y), 2, (0, 0, 255), 2, 8, 0)

    # min = np.array([78, 43, 46])  # 设置范围下限
    # max = np.array([99, 255, 255])  # 设置范围上限
    # mask = cv2.inRange(img, min, max)  # 制作mask
    # res = cv2.bitwise_and(img, img, mask=mask)  # 用带掩膜的与操作进行计算得到我们想要的结果

    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    cv2.circle(dst, (p1_x, p1_y), 2, (0, 255, 0), 2, 8, 0)
    cv2.circle(dst, (p2_x, p2_y), 2, (0, 255, 0), 2, 8, 0)
    cv2.circle(dst, (p3_x, p3_y), 2, (0, 255, 0), 2, 8, 0)
    cv2.circle(dst, (p4_x, p4_y), 2, (0, 255, 0), 2, 8, 0)
    cv2.line(dst, (p1_x, p1_y), (p2_x, p2_y), (0, 0, 255), 2, 8, 0)
    cv2.line(dst, (p1_x, p1_y), (p3_x, p3_y), (0, 0, 255), 2, 8, 0)
    cv2.line(dst, (p2_x, p2_y), (p4_x, p4_y), (0, 0, 255), 2, 8, 0)
    cv2.line(dst, (p4_x, p4_y), (p3_x, p3_y), (0, 0, 255), 2, 8, 0)

    # cv2.imshow("img", img)
    cv2.imshow("dst", dst)

    # cv2.waitKey(0)
    return [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)]


def binary(src):
    rows, cols = src.shape[:2]
    ans = np.zeros((rows, cols), np.uint8)
    for i in range(rows):
        for j in range(cols):
            b, g, r = src[i, j]
            if g > 80 and b < 50:
                ans[i, j] = 255

    # k = np.ones((2, 2), np.uint8)
    # ans = cv2.morphologyEx(ans, cv2.MORPH_OPEN, k)
    return ans


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


img = cv2.imread('./leaf.png', cv2.IMREAD_COLOR)
img = cv2.resize(img, (720, 720))

cv2.imshow('img', img)

pts1 = getSrcPts(img)
rows, cols = img.shape[:2]
dst = np.zeros_like(img)
pts2 = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols -1)]



# cv2.imshow('img', img)


pts1 = np.array(pts1)
pts2 = np.array(pts2)
matrix, status = cv2.findHomography(pts1, pts2)
img_transform = cv2.warpPerspective(img, matrix, (cols, rows))  # (w, h)

cv2.imshow("img_transform", img_transform)


img_bin = binary(img_transform)
cv2.imshow("img_bin", img_bin)

contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


index = findLongestContour(contours)
longestContour = contours[index]

img_draw = img_transform.copy()
cv2.drawContours(img_draw, [longestContour], -1, (0, 255, 0), 2)
cv2.imshow("img_draw", img_draw)

img_draw = img_transform.copy()
ellipse = cv2.fitEllipse(longestContour)
cv2.ellipse(img_draw, ellipse, (0, 255, 0), 2)
cv2.imshow("img_draw_ellipse", img_draw)

length, width = rotateContour(img_bin, longestContour, ellipse[0], ellipse[2])
kc = 25 * 0.5 / rows
print('长为', length * kc, "cm")
print('宽为', width * kc, "cm")
print('周长为', cv2.arcLength(longestContour, True) * kc, "cm")
print('面积为', cv2.contourArea(longestContour) * kc * kc, "square cm")


cv2.waitKey(0)
