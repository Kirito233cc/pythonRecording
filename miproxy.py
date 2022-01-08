import mitmproxy.http
from mitmproxy import ctx
from urllib import parse
import json

f1 = open('/Users/xushengchao/Desktop/origin.txt', 'r')
t1 = f1.read()
f1.close()
# ctx.log.info(t1)
f2 = open('/Users/xushengchao/Desktop/change.txt', 'r')
t2 = f2.read()
f2.close()
# ctx.log.info(t2)


# 当收到请求时触发
def request(flow: mitmproxy.http.HTTPFlow):
    pass


# 当收到响应时触发
def response(flow: mitmproxy.http.HTTPFlow):
    url = flow.request.url
    if 'zhiyitech' in url:
        # 替换response中的内容
        # f = open('/Users/xushengchao/Desktop/response.txt', 'w+')
        # f.write(text)
        # f.close()
        # text = text.replace(t1, t2)

        # 获取响应头中的content-type
        content_type = flow.response.headers.get('content-type')
        # 仅对返回格式为json的响应进行处理
        if(content_type == 'application/json;charset=UTF-8'):
            # 获取response的内容
            text = flow.response.text
            # 将response内容转成字典格式
            text = json.loads(text)
            success = text.get('success')
            print(success)
            # print(content_type)
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
