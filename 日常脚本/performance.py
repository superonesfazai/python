#!/usr/bin/python3.5
# encoding: utf-8
__author__ = 'afa'

import time

def fast():
    time.sleep(0.001)

def slow():
    time.sleep(0.01)

def very_slow():
    for i in range(100):
        fast()
        slow()
    time.sleep(0.1)

def main():
    #性能测试用例
    very_slow()
    very_slow()

if __name__ == '__main__':
    main()
