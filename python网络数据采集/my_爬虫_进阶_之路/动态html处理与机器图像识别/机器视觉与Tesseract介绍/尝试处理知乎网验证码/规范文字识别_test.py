# coding = utf-8

'''
@author = super_fazai
@File    : 规范文字识别_test.py
@Time    : 2017/8/31 13:31
@connect : superonesfazai@gmail.com
'''

import pytesseract
from PIL import Image

# image = Image.open('very_code_image.png')
image = Image.open('11.png')
text = pytesseract.image_to_string(image)

print(text)

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