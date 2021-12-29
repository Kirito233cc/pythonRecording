from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard
import threading
from mss import mss
from PIL import Image

image = cv2.imread("C:/Users/Kirito233cn/Desktop/DSCF3159.jpg")
print('Original Dimensions : ', image.shape)
scale_percent = 10  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
res = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
print(type(image))
print(type(res))
cv2.imshow("Resized image", res)
cv2.waitKey(0)
cv2.destroyAllWindows()