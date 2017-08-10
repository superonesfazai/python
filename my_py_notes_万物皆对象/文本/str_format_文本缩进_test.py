# encoding: utf-8

# python3环境下测试

# indent_test
# 测试缩进

bb = {'001': 'a', '000000002': 'bbbbbb', '0003': 'c', '0000004': 'ddd'}

for a, b in bb.items():
    print('%-20s: %s' % (a, b))


def print_fill_with():
    input_str_list = [
        "abc",
        "abcd",
        "abcde",
    ]

    for eachStr in input_str_list:
        # print '{:->10}'.format(eachStr)
        print('{0:->10}'.format(eachStr))
        # -------abc
        # ------abcd
        # -----abcde

    for eachStr in input_str_list:
        print('{0:-<20}'.format(eachStr))
        # abc-----------------
        # abcd----------------
        # abcde---------------

    for eachStr in input_str_list:
        print('{0:*^30}'.format(eachStr))
        # *************abc**************
        # *************abcd*************
        # ************abcde*************


if __name__ == "__main__":
    print_fill_with()

    a = '好长的汉字啊一定是...'
    b = '影视/媒体/艺术/文化'

    print(len(a))
    print(len(a.encode('utf-8')))
    print(len(b.encode('utf-8')))

'''
测试结果:
001                 : a
000000002           : bbbbbb
0000004             : ddd
0003                : c
-------abc
------abcd
-----abcde
abc-----------------
abcd----------------
abcde---------------
*************abc**************
*************abcd*************
************abcde*************
12
30
27
'''

'''
注意: 由于默认编码格式不一样
python2下
len(a)为30
a.encode('utf-8'))为12
b.encode('utf-8'))为11
'''