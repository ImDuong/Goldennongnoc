import os

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from typing import List
from models.media import CamData


def vertices_detector(image, show_vertices=False, show_all=False):
    filtered_image = cv2.medianBlur(image, ksize=51)
    mask = filtered_image[:, :, 0]
    # For visualize vertices
    white = np.zeros((mask.shape))
    white.fill(255)
    remove_points = [(0, 0), (0, mask.shape[0] - 1), (mask.shape[1] - 1, 0), (mask.shape[1] - 1, mask.shape[0] - 1)]
    # Set a threshold value
    threshold = 0.5
    font = cv2.FONT_HERSHEY_COMPLEX

    # Apply the threshold and convert to gray
    gray = np.where(mask > threshold, 255, 0).astype(np.uint8)

    contours, _ = cv2.findContours(gray, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    res = []
    for cnt in contours:
        # Going through every contours found in the image.
        vertices = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        # draws boundary of contours.
        cv2.drawContours(gray, [vertices], 0, (255, 0, 255), 5)

        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = vertices.ravel()
        i = 0
        for j in n:
            if (i % 2 == 0):
                x = n[i]
                y = n[i + 1]
                if (x, y) not in remove_points:
                    res.append((x, y))
                    string = str(x) + " " + str(y)

                    if (i == 0):
                        # text on topmost co-ordinate.
                        cv2.putText(gray, "Arrow tip", (x, y),
                                    font, 0.5, (255, 0, 0))
                    else:
                        # text on remaining co-ordinates.
                        cv2.putText(gray, string, (x, y),
                                    font, 0.5, (0, 255, 0))
            i = i + 1
    res = res[::-1]
    if show_all:
        plt.imshow(gray, cmap='gray')
    if show_vertices:
        for (x, y) in res:
            cv2.namedWindow("Check Points", cv2.WINDOW_NORMAL)
            cv2.circle(white, (x, y), 10, (0, 0, 255), 10)
            # cv2.imshow("Check Points", white)
            # cv2.waitKey(0)
            cv2.destroyWindow("Check Points")
    return res


def load_cameras(cam_srcs: List, base_path: str) -> List[CamData]:
    cameras_data: List[CamData] = []
    for cam_src in cam_srcs:
        cv_cap = cv2.VideoCapture(os.path.join(base_path, cam_src["src"]))
        if not cv_cap.isOpened():
            print(f'Error opening video file: {cam_src["name"]} - {cam_src["src"]}')
            exit()
        cameras_data.append(CamData(
            cam_name=cam_src["name"],
            cam_src=cam_src["src"],
            cam_cap=cv_cap,
        ))
    return cameras_data


# # for testing
# if __name__ == '__main__':
#     img = cv2.imread('../assets/sample_greyscale_overlapping_area/area1.png')

#     vertices = vertices_detector(img)
#     print(vertices)
#     print(len(vertices))

#     img = cv2.imread('./assets/sample_greyscale_overlapping_area/area2.png')

#     vertices = vertices_detector(img)
#     print(vertices)
#     print(len(vertices))
