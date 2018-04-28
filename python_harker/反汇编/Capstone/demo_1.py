# coding:utf-8

'''
@author = super_fazai
@File    : demo_1.py
@Time    : 2018/4/26 10:29
@connect : superonesfazai@gmail.com
'''

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"

md = Cs(CS_ARCH_X86, CS_MODE_64)
for i in md.disasm(CODE, 0x1000):
    print("0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))