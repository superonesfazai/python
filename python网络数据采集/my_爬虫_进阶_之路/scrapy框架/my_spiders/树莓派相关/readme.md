# 树莓派
[树莓派官网](https://www.raspberrypi.org/)

## sd卡系统刻录相关
[balenaEtcher下载](https://www.balena.io/etcher/)

## enable ssh
## enable vnc

## 更改密码
```bash
$ passwd
```

## vnc远程桌面连接
VNC就是一款可以让你通过手机或者电脑远程控制另一台主机的软件，在我们操作树莓派的时候，就可以通过VNC远程控制，而不再需要另外配置显示器和键盘。

现在的树莓派都默认安装VNC服务的，所以我们很简单就能通过命令行开启VNC。

首先进入系统，打开终端，或者通过远程SSH登陆树莓派。

### 开启vnc
1. 进入树莓派配置界面
```bash
$ sudo raspi-config
```
![](https://i.loli.net/2019/08/22/OE1FyNjiPzcxQvq.png)

2. 选择「5 Interfacing Options」，按回车
![](https://i.loli.net/2019/08/22/ceXR6n8mOdl2Psq.png)

3. 选择「P3 VNC」，按回车
![](https://i.loli.net/2019/08/22/ygAMwUex6JNTPiB.png)

4. 这里问你是否开启VNC服务，选择「Yes」，按回车
![](https://i.loli.net/2019/08/22/L4mzj7g29vZbAF8.png)

5. 提示已经开启VNC服务，按回车确认，之后退出树莓派配置界面
![](https://i.loli.net/2019/08/22/uty6QkzrpneObXL.png)

至此我们已经打开了树莓派的VNC服务，接下来，是通过软件进行VNC远程桌面控制。

### 使用VNC Viewer连接树莓派
推荐使用：VNC Viewer，免费易用。[下载地址](https://www.realvnc.com/en/connect/download/viewer/)

(vnc账户 已存在Chrome vnc书签)

1. 打开VNC Viewer
2. 在地址栏上面输入树莓派的IP地址(eg: 192.168.2.168)，按回车, 即可登录进入树莓派ui页

## 树莓派python开发环境搭建
```bash
```

### vim 变成IDE
代码自动补全神器

[YouCompleteMe](https://github.com/ycm-core/YouCompleteMe)
