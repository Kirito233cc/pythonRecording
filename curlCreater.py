from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def curlMaker():
    # 获取mitmproxy端发送的信息
    content = request.data
    jContent = json.loads(content)
    # 获取url并转成curl格式
    output = 'curl \'%s\' \\\n' % jContent.get('url')
    # 获取headers信息并转成curl格式
    jHeaders = jContent.get('headers')
    for k, v in jHeaders.items():
        output += '-H \'%s: %s\' \\\n' % (k, v)
    # 判断请求方法
    if jContent.get('method') == 'GET':
        output += '-X \'%s\' \\\n' % jContent.get('method')
    if jContent.get('method') == 'POST':
        output += '-X \'%s\' \\\n' % jContent.get('method')
        # 若为post带上body，并转为curl格式
        output += '--data-binary \'%s\' \\\n' % jContent.get('content')
    # curl压缩
    output += '--compressed'
    print(output + '\n')
    # 获取生成的curl并输出到以错误信息命名的txt文件中
    with open('/Users/xushengchao/Desktop/%s.txt' % jContent.get('errorDesc'), 'w+') as f:
        f.write(output)
    return content


if __name__ == '__main__':
    app.run()