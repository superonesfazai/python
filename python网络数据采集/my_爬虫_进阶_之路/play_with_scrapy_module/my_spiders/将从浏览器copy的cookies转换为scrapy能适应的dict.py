# coding = utf-8

'''
@author = super_fazai
@File    : 将从浏览器copy的cookies转换为scrapy能适应的dict.py
@Time    : 2017/9/5 20:50
@connect : superonesfazai@gmail.com
'''

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie
    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = input("请粘贴你复制的cookie：")
    trans = transCookie(cookie)
    print(trans.stringToDict())