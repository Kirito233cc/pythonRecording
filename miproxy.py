import mitmproxy.http
from mitmproxy import ctx
from urllib import parse
import json
from pynput.keyboard import Key, Controller
from time import sleep

f1 = open('/Users/xushengchao/Desktop/origin.txt', 'r')
t1 = f1.read()
f1.close()
f2 = open('/Users/xushengchao/Desktop/change.txt', 'r')
t2 = f2.read()
f2.close()


# 当收到请求时触发
def request(flow: mitmproxy.http.HTTPFlow):
    pass


# 当收到响应时触发
def response(flow: mitmproxy.http.HTTPFlow):
    url = flow.request.url
    # 仅对请求url中包含'zhiyitech'的响应做处理
    if 'zhiyitech' in url:
        # 替换response中的内容
        # f = open('/Users/xushengchao/Desktop/response.txt', 'w+')
        # f.write(text)
        # f.close()
        # text = text.replace(t1, t2)

        # 获取响应头中的content-type
        content_type = flow.response.headers.get('content-type')
        # 仅对返回格式为json的响应进行处理
        if content_type == 'application/json;charset=UTF-8':
            # 获取response的内容
            text = flow.response.text
            # 将response内容转成字典格式
            text = json.loads(text)
            success = text.get('success')
            # 判断response的success状态
            if str(success) == 'True':
                print(success)
            else:
                # 触发并释放Esc按键
                keyboard = Controller()
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                # 获取错误信息并输出
                errorDesc = text.get('errorDesc')
                print('请求报错，url为：%s' % url + '\n' + '错误信息为:%s' % errorDesc)
        else:
            pass
    else:
        pass


# 当请求报错，无法返回响应时触发
def error(flow: mitmproxy.http.HTTPFlow):
    url = flow.request.url
    if 'zhiyitech' in url:
        f = open('/Users/xushengchao/Downloads/mitmproxy自动化截取url文档/mitmproxyError.txt', 'a')
        f.write(url)
        f.write('\n')
        f.close()
    else:
        pass
