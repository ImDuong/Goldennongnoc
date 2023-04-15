import os
import re
import time

import cv2
from typing import List
import math

import matplotlib.pyplot as plt
import numpy as np

from models.media import CamData

WINDOW_NAME = 'Golden Overlapper'
OVERLAPPING_AREA_COLOR = [255, 223, 0]
SAMPLE_ROOT_PATH = "./assets/Public_Test/videos/"
CAMERA_FPS = 5
CAMERA_DELAY = int(1000 / CAMERA_FPS)
NB_COLS = 2
prefix = "scene4cam_10"
CAM_SRCS = [

    {
        "src": prefix + "/CAM_1.mp4",
        "name": "CAM_1"
    },
    {
        "src": prefix + "/CAM_2.mp4",
        "name": "CAM_2"
    },
    {
        "src": prefix + "/CAM_3.mp4",
        "name": "CAM_3"
    },
    {
        "src": prefix + "/CAM_4.mp4",
        "name": "CAM_4"
    },
]

if __name__ == '__main__':
    cameras_data: List[CamData] = []
    for cam_src in CAM_SRCS:
        cv_cap = cv2.VideoCapture(os.path.join(SAMPLE_ROOT_PATH, cam_src["src"]))
        if not cv_cap.isOpened():
            print(f'Error opening video file: {cam_src["name"]} - {cam_src["src"]}')
            exit()
        cameras_data.append(CamData(
            cam_name=cam_src["name"],
            cam_src=cam_src["src"],
            cam_cap=cv_cap,
        ))

    NB_ROWS = math.ceil(len(cameras_data) / NB_COLS)
    width = int(cameras_data[0].cam_cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * NB_COLS
    height = int(cameras_data[0].cam_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) * NB_ROWS

    # Create output window
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, width, height)

    global_frame_idx = 0
    while True:
        frame_np = [[] for _ in range(NB_ROWS)]
        frame_np_idx = 0
        for cam_idx, cam in enumerate(cameras_data):
            ret, frame_img = cam.cam_cap.read()
            if not ret:
                break
            frame_img = cv2.resize(frame_img, (int(width / NB_COLS), int(height / NB_ROWS)))

            # read overlapping region via multiple frames
            with open(os.path.join("./assets/Public_Test/groundtruth/" + prefix, cam.cam_name + ".txt"), 'r') as file:
                lineIdx = 0
                for line in file:
                    if lineIdx == global_frame_idx:
                        line = line.strip()
                        pattern = r'\((.*?)\)'
                        match = re.search(pattern, line)
                        if match:
                            coords_str = match.group(1)
                            coords = [int(x) for x in coords_str.split(',')]
                            coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
                            print(coords)
                            for i in range(len(coords) - 1):
                                cv2.line(frame_img, coords[i], coords[i + 1], (0, 0, 255), thickness=2)
                        break
                    lineIdx += 1

            frame_np[frame_np_idx].append(frame_img)

            if len(frame_np[frame_np_idx]) >= NB_COLS:
                frame_np_idx += 1

            if cam_idx == len(cameras_data) - 1 and frame_np_idx == len(frame_np) - 1 and len(frame_np[frame_np_idx]) < NB_COLS:
                for addedIdx in range(NB_COLS - len(frame_np[frame_np_idx])):
                    frame_np[frame_np_idx].append(frame_img)

        frame_np_concat: List[np.ndarray] = []
        for frame_np_ele in frame_np:
            frame_np_concat.append(np.concatenate(tuple(frame_np_ele), axis=1))

        merged_frame = np.concatenate(tuple(frame_np_concat), axis=0)

        # draw overlapping region to each frame in each camera window

        # Display merged frame in output window
        cv2.imshow(WINDOW_NAME, merged_frame)

        global_frame_idx += 1
        time.sleep(5)
        # Exit if the user presses the 'q' key
        if cv2.waitKey(CAMERA_DELAY) & 0xFF == ord('q'):
            break

    for cam in cameras_data:
        cam.cam_cap.release()

    cv2.destroyAllWindows()
