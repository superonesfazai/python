# coding=utf-8

# 在python2.7的环境下调试,3以上报错

import sys
from fzutils.time_utils import fz_timer

a = {1: 1, 2: 2}
b = {1: 2, 3: 3}

# way 2
@fz_timer(sys.stdout.write)
def test_3():
    c = a.copy()
    c.update(b)
    print(c)

if __name__ == '__main__':
    """
    字典合并的几种方式效率测试
    因时间太短，将测试时间调整到小数后6位
    """
    test_3()


# 测试结果
# 方法test_1开始时间：Tue May  5 17:56:38 2015
# {1: 2, 2: 2, 3: 3}
# 方法test_1结束时间：Tue May  5 17:56:38 2015
# 方法test_1运行时间：0.000039S
# 方法test_2开始时间：Tue May  5 17:56:38 2015
# {1: 2, 2: 2, 3: 3}
# 方法test_2结束时间：Tue May  5 17:56:38 2015
# 方法test_2运行时间：0.000009S
# 方法test_3开始时间：Tue May  5 17:56:38 2015
# {1: 2, 2: 2, 3: 3}
# 方法test_3结束时间：Tue May  5 17:56:38 2015
# 方法test_3运行时间：0.000009S

# 结论：
# 一、当KEY重复，后面的VALUE会覆盖前面
# 二、后两种方案效率较高，推荐第二种方案
