#!/usr/bin/env python
# coding=utf-8

'''
#os.system('ls')
'''
import paramiko

#基于用户名和密码的sshclient方式的登录
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#port_num = 133
#ssh.connect('192.168.104.%d' % port_num, 22, 'python', 'chuanzhi')
#stdin, stdout, stderr = ssh.exec_command("cd a && mkdir c")
#print stdout.readlines()
#ssh.close()


#基于用户名和密码的transport方式的登录
# num = 109
# trans = paramiko.Transport(('192.168.104.%d' % num, 22))  #实例化一个transport对象
# trans.connect(username='python', password='chuanzhi')  #建立连接
#
# ssh = paramiko.SSHClient()
# ssh._transport = trans  #将sshclient的对象的transport指定为上面的trans
#
# stdin, stdout, stderr = ssh.exec_command('df -lh >> a.txt')  #执行命令
# stdin, stdout, stderr = ssh.exec_command('cd Desktop && du -lh >> b.txt')
# stdin, stdout, stderr = ssh.exec_command('cat a.txt > result.txt && \
#                 cat b.txt >> result.txt | cat result.txt')
# print(stdout.read())


# #基于公钥密钥的SSHClient方式的登录
# #指定本地的RSA私钥文件,如果建立密钥对时设置的有密码,password为设定的密码,如无不用指定password参数
# pkey = paramiko.RSAKey.from_private_key_file('/home/python/.ssh/id_rsa', password='12345')
# ssh = paramiko.SSHClient()  # 建立连接
# ssh.connect(hostname='192.168.104.109',
#             port=22,
#             username='python',
#             pkey=pkey)
# stdin, stdout, stderr = ssh.exec_command('df -lh')  # 执行命令
# # 结果放到stdout中，如果有错误将放到stderr中
# print(stdout.read())
# ssh.close()  # 关闭连接


# #基于密钥的 Transport 方式登录
# # 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
# pkey = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa', password='12345')
# # 建立连接
# trans = paramiko.Transport(('192.168.2.129', 22))
# trans.connect(username='super', pkey=pkey)
#
# # 将sshclient的对象的transport指定为以上的trans
# ssh = paramiko.SSHClient()
# ssh._transport = trans
#
# # 执行命令，和传统方法一样
# stdin, stdout, stderr = ssh.exec_command('df -hl')
# print(stdout.read().decode())
#
# # 关闭连接
# trans.close()

# #传文件 SFTP
# # 实例化一个trans对象# 实例化一个transport对象
# trans = paramiko.Transport(('192.168.2.129', 22))
# # 建立连接
# trans.connect(username='super', password='super')
#
# # 实例化一个 sftp对象,指定连接的通道
# sftp = paramiko.SFTPClient.from_transport(trans)
# # 发送文件
# sftp.put(localpath='/tmp/11.txt', remotepath='/tmp/22.txt')
# # 下载文件
# # sftp.get(remotepath, localpath)
# trans.close()


#实现输入命令立马返回结果的功能
import paramiko
import os
import select
import sys

# 建立一个socket
trans = paramiko.Transport(('192.168.104.109', 22))
# 启动一个客户端
trans.start_client()

# 如果使用rsa密钥登录的话
'''
default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
trans.auth_publickey(username='super', key=prikey)
'''
# 如果使用用户名和密码登录
trans.auth_password(username='python', password='chuanzhi')
# 打开一个通道
channel = trans.open_session()
# 获取终端
channel.get_pty()
# 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
channel.invoke_shell()
# 下面就可以执行你所有的操作，用select实现
# 对输入终端sys.stdin和 通道进行监控,
# 当用户在终端输入命令后，将命令交给channel通道，这个时候sys.stdin就发生变化，select就可以感知
# channel的发送命令、获取结果过程其实就是一个socket的发送和接受信息的过程
while True:
    readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
    # 如果是用户输入命令了,sys.stdin发生变化
    if sys.stdin in readlist:
        # 获取输入的内容
        input_cmd = sys.stdin.read(1)
        # 将命令发送给服务器
        channel.sendall(input_cmd)

    # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
    if channel in readlist:
        # 获取结果
        result = channel.recv(1024)
        # 断开连接后退出
        if len(result) == 0:
            print("\r\n**** EOF **** \r\n")
            break
        # 输出到屏幕
        sys.stdout.write(result)
        sys.stdout.flush()
# 关闭通道
channel.close()
# 关闭链接
trans.close()

# #支持tab自动补全
# import paramiko
# import os
# import select
# import sys
# import tty
# import termios
#
# '''
# 实现一个xshell登录系统的效果，登录到系统就不断输入命令同时返回结果
# 支持自动补全，直接调用服务器终端
#
# '''
# # 建立一个socket
# trans = paramiko.Transport(('192.168.104.109', 22))
# # 启动一个客户端
# trans.start_client()
#
# # 如果使用rsa密钥登录的话
# '''
# default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
# prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
# trans.auth_publickey(username='super', key=prikey)
# '''
# # 如果使用用户名和密码登录
# trans.auth_password(username='python', password='chuanzhi')
# # 打开一个通道
# channel = trans.open_session()
# # 获取终端
# channel.get_pty()
# # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
# channel.invoke_shell()
#
# # 获取原操作终端属性
# oldtty = termios.tcgetattr(sys.stdin)
# try:
#     # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
#     tty.setraw(sys.stdin)
#     channel.settimeout(0)
#
#     while True:
#         readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
#         # 如果是用户输入命令了,sys.stdin发生变化
#         if sys.stdin in readlist:
#             # 获取输入的内容，输入一个字符发送1个字符
#             input_cmd = sys.stdin.read(1)
#             # 将命令发送给服务器
#             channel.sendall(input_cmd)
#
#         # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
#         if channel in readlist:
#             # 获取结果
#             result = channel.recv(1024)
#             # 断开连接后退出
#             if len(result) == 0:
#                 print("\r\n**** EOF **** \r\n")
#                 break
#             # 输出到屏幕
#             sys.stdout.write(result.decode())
#             sys.stdout.flush()
# finally:
#     # 执行完后将现在的终端属性恢复为原操作终端属性
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
#
# # 关闭通道
# channel.close()
# # 关闭链接
# trans.close()


