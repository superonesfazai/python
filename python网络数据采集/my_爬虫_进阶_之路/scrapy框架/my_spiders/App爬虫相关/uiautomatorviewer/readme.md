# uiautomatorviewer

## 启动
mac 
```bash
$ cd /Users/afa/Library/Android/sdk/tools/bin && ./uiautomatorviewer
```

### 先卸载atx(必须)
因为uiautomator是独占资源，所以当atx运行的时候uiautomatorviewer是不能用的

### uiautomatorviewer不能手机截屏(eg: atx 中oppo r7s黑屏)
解决方案
```bash
$ adb -s JNPJJREEY5NBS88D shell uiautomator dump /sdcard/app.uix  
$ adb -s JNPJJREEY5NBS88D pull /sdcard/app.uix /Users/afa/myFiles/app.uix
$ adb -s JNPJJREEY5NBS88D shell screencap -p /sdcard/app.png
$ adb -s JNPJJREEY5NBS88D pull /sdcard/app.png /Users/afa/myFiles/app.png

# 上方代码执行过后
# 再打开ui automator viewer导入文件夹，选择这两个文件即可(每次使用uiautomatorviewer都得设置)
```

## 报错处理
1. Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist! Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist!

解决方案

下载对应版本的android sdk。

遗留问题

某些手机厂商的就是不识别，比如魅族Note3（Android 5.0.1）还是不能识别。