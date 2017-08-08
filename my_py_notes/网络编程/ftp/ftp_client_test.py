# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午5:11
# @File    : ftp_client_test.py

# 下方程序用于下载网站中最新版本的文件,你也可以修改此程序让它下载你喜欢的东西

import ftplib
import os
import socket

host = 'ftp.mozilla.org'
dirn = 'pub/mozilla.org/webtools'
file = 'bugzilla-LATEST.tar.gz'

def main():
    try:
        f = ftplib.FTP(host)
    except (socket.error, socket.gaierror) as e:
        print('error:cannot reach "%s"' % host)
        return
    print('***Connected to host "%s"' % host)

    try:
        f.login()
    except ftplib.error_perm:
        print('error: cannot login anonymously')
        f.quit()
        return
    print('***Logged in as "anonymous"')

    try:
        f.cwd(dirn)
    except ftplib.error_perm:
        print('error: cannot cd to "%s"' % dirn)
        f.quit()
        return
    print('*** Changed to "%s" folder' % dirn)

    try:
        f.retrbinary('retr %s' % file, open(file, 'wb').write)
    except ftplib.error_perm:
        print('error: cannot read file "%s"' % file)
        os.unlink(file)
    else:
        print('*** Downloaded "%s" to CWD' % file)
    f.quit()
    return

if __name__ == '__main__':
    main()
