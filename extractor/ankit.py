import cv2
import numpy as np
import os
scriptpath = os.path.dirname(__file__)
filename1 = os.path.join(scriptpath, 'images.jpg')
filename2 = os.path.join(scriptpath, 'goi.jpg')
image = cv2.imread(filename1)
template = cv2.imread(filename2)
result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
print (np.unravel_index(result.argmax(),result.shape))