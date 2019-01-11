# xposed
Xposed Framework 为来自国外XDA论坛（forum.xda-developers.com）的rovo89自行开发的一个开源的安卓系统框架。

Xposed框架的原理是修改系统文件，替换了/system/bin/app_process可执行文件，在启动Zygote时加载额外的jar文件（/data/data/de.robv.android.xposed.installer/bin/XposedBridge.jar），并执行一些初始化操作(执行XposedBridge的main方法)。然后我们就可以在这个Zygote上下文中进行某些hook操作。

[github](https://github.com/rovo89/Xposed)

[download](https://repo.xposed.info/module/de.robv.android.xposed.installer)

## download
[安装过程](https://blog.csdn.net/fuchaosz/article/details/53143216)

XposedInstaller_*.apk from this thread: Must be installed to manage installed modules, the framework won't work without it.

xposed*.zip from https://dl-xda.xposed.info/framework/: Must be flashed with a custom recovery (e.g. TWRP) to install the framework.

- SDK21 is Android 5.0 (Lollipop), 
- SDK22 is Android 5.1 (also Lollipop) 
- SDK23 is Android 6.0 (Marshmallow).
- SDK24 is Android 7.0 
- SDK25 is Android 7.1.
- SDK26 is Android 8.0 and SDK27 is Android 8.1.

I only support the latest Xposed version per Android release!

xposed-uninstaller*.zip from https://dl-xda.xposed.info/framework/: Can be flashed with a custom recovery (e.g. TWRP) to uninstall the framework.

The small .asc files are GPG signatures of the .zip files. You can verify them against this key (fingerprint: 0DC8 2B3E B1C4 6D48 33B4 C434 E82F 0871 7235 F333). That's actually the master key, the files are signed with subkey 852109AA.

# VirtualXposed
无需root的xposed

[github](https://github.com/android-hacker/VirtualXposed)

## 安装
从[发布页面](https://github.com/android-hacker/VirtualXposed/releases)下载最新的APK ，并将其安装在您的Android设备上。

### 安装APP和Xposed模块
打开VirtualXposed，单击主页底部的抽屉按钮（或长按屏幕），将所需的APP和Xposed模块添加到VirtualXposed的虚拟环境中。

注意：所有操作（Xposed Module，APP的安装）必须在VirtualXposed中完成，否则安装的Xposed模块将不会生效。

例如，如果您在系统上安装YouTube应用程序（手机的原始系统，而不是VirtualXposed），然后在VirtualXposed中安装YouTube AdAway（YouTube Xposed模块）; 

或者您在VirtualXposed中安装YouTube，并在原始系统上安装YouTube AdAway; 或者两者都安装在原始系统上，这三种情况都不会起作用！

将应用程序或Xposed模块安装到VirtualXposed有三种方法：

1. 从原始系统克隆已安装的应用程序。（单击主页底部的“按钮”，然后单击“添加应用程序”，第一页显示已安装应用程序的列表。）
2. 通过APK文件安装。（单击主页底部的按钮，然后单击添加应用程序，第二页显示在SD卡中找到的APK）
3. 通过外部文件选择器安装。（单击主页底部的按钮，然后单击添加应用程序，使用浮动操作按钮选择要安装的APK文件）

对于Xposed Module，您也可以从Xposed Installer安装它。

#### 激活Xposed模块
在VirtualXposed中打开Xposed Installer，转到模块片段，检查要使用的模块：

#### 重启
您只需重启VirtualXposed，无需重启手机 ; 只需单击VirtualXposed主页中的Settings，单击Reboot按钮，VirtualXposed将立即重启。

## 基于xposed开发

注意修改的是app/build.gradle配置里面的配置
```bash
repositories {
    jcenter();
}

dependencies {
    provided 'de.robv.android.xposed:api:82'
    provided 'de.robv.android.xposed:api:82:sources'
}
```
[blog1](https://blog.csdn.net/niubitianping/article/details/52571438)

[blog2](https://blog.csdn.net/yzzst/article/details/47659479)