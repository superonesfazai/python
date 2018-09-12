# python沙箱逃逸的n种姿势
Python的沙箱逃逸是一些OJ,Quantor网站渗透测试的重要渠道, 这里主要从一些语言特性和一些技巧上来讲解python的一些元知识以及如何突破限制达到我们渗透的目的

此处的沙箱逃逸 代表的意思是: 从一个被阉割和做了严格限制的python执行环境中获取到更高的权限,甚至getshell

## 概述
沙箱逃逸,就是在给我们的一个代码执行环境下(Oj或使用socat生成的交互式终端),脱离种种过滤和限制,最终成功拿到shell权限的过程

对于python的沙箱逃逸而言,我们来实现目的的最终想法有以下几个

- 使用os包中的popen,system两个函数来直接执行shell
- 使用commands模块中的方法
- 使用subprocess
- 使用写文件到指定位置,再使用其他辅助手段
- 总体来说,我们使用以下几个函数,就可以直接愉快的拿到shell啦!
```python
import os
import subprocess
import commands

# 直接输入shell命令,以ifconfig举例
os.system('ifconfig')
os.popen('ifconfig')
commands.getoutput('ifconfig')
commands.getstatusoutput('ifconfig')
subprocess.call(['ifconfig'],shell=True)
```
但是,可以确定的是,防御者是不会这么轻易的让我们直接拿到shell的,肯定会有各种过滤,对代码进行各种各样的检查,来阻止可能的进攻
防御者会怎么做呢

## 常见的实战应用场景
- 直接的代码环境

常见的就是各种提供在线代码运行的网站,还有一些虚拟环境,以及一些编程练习网站,这种来说一般过滤较少,很容易渗透,但是getshell之后会相当麻烦,大多数情况下这类网站的虚拟机不仅与物理系统做了隔离还删除了很多内网渗透时实用的工具比如ifconfig之类的,后渗透工作相当的费工夫

- 提供的python交互式shell

这种情况较为少见,但是总体来说根据业务场景的不同一般会做很多的限制,但总体来说还是比较容易突破防御的

- SSTI

SSTI的情况下,模板的解析就是在一个被限制的环境中的
在flask框架动态拼接模板的时候,使用沙盒逃逸是及其致命的,flask一般直接部署在物理机器上面,getshell可以拿到很大的权限.