
import cv2
import os
import os.path
import numpy as np




try:
    from PIL import Image, ImageEnhance, ImageFilter
except:
    print("please install PIL")

import sys

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

scriptpath = os.path.dirname(__file__)
filename1 = os.path.join(scriptpath, 'comp.jpg')
filename2 = os.path.join(scriptpath, 'goi.jpg')

img_rgb = cv2.imread(filename1)
#im=img_rgb.copy()
#print(img_rgb)
template = cv2.imread(filename2)
#cv2.imwrite('result.png', img_rgb)
h,w = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
#print(res)
threshold = .8
loc = np.where(res >= threshold)
print(loc is None)
# for pt in zip(*loc[::-1]):  # Switch collumns and rows
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#
# cv2.imwrite('result1.jpg', img_rgb)
#print(im==img_rgb)



