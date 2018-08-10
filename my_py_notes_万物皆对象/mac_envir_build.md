# 送给老是换mac的人 

## 安装sublime3
http://www.sublimetext.com/3

## 安装搜狗输入法
地址：https://pinyin.sogou.com/mac/ 
- 换肤
	- 偏好设置 -> 外观 -> 更多皮肤
	- 选择World Earth Day皮肤下载, 然后双击打开即可
	- 接着选 候选词个数: 7个，卷轴模式

## 安装latern
https://github.com/getlantern/download/wiki

## 安装shadowsocks
具体安装: https://github.com/ziggear/shadowsocks
```
(由于没有设置成默认, server每次重启, 都要重新run)
# 后台运行
$ sudo ssserver -p 443 -k password -m aes-256-cfb --user nobody -d start
# 停止
$ sudo ssserver -d stop
```

## 安装Alfred3
https://www.alfredapp.com/

## 安装chrome(最新版)

## 安装pycharm
- 2018破解(https://blog.csdn.net/u014044812/article/details/78727496)
- 注意: 安装时不要安装IdeaVim插件, 否则部分快键键无法使用
- 主题地址(http://www.themesmap.com/details.html?id=56af4d27333ecc1800c392b3)
- keymap设置为Eclipse(Mac os X) | 加个command+F为查找, command+option+r为替换 | 
- Editor->Font->Size: 14
- Eclipse(mac os x)快键键
    - 全部收缩 ⌘- 折叠树视图中的所有节点 
    - 展开全部 ⌘+ 展开树视图中的所有节点

## shell
- 设置背景色(终端->偏好设置->描述文件->Grass 字体15磅->点击默认)

## brew(网速要求较高)
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

## oh-my-zsh
地址: https://github.com/robbyrussell/oh-my-zsh
```
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# 当前用户设置为zsh
chsh -s /bin/zsh

# 改变主题
vi ~/.zshrc
# 修改为pygmalion
```

## vimplus(强大的vim)(没有自动提示)
https://github.com/chxuan/vimplus
```
$ git clone https://github.com/chxuan/vimplus.git ~/.vimplus
$ cd ~/.vimplus
$ ./install.sh
```

## vimrc star 14万
https://github.com/amix/vimrc

## 或者安装MacVim
开源地址: https://github.com/Valloric/YouCompleteMe
下载地址: https://github.com/macvim-dev/macvim/releases
```shell
# 下载完毕后shell下要想打开mvim，新建个软连接
$ sudo ln -s /Applications/MacVim.app/Contents/bin/mvim /usr/local/bin/mvim
# 即可打开
$ mvim
```


## 安装FileZilla
https://filezilla-project.org/download.php?type=client

## appstore 安装Dr.Cleaner

## 安装appcleaner
http://freemacsoft.net/appcleaner/

## python环境搭建(最好是直接brew install python3::但是这样下载的是最新版本3.7, 坑非常多!! 还是用下面的方法安装python3.6.3)因为会附带安装pip3
python3.6.3 下载

https://www.python.org/ftp/python/3.6.3/python-3.6.3-macosx10.6.pkg

### 安装Xcode command line tool(可以先不装)
```
$ xcode-select --install
```

### 安装pip3
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py
```

### IPProxyPool
https://github.com/qiyeboy/IPProxyPool
```
pip3 install requests chardet web.py==0.40.dev1 sqlalchemy gevent psutil
```

### 安装fzutils
```
$ pip3 install fzutils

# 安装pymssql, 先安装freetds
$ brew unlink freetds
$ brew install freetds@0.91
$ brew link --force freetds@0.91
$ pip3 install pymssql
```

## appstore安装Magnet

## 安装charlesproxy
https://www.charlesproxy.com/latest-release/download.do

- 注册码: https://www.jianshu.com/p/89111882fa99
- https抓取设置: https://www.jianshu.com/p/ec0a38d9a8cf

注意：在iOS 10.3之前,当你将安装一个自定义证书,iOS会默认信任,不需要进一步的设置。而iOS 10.3之后,安装新的自定义证书默认是不受信任的。如果要信任已安装的自定义证书,需要手动打开开关以信任证书。

## 安装mitmproxy
```
# 会附带安装mitmdump
pip3 install mitmproxy

# 并在手机上安装mitmproxy的证书
```

## 安装cheatsheet (mac快键键提示工具)
https://cheatsheet-mac.en.softonic.com/mac

## 安装Navicat Premium破解版
http://www.sdifen.com/navicatpremium11215.html

## 安装wps
http://www.wps.cn/product/wpsmac/

## 安装docker
https://store.docker.com/editions/community/docker-ce-desktop-mac
```shell
# *NOTICE*: 下面的容器名都可采用容器id的前几个字母代替

# 搜索某个镜像
$ docker search ubuntu

# 远程拉取某个镜像
$ docker pull ubuntu:latest

# 推送镜像到远程仓库
$ docker push superonesfazai/fz_ubuntu:0.0.0.0.1

# 列出镜像中文件和目录的变化
$ docker diff container_id

# 查看docker镜像
$ docker images

# 首次启动容器:
# -i 代表保持STDIN开启，-t 代表为容器分配一个tty, 
# --name自定义容器名, -p指定端口映射(前者为虚拟机端口，后者为容器端口), 成功后返回容器id 
$ docker run -it -d --name fz_ubuntu -p 8088:80 ubuntu

# 进入docker(或者把容器id改为容器名，也可以进入)
$ docker exec -it [container_id/容器名] /bin/bash

# 退出容器
$ exit

# 停止容器
$ docker stop container_id

# 杀掉running的容器
$ docker kill container_id

# 删除容器
$ docker rm container_id

# 重启停止的容器
$ docker start container_id

# 重启running的容器
$ docker restart container_id

# 显示镜像或容器的详细信息
$ docker inspect container_id

# 创建容器镜像(保存镜像状态)(每次版本号都要变)
# 0.0.0.0.1为版本号(必须), 镜像名字随意, -a是作者信息, -m是提交信息, --pause=true是在提交镜像时暂停容器(参数可省)
$ docker commit [-a "super_fazai<superonesfazai@gmail.com>" -m "修复bug"] container_id fz_ubuntu:0.0.0.0.1

# 此时镜像只能本地使用, 在其他机器使用需打包  
$ docker save -o fz_ubuntu.tar fz_ubuntu:0.0.0.0.1

# 将tar压缩文件保存为image
$ docker load --input fz_ubuntu.tar

# 把容器系统文件打包并导出来，方便分发给其他场景使用
$ docker export fz_ubuntu > fz_ubuntu.tar

# 拷贝容器中的文件
$ docker cp container_id:path host_path

# 查看容器输出
$ docker top container_id

# 要与容器分离并回到之前的终端访问点，可以按 CTRL+P 接着 CTRL+Q 执行脱离操作。
# “附着”在一个Docker容器上，基本上相当于从一个VPS内部访问另一个VPS。

# 从脱离的状态想要回到附着的状态，需要执行如下步骤：
1.用 sudo docker ps 列出所有运行中的容器
2.找到之前创建的那个容器的ID
3.执行 sudo docker attach [id] 完成当前终端到该容器的附着

# 终止状态的容器可以用 docker ps -a 命令看到
处于终止状态的容器，可以通过 docker start 命令来重新启动
可以使用 docker rm 来删除一个处于终止状态的容器。(rm 后面跟的是他的容器的ID)
如果要删除一个运行中的容器，可以添加 -f 参数。Docker 会发送 SIGKILL 信号给容器。

# 清理所有处于终止状态的容器
$ docker rm $(docker ps -a -q)

# 要获取容器的输出信息，可以通过 docker logs 命令
$ docker logs [container ID or NAMES]
```

## 安装Caffeine

## 安装xcode(也可不装, 通过共享wifi)
```
# 用于wireshark抓包iphone
rvictl -s [uuid]
```

## 安装appium
下载地址: https://github.com/appium/appium-desktop/releases

java jdk下载地址: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

android studio下载地址: http://tools.android-studio.org/
```bash
### ios真机
$ brew install carthage
# Appium iOS真实设备支持取决于中央第三方软件套件 libimobiledevice
$ brew install libimobiledevice
$ brew install node
# Appium对使用Xcode 8+运行iOS 9.3及更高版本的真实设备的支持也依赖于ios-deploy
$ brew install ios-deploy
# 对于混合或Web测试，您还需要遵循 ios-webkit-debug-proxy 设置说明
$ brew install ios-webkit-debug-proxy

```
```bash
### android
$ brew install npm
$ npm install wd
# adb
$ brew cask install android-platform-tools

# 安装Genymotion模拟器
http://www.genymotion.net/
# 上诉模拟器依靠virtualbox, 请先下载
https://www.virtualbox.org/wiki/Downloads
# Genymotion无法安装apk解决方案
https://blog.csdn.net/xiaolong20081/article/details/79204251
# 下载5.1_Lolli... 
链接：http://pan.baidu.com/s/1skPELxN 密码：086j

# 查看连接状况
$ adb devices -l

# 需要配置启动App时的Desired Capabilities参数，
# 它们分别是platformName、deviceName、appPackage、appActivity。
platformName：它是平台名称，需要区分Android或iOS，此处填写Android。
deviceName：它是设备名称，此处是手机的具体类型。(model: 之间的参数 device:)
appPackage：它是App程序包名。
appActivity：它是入口Activity名，这里通常需要以'.'开头。
```

## android逆向

## 安装dash

## qt designer + pycharm开发GUI
首先下载qt最新安装包.dmg, 并安装

流程可参考: https://www.jianshu.com/p/094928ac0b73
```bash
$ pip3 install pyqt5
```

## 安装网易云音乐
https://music.163.com/#/download