# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午12:23
# @File    : 自定义异常抛出_test.py

class ShortInputException(Exception):
    '''自定义异常类'''
    def __init__(self, length, atleast):
        # super().__init__()
        self.length = length
        self.atleast = atleast

def main():
    try:
        s = input('请输入 --> ')
        if len(s) < 3:
            # raise引发一个你定义的异常
            raise ShortInputException(len(s), 3)
    except ShortInputException as result:   # x这个变量被绑定到了错误的实例
        print('ShortInputException: 输入的长度是 %d,长度至少应是 %d'% (result.length, result.atleast))
    else:
        print('没有异常发生.')

main()