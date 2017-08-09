# coding = utf-8

'''
@author = super_fazai
@File    : python版本判断_test.py
@Time    : 2017/8/8 14:06
@connect : superonesfazai@gmail.com
'''

import sys

def main():
    if sys.version_info.major >= 3:
        input_func = input      # otherwise use 'raw_input'
    else:
        input_func = raw_input

    print('python version is python%d %s' % (sys.version_info.major, input_func))

if __name__ == '__main__':
    main()