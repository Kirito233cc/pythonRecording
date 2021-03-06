from time import sleep
from PIL import ImageGrab
import numpy as np
import cv2
import datetime
# from pynput import keyboard
import keyboard
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
sFlag = False  # 终结标志位


def adj_size(self, size):  # 将图像按照比例缩放
    scale_percent = size  # 按照比例缩小尺寸
    width = int(self.shape[1] * scale_percent / 100)
    height = int(self.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(self, dim, interpolation=cv2.INTER_AREA)


def video_record():
    """
    屏幕录制！
    :return:
    """
    global flag, sFlag
    if not sFlag:
        name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 当前的时间
        p = ImageGrab.grab()  # 获得当前屏幕
        new_p = Image.fromarray(adj_size(np.array(p), 50))  # 调用adj_size方法按比例调整大小
        a, b = new_p.size  # 获得当前屏幕的大小
        print(p.size)
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
                if flag or sFlag:
                    break
            else:
                if flag or sFlag:
                    break

        print("正在生成录像")
        for i in ims:
            raw_pic = Image.frombytes('RGB', i.size, i.bgra, 'raw', 'BGRX')  # 对截图进行编码
            image = np.array(raw_pic)
            new_pic = adj_size(image, 50)  # 缩放截图比例50%
            imm = cv2.cvtColor(new_pic, cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            video.write(imm)
        print("录制结束！")
        video.release()
        flag = False
        video_record()
    else:
        print("程序关闭！")


# def on_press(key):
#     # print(key)
#     global flag
#     if key == keyboard.Key.esc:
#         # 让前端接收到response后再结束录制
#         sleep(3)
#         flag = True
#         print("stop monitor！")
#         return False  # 返回False，键盘监听结束！

def on_press():
    # print(key)
    global flag
    # 让前端接收到response后再结束录制
    sleep(3)
    flag = True
    print("stop monitor！")


def shut_down():
    global sFlag
    sFlag = True
    keyboard.wait()


if __name__ == '__main__':
    th = threading.Thread(target=video_record)
    th.start()
    keyboard.add_hotkey('esc', on_press)
    keyboard.add_hotkey('q', shut_down)
    # print(threading.current_thread().name)
    # with keyboard.Listener(on_press=on_press) as listener:
    #     listener.join()
    # print(threading.current_thread().name)
    # listener = threading.
    # listener.start()
