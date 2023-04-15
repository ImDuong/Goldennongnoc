import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def vertices_detector(mask, show_vertices=False, show_all=False):
    # For visualize vertices
    white = np.zeros((mask.shape))
    white.fill(255)

    # Set a threshold value
    threshold = 0.5
    font = cv2.FONT_HERSHEY_COMPLEX

    # Apply the threshold and convert to gray
    gray = np.where(mask > threshold, 255, 0).astype(np.uint8)

    contours, _ = cv2.findContours(gray, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Going through every contours found in the image.
    vertices = cv2.approxPolyDP(contours[1], 0.009 * cv2.arcLength(contours[1], True), True)

    # draws boundary of contours.
    cv2.drawContours(gray, [vertices], 0, (255, 0, 255), 5)

    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = vertices.ravel()
    i = 0
    res = []

    for j in n:
        if (i % 2 == 0):
            x = n[i]
            y = n[i + 1]
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
            cv2.circle(white, (x, y), 3, (0, 0, 255), 10)
            cv2.imshow("Check Points", white)
            cv2.waitKey(0)
            cv2.destroyWindow("Check Points")
    return res


# for testing
if __name__ == '__main__':
    img = plt.imread('./assets/sample_greyscale_overlapping_area/area1.png')[:, :, 0]

    vertices = vertices_detector(img)
    print(vertices)
    print(len(vertices))

    img = plt.imread('./assets/sample_greyscale_overlapping_area/area2.png')[:, :, 0]

    vertices = vertices_detector(img)
    print(vertices)
    print(len(vertices))
