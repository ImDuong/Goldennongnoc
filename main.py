import os
import cv2
from typing import List
import math
import numpy as np

from models.media import CamData


WINDOW_NAME = 'Golden Overlapper'
SAMPLE_ROOT_PATH = "./assets/sample"
CAMERA_FPS = 5
CAMERA_DELAY = int(1000/CAMERA_FPS)
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

    while True:
        frame_np = [[] for _ in range(NB_ROWS)]
        frame_np_idx = 0
        for cam in cameras_data:
            ret, frame_img = cam.cam_cap.read()
            if not ret:
                break
            frame_img = cv2.resize(frame_img, (int(width / NB_COLS), int(height / NB_ROWS)))

            frame_np[frame_np_idx].append(frame_img)

            if len(frame_np[frame_np_idx]) >= NB_COLS:
                frame_np_idx += 1

        frame_np_concat: List[np.ndarray] = []
        for frame_np_ele in frame_np:
            frame_np_concat.append(np.concatenate(tuple(frame_np_ele), axis=1))

        merged_frame = np.concatenate(tuple(frame_np_concat), axis=0)

        # Display merged frame in output window
        cv2.imshow(WINDOW_NAME, merged_frame)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(CAMERA_DELAY) & 0xFF == ord('q'):
            break

    for cam in cameras_data:
        cam.cam_cap.release()

    cv2.destroyAllWindows()
