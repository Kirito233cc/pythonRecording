"""
python 屏幕录制改进版，无opencv黑框显示！
@zhou 2020/1/29_
"""
import time

from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard
import threading
from mss import mss
from PIL import Image


def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        # monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        # return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        return sct_img


flag = False  # 停止标志位


def video_record():
    """
    屏幕录制！
    :return:
    """
    name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 当前的时间
    p = ImageGrab.grab()  # 获得当前屏幕
    a, b = p.size  # 获得当前屏幕的大小
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
    video = cv2.VideoWriter('%s.avi' % name, fourcc, 30.0, (a, b), True)  # 输出文件命名为‘time.avi’,帧率为30，可以自己设置
    ims = []
    while True:
        # im = ImageGrab.grab()
        im = capture_screenshot()
        ims.append(im)
        print(len(ims))
        if len(ims) > 300:  # 限制录制时长10s
            ims.pop(0)
            if flag:
                break
        else:
            if flag:
                break

    print("正在生成录像")
    for i in ims:
        raw_pic = Image.frombytes('RGB', i.size, i.bgra, 'raw', 'BGRX')  # 对截图进行编码
        image = np.array(raw_pic)
        scale_percent = 10  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        new_pic = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        # new_pic = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
        imm = cv2.cvtColor(np.array(new_pic), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        video.write(imm)
    print("录制结束！")
    video.release()


def on_press(key):
    """
    键盘监听事件！！！
    :param key:
    :return:
    """
    # print(key)
    global flag
    if key == keyboard.Key.esc:
        flag = True
        print("stop monitor！")
        return False  # 返回False，键盘监听结束！


if __name__ == '__main__':
    th = threading.Thread(target=video_record)
    th.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
