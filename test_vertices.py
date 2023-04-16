import os

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from typing import List
from models.media import CamData
from lib.utils import vertices_detector

if __name__ == '__main__':
    img = cv2.imread('assets\sample_greyscale_overlapping_area\\area1.png')

    vertices = vertices_detector(img)
    print(vertices)
    print(len(vertices))

    img = cv2.imread('assets\sample_greyscale_overlapping_area\\area2.png')

    vertices = vertices_detector(img)
    print(vertices)
    print(len(vertices))