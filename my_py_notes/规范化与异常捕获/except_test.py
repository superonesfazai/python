# coding: utf-8

import time
import traceback

def test_01():
    try:
        # raise Exception('error_message')
        raise(Exception('error_message', 'error_code'))
    except Exception as e:
        # 打印异常
        print(type(e), e)

        time.sleep(0.1)

        # 打印异常消息
        print(type(e.args[0]), e.args[0])

        time.sleep(0.1)

        # 打印异常参数
        print(e.args, type(e.args[0]), e.args[0])

        time.sleep(0.1)

        # 打印异常堆栈跟踪信息 stack traceback
        traceback.print_exc()


def test_02():
    try:
        print('try')
        raise(Exception('try'))
    except Exception as e:
        print('except')
        raise(Exception('except'))
    finally:
        print('finally')

test_02()
test_01()
