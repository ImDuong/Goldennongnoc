import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

from lib.utils import vertices_detector

img = 0
src_pts = []
i = 0
point_list = []

def click_event(event, x, y, flags, param):
    global src_pts, i, img, point_list
    if event == cv2.EVENT_LBUTTONDOWN and i < 4:
        # print(img)
        # Display the selected points
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('image', img)
        # Add the selected point to the list of source points
        src_pts.append([x, y])
        i += 1
    elif event == cv2.EVENT_LBUTTONDOWN and i == 4:
        # When all points are selected, calculate the transform matrix and apply the transform
        # tgt_pts = np.float32([[0, 0], [400, 0], [400, 600], [0, 600]])
        point_list.append(src_pts)
        # print('point list appended')
        src_pts = []
        i = 0


def Predict(list_of_image=[]):
    global img
    img_1 = list_of_image[0]
    height, width, channels = img_1.shape
    border_size_width = int(1 * width)
    border_size_height = int(1 * height)
    border_color = (255, 255, 255)
    for image in list_of_image:
        img = image
        # Display the image and set the callback function
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    point_list.append(src_pts)
    out_list = []
    inv_M_list = []
    image_list_w_border = []
    border_image_width = 0
    border_image_height = 0
    for i in range(len(list_of_image)):
        image_w_border = cv2.copyMakeBorder(list_of_image[i], border_size_height, border_size_height, border_size_width,
                                            border_size_width,
                                            cv2.BORDER_CONSTANT, value=border_color)
        image_width, image_height, image_channels = image_w_border.shape
        image_list_w_border.append(image_w_border)
        # print(image_width, image_height)
        border_image_width = image_width
        border_image_height = image_height
        center_point_x = image_width / 2
        center_point_y = image_height / 2
        top_left_x = center_point_x - image_width / 10
        top_left_y = center_point_y - image_height / 10
        bottom_right_x = center_point_x + image_width / 10
        bottom_right_y = center_point_y + image_height / 10
        for point in point_list[i]:
            point[0] += border_size_width
            point[1] += border_size_height
        input_pts = np.array(point_list[i]).reshape((4, 2)).astype('float32')
        output_pts = np.array([[top_left_x, top_left_y], [bottom_right_x, top_left_y], [bottom_right_x, bottom_right_y],
                               [top_left_x, bottom_right_y]]).astype('float32')
        M = cv2.getPerspectiveTransform(input_pts, output_pts)
        inv_M = cv2.getPerspectiveTransform(output_pts, input_pts)
        inv_M_list.append(inv_M)
        out = cv2.warpPerspective(image_w_border, M, (image_height, image_width), flags=cv2.INTER_LINEAR)

        out_list.append(out)
    mask_list = []
    for out_image in out_list:
        out_image = np.array(out_image)
        gray = cv2.cvtColor(out_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        delete_white = cv2.bitwise_and(out_image, out_image, mask=mask)
        img_gray = cv2.cvtColor(delete_white, cv2.COLOR_BGR2GRAY)
        # Apply binary thresholding with a threshold value of 0
        _, thresh = cv2.threshold(img_gray, 0, 1, cv2.THRESH_BINARY)
        median = cv2.medianBlur(thresh, 7)

        # Apply max pooling to fill in gaps
        kernel = np.ones((5, 5), np.uint8)
        max_pool = cv2.dilate(median, kernel, iterations=1)
        mask_list.append(max_pool)
    # for i,mask_image in enumerate(mask_list):
    #     plt.subplot(1,4,i+1)
    #     plt.imshow(mask_image)
    result_all_overlap = np.add(np.add(np.add(mask_list[0], mask_list[1]), mask_list[2]), mask_list[3])
    result = result_all_overlap.copy()
    result[result < 4] = 255
    # plt.subplot(1,2,1)
    # plt.imshow(result)
    # plt.subplot(1,2,2)
    # plt.imshow(result_all_overlap)
    result[result == 4] = 0
    # img = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    # img = cv2.medianBlur(img, 27)
    result_3D = np.stack((result, result, result), axis=-1)
    filtered_image = cv2.medianBlur(result_3D, ksize=61)
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.imwrite('final.png', img)
    # cv2.destroyAllWindows()
    back_list = []
    cropped_back_list = []
    vertices_list = []
    for i in range(len(out_list)):
        image_width, image_height, image_channels = out_list[i].shape
        back = cv2.warpPerspective(filtered_image, inv_M_list[i], (border_image_height, border_image_width),
                                   flags=cv2.INTER_LINEAR)
        back_list.append(back)
        cropped_img = back[border_size_height:-border_size_height, border_size_width:-border_size_width]
        # print(cropped_img.shape)
        cropped_back_list.append(cropped_img)
        vertices = vertices_detector(cropped_img)
        vertices_list.append(vertices)
    final_frame_list = []
    for i in range(len(list_of_image)):
        final_frame = cv2.addWeighted(list_of_image[i], 1 - 0.5, cropped_back_list[i], 0.5, 0)
        final_frame_list.append(final_frame)
    return final_frame_list, vertices_list