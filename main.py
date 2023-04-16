import os
import cv2
from typing import List
import math
import time

import matplotlib.pyplot as plt
import numpy as np

from models.detector import Predict
from models.media import CamData
from lib.utils import load_cameras, vertices_detector

WINDOW_NAME = 'Golden Overlapped'
OVERLAPPING_AREA_COLOR = (0, 0, 255)
SAMPLE_ROOT_PATH = "./assets/sample"
CAMERA_FPS = 5
CAMERA_DELAY = int(1000 / CAMERA_FPS)
NB_COLS = 2

CAM_SRCS = [
    {
        "src": "192_168_5_101.mp4",
        "name": "CAM_1"
    },
    {
        "src": "192_168_5_102.mp4",
        "name": "CAM_2"
    },
    {
        "src": "192_168_5_103.mp4",
        "name": "CAM_3"
    },
    {
        "src": "192_168_5_104.mp4",
        "name": "CAM_4"
    }
]


def get_rendered_frames():
    frame_imgs = []
    for cam in cameras_data:
        ret, frame_img = cam.cam_cap.read()
        if not ret:
            break
        frame_img = cv2.resize(frame_img, (int(width / NB_COLS), int(height / NB_ROWS)))
        frame_imgs.append(frame_img)

    return frame_imgs


def get_merged_window(frame_imgs: List, nb_columns: int, nb_rows: int):
    frame_np = [[] for _ in range(nb_rows)]
    frame_np_idx = 0
    for frame_idx, frame_img in enumerate(frame_imgs):
        frame_img = cv2.resize(frame_img, (int(width / nb_columns), int(height / nb_rows)))

        frame_np[frame_np_idx].append(frame_img)

        if len(frame_np[frame_np_idx]) >= nb_columns:
            frame_np_idx += 1

        if frame_idx == len(frame_imgs) - 1 and frame_np_idx == len(frame_np) - 1 and len(
                frame_np[frame_np_idx]) < nb_columns:
            for addedIdx in range(nb_columns - len(frame_np[frame_np_idx])):
                frame_np[frame_np_idx].append(frame_img)

    frame_np_concat: List[np.ndarray] = []
    for frame_np_ele in frame_np:
        frame_np_concat.append(np.concatenate(tuple(frame_np_ele), axis=1))

    merged_window = np.concatenate(tuple(frame_np_concat), axis=0)
    return merged_window


if __name__ == '__main__':
    cameras_data = load_cameras(cam_srcs=CAM_SRCS, base_path=SAMPLE_ROOT_PATH)

    # init window settings
    NB_ROWS = math.ceil(len(cameras_data) / NB_COLS)
    width = int(cameras_data[0].cam_cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * NB_COLS
    height = int(cameras_data[0].cam_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) * NB_ROWS
    for i in range(10):
        frames = get_rendered_frames()
    list_of_frame, list_of_vertices = Predict(frames)
    # list_of_vertices = [[(1366, 120), (1919, 346), (1456, 1079), (1116, 533), (1652, 369), (1248, 190), (898, 163), (836, 61)], [(201, 127), (599, 158), (402, 336), (1918, 757), (0, 212), (745, 329), (764, 330), (788, 345), (799, 358), (796, 375), (787, 382), (773, 384), (739, 364), (735, 358), (735, 350), (740, 333)], [(1914, 53), (393, 231), (560, 143), (1316, 0)], [(653, 0), (869, 83), (1037, 260), (0, 96), (1919, 237), (1577, 149), (1478, 0), (509, 316), (533, 315), (572, 324), (577, 329), (577, 346), (547, 356), (500, 356), (482, 352), (469, 343), (468, 331), (0, 805), (1285, 529), (1823, 1078)]]
    # print(list_of_vertices)
    # Create output window
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, width, height)
    i = 0
    while True:
        i += 1
        # read frames
        frames = get_rendered_frames()
        # predict overlapping region via multiple frames (1 frame for each camera)
        #list_of_frame, list_of_vertices = Predict(frames)
        #print(list_of_vertices)
        # draw overlapping region to each frame in each camera window
        for frame_idx in range(len(frames)):
            # for i in range(len(list_of_vertices[frame_idx]) - 1):
            #     cv2.fillPoly(frames[frame_idx], list_of_vertices[frame_idx][i], list_of_vertices[frame_idx][i + 1], (0, 0, 255), thickness=2)
            cv2.fillPoly(frames[frame_idx], pts=[np.array(list_of_vertices[frame_idx],np.int32)], color=(255, 0, 0))

        # get merged window
        final_window = get_merged_window(frames, NB_COLS, NB_ROWS)

        # Display merged frame in output window
        cv2.imshow(WINDOW_NAME, final_window)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(CAMERA_DELAY) & 0xFF == ord('q'):
            break

    for cam in cameras_data:
        cam.cam_cap.release()

    cv2.destroyAllWindows()
