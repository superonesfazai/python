# Genymotion与xposed

## 安装步骤

1. 打开Genymotion，点Add，自行选取一个Android 6.0(sdk 23)的镜像(打开之后会遇到问题，Genymotion底层是X86架构，不能运行为ARM架构编写的APP，这里要用[Genymotion-ARM-Translation](https://pan.baidu.com/s/17_3QkN0opGso_iP5Pj1jAw)(密码：26mq)来让Geymotion能运行X86的APP)

2. 之后就要进行Root, 可参考[文章](https://www.findhao.net/easycoding/1707), SuperSU必须使用V2.46，文中链接已失效，我重新查找后已重新上传，这里是[Super SU V2.46](https://pan.baidu.com/s/1JevSgNg98iRYuaVKhVry6A)(密码: nf1f)。

    1. 刷入genymotion arm transltor(非常重要的步骤，以便让x86架构的genymotion 镜像里支持arm架构的app。
    直接拖动下载的genymotion arm translator到开启的android 镜像里，会提示你是否刷入，选择是，然后等待提示刷入成功。)
    2. 刷入supersu，重启(类似上述步骤刷入即可。
    注意，也可以通过shell刷入，首先把文件传入到android 6.0以后，通过)($ adb shell flash-archive.sh /sdcard/Download/UPDATE-SuperSU-v2.65-20151226141550.zip)(flash-archive.sh是genymotion提供的一个刷入zip文件的脚本，在/system/bin/下，后面的路径是你选择的要输入的文件路径，在虚拟机里。)
    3. 刷入supersu，重启
    
3. 重启之后刷入[Xposed框架](https://pan.baidu.com/s/1mMfkd0k14J8xirP7L1iKvA)(密码: ex7f)

4. 再次重启，安装[Xposed Installer](https://pan.baidu.com/s/1RkNNSh-NnrkQCGkAWpCInA)(密码: jtpe)

完毕之后即可直接安装Xposed模块，就可进行Geymotion与Android Studio的交互.