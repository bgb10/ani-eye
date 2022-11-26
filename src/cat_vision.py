# imports
import numpy as np
import cv2
import src.filters as f

def rgb_to_lms(img):
    lms_matrix = np.array(
        [[0.3904725 , 0.54990437, 0.00890159],
        [0.07092586, 0.96310739, 0.00135809],
        [0.02314268, 0.12801221, 0.93605194]]
        )
    return np.tensordot(img, lms_matrix, axes=([2], [1]))


def lms_to_rgb(img):
    rgb_matrix = np.array(
        [[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
        [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
        [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]]
        )
    return np.tensordot(img, rgb_matrix, axes=([2], [1]))

def see(src: cv2.Mat):
    res = src.copy()

    if f.calcBrightness(res) < 50:
        res = f.addBrightness(res, 100)

    lms = rgb_to_lms(res)
    red_green_filter = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
    red_green_blinded = np.tensordot(lms, red_green_filter, axes=([2], [1]))
    rgb_img = lms_to_rgb(red_green_blinded)
    res = rgb_img.astype(np.uint8)

    res = f.imitateFOV(res, 30, 100, (3,3))

    return res