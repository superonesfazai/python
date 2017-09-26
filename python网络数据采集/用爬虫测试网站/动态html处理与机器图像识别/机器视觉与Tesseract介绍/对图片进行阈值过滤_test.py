# coding = utf-8

'''
@author = super_fazai
@File    : 对图片进行阈值过滤_test.py
@Time    : 2017/8/31 14:18
@connect : superonesfazai@gmail.com
'''

"""
随着背景色从左到右不断加深,文字变得越来越难以识别,Tesseract 识别出的 每一行的最后几个字符都是错的。

遇到这类问题,可以先用 Python 脚本对图片进行清理。
利用 Pillow 库,我们可以创建一个 阈值过滤器来去掉渐变的背景色,
只把文字留下来,从而让图片更加清晰,便于 Tesseract 读取:
"""

from PIL import Image
import subprocess

def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)

    # 对图片进行阈值过滤,然后保存
    image = image.point(lambda x: 0 if x<143 else 255)
    image.save(newFilePath)

    # 调用系统的tesseract命令对图片进行OCR识别
    subprocess.call(["tesseract", newFilePath, "output"])

    # 打开文件读取结果
    file = open("output.txt", 'r', encoding='utf-8')
    print(file.read())
    file.close()

# cleanFile("./images/tess2.png", "./images/tess2clean.png")
cleanFile('./images/seccode.jpeg', './images/seccode.jpeg')
'''
测试结果:
Thus IS some text. written In Arial. that will be ,
Tesseract Here are some symbols: IW“ ’
'''