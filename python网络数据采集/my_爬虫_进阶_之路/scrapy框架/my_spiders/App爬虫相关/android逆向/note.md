# apktool用法
官方地址: http://ibotpeaches.github.io/Apktool/install/
```bash
# 检查Java环境是否Ready
$ java -version
```

#### apktool环境配置
1. 获取apktool脚本, 复制里面内容保存为apktool 地址: https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool
2. apktool.jar 文件 地址: https://bitbucket.org/iBotPeaches/apktool/downloads/
3. 重命名下载的jar为apktool.jar
4. Move both files (apktool.jar & apktool) to /usr/local/bin (root needed)
```bash
$ cp /Users/afa/Downloads/apktool /usr/local/bin
$ cp /Users/afa/Downloads/apktool.jar /usr/local/bin
```
5. Make sure both files are executable (chmod +x)
```bash
$ cd /usr/local/bin && chmod +x apktool && chmod +x apktool.jar
```
6. Try running apktool via cli

# jd_gui
jd_gui主要是为了方便查看 dex2jar 转换的jar文件结构和部分代码(未混淆)

版本地址: https://github.com/java-decompiler/jd-gui/releases 

下载地址: https://github.com/java-decompiler/jd-gui/releases/download/v1.4.0/jd-gui-1.4.0.jar

然后放到常用文件夹
```bash
$ java -jar jd-gui-1.4.0.jar
```

* 常用操作: Search

# dex2jar用法
1. 下载 dex2jar，并解压, 放到常用文件夹下 地址: https://sourceforge.net/projects/dex2jar/files/
```bash
# 进入dex2jar目录, 给与权限
$ chmod +x d2j_invoke.sh d2j-dex2jar.sh
```
2. 将测试的安装包xxx.apk后缀改为.zip，解压后拷贝classes.dex文件到dex2jar文件目录下，cmd进入改目录，执行dex2jar.bat classes.dex命令，会生成classes-dex2jar.jar文件；
```bash
# shell下面解压到指定文件夹
$ unzip -x aweme_dy_4_v2.3.0_1aac92c.zip -d /Users/afa/Downloads/抖音
```
```bash
$ ./d2j-dex2jar.sh classes.dex
```
3. 打开jd-gui工具，然后将生成的classes-dex2jar.jar文件拖进去，即可看见反编译的文件

# Android Apk反编译步骤
1. 使用Apktool反编译.apk文件,目的是获取未被混淆的资源文件(除混淆资源文件/加壳的apk外)

   作用：主要查看res文件下xml文件、AndroidManifest.xml和图片。（注意：如果直接解压.apk文件，xml文件打开全部是乱码）
```bash
$ apktool d your.apk
```

2. 使用解压软件解压.apk文件,获取classes.dex文件,使用dex2jar转换为可以使用jd_gui打开的jar文件

   作用：将apk反编译成Java源码（classes.dex转化成jar文件）
```bash
$ d2j-dex2jar.sh classes.dex
```
生成文件 classes-dex2jar.jar ,使用jd_gui打开即可.