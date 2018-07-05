# coding = utf-8

'''
@author = super_fazai
@File    : 规范文字识别_test.py
@Time    : 2017/8/31 13:31
@connect : superonesfazai@gmail.com
'''

import pytesseract
from PIL import Image
import requests
from io import BytesIO
import json, re, base64

'''
1. 从网络获取验证码(识别中文)
'''
### test_1
# response = requests.get('http://www.wisedream.net/res/img/ocr-test.png')
# img = Image.open(BytesIO(response.content))
# print(pytesseract.image_to_string(img, lang='chi_sim'))

### test_2，测试折800的验证码
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'diablo.alibaba.com',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
}

query_string = {
    'sessionid': '01-m_ZiEy0_67YhTwhCfGlCh2gNq93HaGS_yk3hfYmY9iIVT6la1TM1rtkaLSZe5mwV2Wi9kDZBAK50WYxZOwAY5KYPpBGAyJKsEnvG1VEUXb5hpFCQEDaCU2YrqTfjlRPsin7-1iLEyzNzKzaPUVJKA',
    'identity': 'WKBT',
    'style': 'default_science',
    'callback': 'jsonp_08668900079497168',
}
url = 'http://diablo.alibaba.com/captcha/image/get.jsonp'
response = requests.get(url, headers=headers, params=query_string)
body = response.content.decode('utf-8')

try:
    body = re.compile('jsonp_08668900079497168\((.*)\);').findall(body)[0]
    img_data = json.loads(body)
    base64_img_str = img_data.get('result', {}).get('data', [])[0]
except Exception as e:
    print('遇到错误: ', e)
    base64_img_str = ''

## 将base64转换位图片存储
print(base64_img_str)
base64_img_str = base64_img_str[base64_img_str.find(",") + 1:]  # 得到data:image/jpg;base64,后面的图片的base64格式的字符串
# print(base64_img_str)
with open('./images/some_img.jpg', 'wb') as f:
    base64_img_str = base64.b64decode(base64_img_str)
    f.write(base64_img_str)

'''
1) 将图片进行降噪处理, 通过二值化去掉后面的背景色并加深文字对比度
'''
def convert_Image(img, standard=127.5):
    '''
    【灰度转换】
    '''
    image = img.convert('L')

    #【二值化】根据阈值 standard , 将所有像素都置为 0(黑色) 或 255(白色), 便于接下来的分割
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image

img = Image.open('./images/some_img.jpg')
img.show()
# convert_Image(img=img)
print(pytesseract.image_to_string(img))

'''
2.本地验证码识别
'''
# image = Image.open('./images/tesseract_test.jpg')
# image = Image.open('./images/seccode.jpeg')
# image = Image.open('./images/zhe_800.jpg')
# image = Image.open('./images/get_img.jpeg')
# text = pytesseract.image_to_string(image)

# print(text)

'''
测试结果:
- Power—Thanks forflying Vim —-bash—80x24

[Power@PowerMac ~$ tesseract test.jpg text

Tesseract Open Source OCR Engine v3.04.01 with Leptonica
Warning in pixReadMemPng: work—around: writing to a temp file
[Power@PowerMac ~$

[Power@PowerMac ~$ cat text.txt

This is some text, written in Arial, that will be read by
Tesseract. Here are some symbols: !@#$%"&*()

Power@PowerMac ~$
'''