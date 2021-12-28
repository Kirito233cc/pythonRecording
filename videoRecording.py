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
    video = cv2.VideoWriter('%s.avi' % name, fourcc, 20.0, (a, b), True)  # 输出文件命名为test.mp4,帧率为20，可以自己设置
    ims = []
    while True:
        im = ImageGrab.grab()
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        ims.append(imm)
        print(len(ims))
        if len(ims) > 160:
            ims.pop(0)
            if flag:
                for i in ims:
                    video.write(i)
                print("录制结束！")
                break
        else:
            if flag:
                for i in ims:
                    video.write(i)
                print("录制结束！")
                break
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