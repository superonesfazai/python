# Xposed
Xposed框架是一款可以在不修改APK的情况下影响程序运行（修改系统）的框架服务，通过替换/system/bin/app_process程序控制zygote进程，使得app_process在启动过程中会加载XposedBridge.jar这个jar包，从而完成对Zygote进程及其创建的Dalvik虚拟机的劫持。

基于Xposed框架可以制作出许多功能强大的模块，且在功能不冲突的情况下同时运作。

此外，Xposed框架中的每一个库还可以单独下载使用，如Per APP Setting（为每个应用设置单独的dpi或修改权限）、Cydia、XPrivacy（防止隐私泄露）、BootManager（开启自启动程序管理应用）对原生Launcher替换图标等应用或功能均基于此框架。

Xposed框架是基于一个Android的本地服务应用XposedInstaller与一个提供API 的jar文件来完成的。

[官网](https://repo.xposed.info/)

[源码](https://github.com/rovo89/Xposed)

## 安装

### 安装本地服务XposedInstaller 
需要安装XposedInstall.apk本地服务应用，我们能够在其官网的framework栏目中找到，下载并安装。[地址](http://repo.xposed.info/module/de.robv.android.xposed.installer)

安装好后进入XposedInstaller应用程序，会出现需要激活框架的界面, 这里我们点击“安装/更新”就能完成框架的激活了。部分设备如果不支持直接写入的话，可以选择“安装方式”，修改为在Recovery模式下自动安装即可。

因为安装时会存在需要Root权限，安装后会启动Xposed的app_process，所以安装过程中会存在设备多次重新启动。

```bash
TIPS：由于国内的部分ROM对Xposed不兼容，如果安装Xposed不成功的话，强制使用Recovery写入可能会造成设备反复重启而无法正常启动。
```

### 下载使用API库
其API库XposedBridgeApi-.jar（version是XposedAPI的版本号)

我们能够在Xposed的官方支持xda论坛找到，其[地址](http://forum.xda-developers.com/xposed/xposed-api-changelog-developer-news-t2714067)

下载完毕后我们需要将 Xposed Library 复制到 lib目录（注意是 lib 目录不是Android提供的 libs 目录），然后将这个 jar 包添加到 Build PATH 中