import cv2
import numpy as np
from typing import List

VIDEO_RESOLUTION = (1920, 1080, 3)


def plygon_ticks(file):
    ticks = []
    # read file txt and extract value
    with open(file, 'r') as file:
        a = file.readline()
        a = a.split('(')[1]
        a = a.split(')')[0]
        a = a.split(',')

        x, y = [], []
        final = []
        for i, ele in enumerate(a):
            if i % 2 == 0:
                x.append(int(ele))
            else:
                y.append(int(ele))

        for ele in range(len(x)):
            final.append((x[ele], y[ele]))
        ticks.append(final)

    # return [[(x1,y1),(x2,y2),(x3,y3),...]]
    return ticks


def calculate_IOU_btw_frames(ply1, ply2):
    # create a black image
    img1 = np.zeros(VIDEO_RESOLUTION, np.uint8)
    points = ply1
    # draw the lines on the image
    for i in range(len(points) - 1):
        cv2.line(img1, points[i], points[i + 1], (0, 255, 0), 3)

    # fill the polygon formed by the endpoints of the lines with black color
    pts = np.array(points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img1, [pts], (0, 0, 0))

    img2 = np.zeros(VIDEO_RESOLUTION, np.uint8)
    points = ply2
    # draw the lines on the image
    for i in range(len(points) - 1):
        cv2.line(img2, points[i], points[i + 1], (0, 255, 0), 3)

    # fill the polygon formed by the endpoints of the lines with black color
    pts = np.array(points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img2, [pts], (0, 0, 0))

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # threshold the images to obtain binary masks
    _, mask1 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY)
    _, mask2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY)

    # calculate the intersection and union of the masks
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)

    # calculate the IoU
    iou = np.sum(intersection) / np.sum(union)

    return iou


def calculate_IOU_btw_frame_lists(ply1s: List, ply2s: List):
    if len(ply1s) != len(ply2s):
        return 0
    IOUs = [calculate_IOU_btw_frames(ply1s[ply_idx], ply2s[ply_idx]) for ply_idx in range(len(ply1s))]
    return np.mean(IOUs)

def calculate_IOU_btw_files(file1: str, file2: str):
    ply1s = plygon_ticks(file1)
    ply2s = plygon_ticks(file2)
    return calculate_IOU_btw_frame_lists(ply1s, ply2s)
