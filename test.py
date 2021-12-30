from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard
import threading
from mss import mss
from PIL import Image


# image = cv2.imread("C:/Users/Kirito233cn/Desktop/DSCF3159.jpg")
# print('Original Dimensions : ', image.shape)
# scale_percent = 10  # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# res = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
# print(type(image))
# print(type(res))
# cv2.imshow("Resized image", res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        # monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        # return sct_img


def adj_size(self, size):
    scale_percent = size  # 按照比例缩小尺寸
    width = int(self.shape[1] * scale_percent / 100)
    height = int(self.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(self, dim, interpolation=cv2.INTER_AREA)


if __name__ == '__main__':
    a = capture_screenshot()
    res = adj_size(np.array(a), 50)
    cv2.imshow("Resized image", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
