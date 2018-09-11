# coding:utf-8

'''
@author = super_fazai
@File    : 测试批量验证码生成训练集.py
@Time    : 2018/4/8 10:01
@connect : superonesfazai@gmail.com
'''

from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random, time, os

# 验证码中的字符, 就不用汉字了
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):
    '''
    随机生成验证码文本(验证码一般都无视大小写；验证码长度4个字符)
    :param char_set:
    :param captcha_size:
    :return: a list eg: ['a', 'v', 'A', '1', ...]
    '''
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)

    return captcha_text

def gen_captcha_text_and_image():
    '''
    生成字符对应的验证码
    :return:
        eg: captcha_image : type np array 数组
            [[[239 244 244]
              [239 244 244]
              [239 244 244]
              ...,
              ...,
              [239 244 244]
              [239 244 244]
              [239 244 244]]]
    '''
    image = ImageCaptcha()
    captcha_text = ''.join(random_captcha_text())

    captcha = image.generate(captcha_text)
    # image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

    # rm  =  'rm '+captcha_text + '.jpg'
    # print(rm)
    # os.system(rm)
    # time.sleep(10)

    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image)     # 得到一个 Numpy 数组，这个其实是把验证码转化成了每个像素的 RGB
    # print(captcha_image.shape)        # (60, 160, 3) 这其实代表验证码图片的高度是60，宽度是160，是60 x 160像素的验证码，每个像素都有 RGB 值，所以最后一维即为像素的 RGB 值

    return captcha_text, captcha_image

if __name__ == '__main__':
    # 测试
    while(True):
        text, image = gen_captcha_text_and_image()
        print('begin ', time.ctime(), type(image))
        f = plt.figure()
        ax = f.add_subplot(1, 1, 1)
        # 给坐标轴axes 增加说明
        ax.text(x=0.1, y=0.9, s=text, ha='center', va='center', transform=ax.transAxes)
        plt.imshow(image)

        plt.show()
        print('end ', time.ctime())