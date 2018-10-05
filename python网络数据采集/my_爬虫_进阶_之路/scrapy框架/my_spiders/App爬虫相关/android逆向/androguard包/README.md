# androguard
Androguard是一个完整的python工具，可以播放Android文件。

- DEX，ODEX
- APK
- Android的二进制xml
- Android资源
- 反汇编DEX / ODEX字节码
- DEX / ODEX文件的反编译器

您既可以使用cli或图形前端进行androguard，也可以将androguard纯粹用作自己的工具和脚本的库。

[官方文档](https://androguard.readthedocs.io/en/latest/)

`pip3 install androguard`

## 使用Androlyze
分析APK文件的最简单方法是使用androlyze.py。它将启动一个iPython shell并加载所有模块以实现操作。

为了分析和加载APK或DEX文件，存在一些包装函数。使用AnalyzeAPK(filename)或AnalyzeDEX(filename)加载文件并开始分析。在androguard repo中已经有很多APK，您可以使用其中一个，也可以开始自己的分析。

```bash
$ androlyze.py
Androguard version 3.2.1 started
In [1]: a, d, dx = AnalyzeAPK("examples/android/abcore/app-prod-debug.apk")
# Depending on the size of the APK, this might take a while...

In [2]:
```
你得到的三个对象是a一个APK对象，d一个DalvikVMFormat对象数组和dx一个Analysis对象。

在APK对象内部，您可以找到有关APK的所有信息，例如包名称，权限，AndroidManifest.xml或其资源。

该DalvikVMFormat对应于DEX文件中的APK文件中。您可以从DEX文件中获取类，方法或字符串。但是当使用多DEX APK时，从另一个地方获取它们可能是个更好的主意。Analysis应该使用该对象，因为它包含特殊的类，它们链接有关classes.dex的信息，甚至可以同时处理许多DEX文件。

## 获取有关APK的信息
如果您已经成功加载了APK AnalyzeAPK，您现在可以开始获取有关APK的信息。

- 获取APK的权限
```bash
In [2]: a.get_permissions()
Out[2]:
['android.permission.INTERNET',
 'android.permission.WRITE_EXTERNAL_STORAGE',
 'android.permission.ACCESS_WIFI_STATE',
 'android.permission.ACCESS_NETWORK_STATE']
```
- 获取AndroidManifest.xml中定义的所有活动的列表
```bash
In [3]: a.get_activities()
Out[3]:
['com.greenaddress.abcore.MainActivity',
 'com.greenaddress.abcore.BitcoinConfEditActivity',
 'com.greenaddress.abcore.AboutActivity',
 'com.greenaddress.abcore.SettingsActivity',
 'com.greenaddress.abcore.DownloadSettingsActivity',
 'com.greenaddress.abcore.PeerActivity',
 'com.greenaddress.abcore.ProgressActivity',
 'com.greenaddress.abcore.LogActivity',
 'com.greenaddress.abcore.ConsoleActivity',
 'com.greenaddress.abcore.DownloadActivity']
```
- 获取包名称，应用程序名称和图标路径
```bash
In [4]: a.get_package()     # 包名称
Out[4]: 'com.greenaddress.abcore'

In [5]: a.get_app_name()    # 应用程序名称
Out[5]: u'ABCore'

In [6]: a.get_app_icon()
Out[6]: u'res/mipmap-xxxhdpi-v4/ic_launcher.png'
```
- 获取数字版本和版本字符串，以及最小，最大，目标和有效的SDK版本
```bash
In [7]: a.get_androidversion_code()
Out[7]: '2162'

In [8]: a.get_androidversion_name()
Out[8]: '0.62'

In [9]: a.get_min_sdk_version()
Out[9]: '21'

In [10]: a.get_max_sdk_version()

In [11]: a.get_target_sdk_version()
Out[11]: '27'

In [12]: a.get_effective_target_sdk_version()
Out[12]: 27
```
- 甚至可以获取AndroidManifest.xml的解码XML
```bash
In [15]: a.get_android_manifest_axml().get_xml()
Out[15]: '<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="2162" android:versionName="0.62" package="com.greenaddress.abcore">\n<uses-sdk android:minSdkVersion="21" android:targetSdkVersion="27">\n</uses-sdk>\n<uses-permission android:name="android.permission.INTERNET">\n</uses-permission>\n<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE">\n</uses-permission>\n<uses-permission android:name="android.permission.ACCESS_WIFI_STATE">\n</uses-permission>\n<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE">\n</uses-permission>\n<application android:theme="@7F0F0006" android:label="@7F0E001D" android:icon="@7F0D0000" android:debuggable="true" android:allowBackup="false" android:supportsRtl="true">\n<activity android:name="com.greenaddress.abcore.MainActivity">\n<intent-filter>\n<action android:name="android.intent.action.MAIN">\n</action>\n<category android:name="android.intent.category.LAUNCHER">\n</category>\n</intent-filter>\n</activity>\n<service android:name="com.greenaddress.abcore.DownloadInstallCoreIntentService" android:exported="false">\n</service>\n<service android:name="com.greenaddress.abcore.RPCIntentService" android:exported="false">\n</service>\n<service android:name="com.greenaddress.abcore.ABCoreService" android:exported="false">\n</service>\n<activity android:name="com.greenaddress.abcore.BitcoinConfEditActivity">\n<intent-filter>\n<category android:name="android.intent.category.DEFAULT">\n</category>\n<action android:name="com.greenaddress.abcore.BitcoinConfEditActivity">\n</action>\n</intent-filter>\n</activity>\n<activity android:name="com.greenaddress.abcore.AboutActivity">\n</activity>\n<activity android:label="@7F0E0038" android:name="com.greenaddress.abcore.SettingsActivity" android:noHistory="true">\n</activity>\n<activity android:label="@7F0E0035" android:name="com.greenaddress.abcore.DownloadSettingsActivity" android:noHistory="true">\n</activity>\n<activity android:theme="@7F0F0006" android:label="@7F0E0036" android:name="com.greenaddress.abcore.PeerActivity">\n</activity>\n<activity android:theme="@7F0F0006" android:label="@7F0E0037" android:name="com.greenaddress.abcore.ProgressActivity">\n</activity>\n<activity android:name="com.greenaddress.abcore.LogActivity">\n</activity>\n<activity android:name="com.greenaddress.abcore.ConsoleActivity">\n</activity>\n<activity android:name="com.greenaddress.abcore.DownloadActivity">\n</activity>\n<receiver android:name="com.greenaddress.abcore.PowerBroadcastReceiver">\n<intent-filter>\n<action android:name="android.intent.action.ACTION_POWER_CONNECTED">\n</action>\n<action android:name="android.intent.action.ACTION_POWER_DISCONNECTED">\n</action>\n<action android:name="android.intent.action.ACTION_SHUTDOWN">\n</action>\n<action android:name="android.intent.action.ACTION_BATTERY_LOW">\n</action>\n<action android:name="android.net.wifi.STATE_CHANGE">\n</action>\n</intent-filter>\n</receiver>\n</application>\n</manifest>\n'
```
- 或者，如果您想将AndroidManifest.xml用作ElementTree对象，请使用以下方法
```bash
In [13]: a.get_android_manifest_xml()
Out[13]: <Element manifest at 0x7f9d01587b00>
```
- 获取证书
```bash
In [15]: a.get_certificates()
Out[15]: [<asn1crypto.x509.Certificate 8069905488 b'0\x82\x03V0\x82\x02>\xa0\x03\x02\x01\x02\x02\x04N\xfe\xc9j0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000m1\x0b0\t\x06\x03U\x04\x06\x13\x02CN1\x100\x0e\x06\x03U\x04\x08\x13\x07Beijing1\x100\x0e\x06\x03U\x04\x07\x13\x07Beijing1\x120\x10\x06\x03U\x04\n\x13\tByteDance1\x120\x10\x06\x03U\x04\x0b\x13\tByteDance1\x120\x10\x06\x03U\x04\x03\x13\tMicro Cao0\x1e\x17\r111231083554Z\x17\r390518083554Z0m1\x0b0\t\x06\x03U\x04\x06\x13\x02CN1\x100\x0e\x06\x03U\x04\x08\x13\x07Beijing1\x100\x0e\x06\x03U\x04\x07\x13\x07Beijing1\x120\x10\x06\x03U\x04\n\x13\tByteDance1\x120\x10\x06\x03U\x04\x0b\x13\tByteDance1\x120\x10\x06\x03U\x04\x03\x13\tMicro Cao0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xa4m\x10\x8b\xe8\'\xbf\xf2\xc1\xacz\xd9\x86\xc4c\xb8\xcd\xa9\xf0\xe7\xdd\xc2\x12\x95\xafU\xbd\x16\xf7\xbf\xab\xb3o\xa3;r\xa8\xe7oZY\xb4\x8b)\xcbn4\xc3\x8d\x06U\x89cm\xd1 \xf3\x93F\xc3{7S\x83\x04"\xcc\x0c\x84$?\xdf\x0e(\xd3\xe5\x97\r\xcdd\x1cp\xc9\xe2\xe3\xecf\xac\x14\xaf\xd3Q\xab\xb5\x9dh\x857\x0e\x16\xb6K\xbf\xb2\x8f\xbb#M\xff\xe2_\\\xfbf\x80\xc8A!w\x0c\xf3\xa1w\xbc\x8a(\xb7\x8b|\x86\xd3\na\xebg\xb9\xfb\xfd\x92\xe0\xc8\xfc^\xb84j#\x8d\xdf\xe0\x85"\xf0\x91\xc6"x\x992\xd9\xde\xbei\x10\xb4\xb9\x03\xd0._m\xedi\xf5\xc1:]\x17B\xda\xc2\x10P\xdf\xbb_N\xa6\x15\x02\x8dz\x86B\xe4\xa9>\x07\\\xf8\xf0\xe3:JeJ\xf1\x1fO\x9aI\x05\xd9\x17\xf0\xbb\xb8Nc\xa1\xa2\xe9\x0b\x89\x97\xf96\xe5\xbfZu\xeam\x19\xd1\xd9=&w\x88nY\xe9\\\x0b\xb35\x056<\x05\xe1\n8\x9d\x0b\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00\x87\x04\xe57X\x90}\xb6x[\xece\xc5\xf5\x1a\xf0P\x87<K\n^\x08\xf9\x01\x91\xb9\x01\xc5\x99i\xceSyB\xdb\xc90\x7f\x8f\xcc#\xb1\xc2\x81\xa6o\xe4a6\x89\x05d\xf8\x9f\xb1h9\xaci\xf86\xa9\xea\x07N\xb0=\xa8W\x830\xabP\xb1\x85\xbdi\x16\xf1\x95\xa6p6\x06\n\x0b\xbf*\xed\x06\x99\x0er\xbcM\xed\xe8\x95\xae^iSq\xaaJ\xd2n\xfc\xd4Ke\x89\x1b\xda\x9c\xe0-\x9eqT\x85\x92\xc2\x95\x1e,\xb6.\xd4@\x8e\xec~\x82\x8c\xe5s\xff\xba\x04X4\x1a\xef%\x95{*v@=\xa0\x912.\xb8E\xb6\xa9\x90?\xe6\xae\xd1C@\x12\xd4\x83\xf1\xc6h\xe2F\x8c\xe1)\x81^\x18(;\xaa^\x1cB\ti\x1b6\xff\xa8e\x06\xffjK\x83\xf2O\xaatC\x83\xb7Yh\x04lip=,]\xf3\x8b\xadi \xd9\x12,\xb1\xf7\xc7\x8e\x8b\xfe(8p5\x9c\x051\x15\xe2\xba\nz\x03\xc9ej/Z-\x81\xf6\xa6\xfa\xd5\xdb,\xd7'>]
```
- 获取声明的权限列表
```bash
In [17]: a.get_declared_permissions()
Out[17]: 
['com.ss.android.ugc.aweme.permission.C2D_MESSAGE',
 'com.ss.android.ugc.aweme.permission.READ_ACCOUNT',
 'com.ss.android.ugc.aweme.permission.WRITE_ACCOUNT',
 'com.ss.android.ugc.aweme.push.permission.MESSAGE',
 'com.ss.android.ugc.aweme.permission.MIPUSH_RECEIVE']
```
- 获取主要活动的名称
```bash
In [22]: a.get_main_activity()
Out[22]: 'com.ss.android.ugc.aweme.splash.SplashActivity'
```
- 获取apk的原始字节
```bash
In [23]: a.get_raw()
```
- 获取所有接收者的android：name属性
```bash
In [25]: a.get_receivers()
Out[25]: 
['com.ss.android.ugc.aweme.common.net.NetworkReceiver',
 'com.ss.android.ugc.aweme.common.net.NetWorkStateReceiver',
 'com.ss.android.download.DownloadReceiver',
 'com.ss.android.socialbase.downloader.downloader.DownloadReceiver',
 'com.ss.android.common.applog.HotsoonReceiver',
 'com.ss.android.ugc.aweme.livewallpaper.receiver.LiveWallPaperPluginInstalledReceiver',
 'com.ss.android.ugc.aweme.live.sdk.chatroom.receiver.PhoneReceiver',
 'com.ss.android.push.daemon.PushReceiver',
 'com.huawei.push.service.receivers.HWPushMessageHandler',
 'com.huawei.android.pushagent.PushEventReceiver',
 'com.huawei.android.pushagent.PushBootReceiver',
 'com.ss.android.message.MessageReceiver',
 'com.ss.android.message.sswo.SswoReceiver',
 'com.baidu.android.pushservice.RegistrationReceiver',
 'com.igexin.sdk.PushReceiver',
 'com.xiaomi.push.service.receivers.NetworkStatusReceiver',
 'com.xiaomi.push.service.receivers.PingReceiver',
 'com.xiaomi.push.service.receivers.MIPushMessageHandler',
 'com.taobao.accs.EventReceiver',
 'com.taobao.accs.ServiceReceiver',
 'com.taobao.agoo.AgooCommondReceiver',
 'com.aliyun.AliyunMessageReceiver',
 'com.ss.android.ugc.awemepushlib.message.ScreenOnPushActionReceiver',
 'com.meizu.message.MzMessageReceiver',
 'com.ss.android.ugc.awemepushlib.message.ScreenReceiver',
 'com.ss.android.ugc.awemepushlib.receiver.NotificationBroadcastReceiver',
 'com.ss.android.downloadlib.core.download.DownloadReceiver',
 'com.ss.android.article.base.feature.plugin.PluginReportReceiver',
 'com.bytedance.ttnet.hostmonitor.ConnectivityReceiver',
 'com.ss.android.socialbase.appdownloader.DownloadReceiver',
 'com.alibaba.sdk.android.push.SystemEventReceiver',
 'com.meizu.cloud.pushsdk.SystemReceiver',
 'com.vivo.VivoPushMessageReceiver',
 'com.tt.miniapphost.placeholder.MiniappReceiver0',
 'com.tt.miniapphost.placeholder.MiniappReceiver1',
 'com.tt.miniapphost.placeholder.MiniappReceiver2',
 'com.tt.miniapphost.placeholder.MiniappReceiver3',
 'com.tt.miniapphost.placeholder.MiniappReceiver4',
 'com.bytedance.frameworks.plugin.receiver.MiraErrorLogReceiver',
 'com.ss.android.push.window.oppo.ScreenReceiver',
 'com.ss.android.push.DefaultReceiver']
```
- 获取所有服务的android：name属性
```bash
In [26]: a.get_services()
```
- 获取签名文件名列表（v1签名/ JAR签名）
```bash
In [27]: a.get_signature_names()
Out[27]: ['META-INF/FUNNYGAL.RSA']
```
- 获取签名文件的数据列表。只有v1 / JAR签名。
```bash
In [28]: a.get_signatures()
Out[28]: [b'0\x82\x05.\x06\t*\x86H\x86\xf7\r\x01\x07\x02\xa0\x82\x05\x1f0\x82\x05\x1b\x02\x01\x011\x0b0\t\x06\x05+\x0e\x03\x02\x1a\x05\x000\x0b\x06\t*\x86H\x86\xf7\r\x01\x07\x01\xa0\x82\x03Z0\x82\x03V0\x82\x02>\xa0\x03\x02\x01\x02\x02\x04N\xfe\xc9j0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000m1\x0b0\t\x06\x03U\x04\x06\x13\x02CN1\x100\x0e\x06\x03U\x04\x08\x13\x07Beijing1\x100\x0e\x06\x03U\x04\x07\x13\x07Beijing1\x120\x10\x06\x03U\x04\n\x13\tByteDance1\x120\x10\x06\x03U\x04\x0b\x13\tByteDance1\x120\x10\x06\x03U\x04\x03\x13\tMicro Cao0\x1e\x17\r111231083554Z\x17\r390518083554Z0m1\x0b0\t\x06\x03U\x04\x06\x13\x02CN1\x100\x0e\x06\x03U\x04\x08\x13\x07Beijing1\x100\x0e\x06\x03U\x04\x07\x13\x07Beijing1\x120\x10\x06\x03U\x04\n\x13\tByteDance1\x120\x10\x06\x03U\x04\x0b\x13\tByteDance1\x120\x10\x06\x03U\x04\x03\x13\tMicro Cao0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xa4m\x10\x8b\xe8\'\xbf\xf2\xc1\xacz\xd9\x86\xc4c\xb8\xcd\xa9\xf0\xe7\xdd\xc2\x12\x95\xafU\xbd\x16\xf7\xbf\xab\xb3o\xa3;r\xa8\xe7oZY\xb4\x8b)\xcbn4\xc3\x8d\x06U\x89cm\xd1 \xf3\x93F\xc3{7S\x83\x04"\xcc\x0c\x84$?\xdf\x0e(\xd3\xe5\x97\r\xcdd\x1cp\xc9\xe2\xe3\xecf\xac\x14\xaf\xd3Q\xab\xb5\x9dh\x857\x0e\x16\xb6K\xbf\xb2\x8f\xbb#M\xff\xe2_\\\xfbf\x80\xc8A!w\x0c\xf3\xa1w\xbc\x8a(\xb7\x8b|\x86\xd3\na\xebg\xb9\xfb\xfd\x92\xe0\xc8\xfc^\xb84j#\x8d\xdf\xe0\x85"\xf0\x91\xc6"x\x992\xd9\xde\xbei\x10\xb4\xb9\x03\xd0._m\xedi\xf5\xc1:]\x17B\xda\xc2\x10P\xdf\xbb_N\xa6\x15\x02\x8dz\x86B\xe4\xa9>\x07\\\xf8\xf0\xe3:JeJ\xf1\x1fO\x9aI\x05\xd9\x17\xf0\xbb\xb8Nc\xa1\xa2\xe9\x0b\x89\x97\xf96\xe5\xbfZu\xeam\x19\xd1\xd9=&w\x88nY\xe9\\\x0b\xb35\x056<\x05\xe1\n8\x9d\x0b\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00\x87\x04\xe57X\x90}\xb6x[\xece\xc5\xf5\x1a\xf0P\x87<K\n^\x08\xf9\x01\x91\xb9\x01\xc5\x99i\xceSyB\xdb\xc90\x7f\x8f\xcc#\xb1\xc2\x81\xa6o\xe4a6\x89\x05d\xf8\x9f\xb1h9\xaci\xf86\xa9\xea\x07N\xb0=\xa8W\x830\xabP\xb1\x85\xbdi\x16\xf1\x95\xa6p6\x06\n\x0b\xbf*\xed\x06\x99\x0er\xbcM\xed\xe8\x95\xae^iSq\xaaJ\xd2n\xfc\xd4Ke\x89\x1b\xda\x9c\xe0-\x9eqT\x85\x92\xc2\x95\x1e,\xb6.\xd4@\x8e\xec~\x82\x8c\xe5s\xff\xba\x04X4\x1a\xef%\x95{*v@=\xa0\x912.\xb8E\xb6\xa9\x90?\xe6\xae\xd1C@\x12\xd4\x83\xf1\xc6h\xe2F\x8c\xe1)\x81^\x18(;\xaa^\x1cB\ti\x1b6\xff\xa8e\x06\xffjK\x83\xf2O\xaatC\x83\xb7Yh\x04lip=,]\xf3\x8b\xadi \xd9\x12,\xb1\xf7\xc7\x8e\x8b\xfe(8p5\x9c\x051\x15\xe2\xba\nz\x03\xc9ej/Z-\x81\xf6\xa6\xfa\xd5\xdb,\xd71\x82\x01\x9c0\x82\x01\x98\x02\x01\x010u0m1\x0b0\t\x06\x03U\x04\x06\x13\x02CN1\x100\x0e\x06\x03U\x04\x08\x13\x07Beijing1\x100\x0e\x06\x03U\x04\x07\x13\x07Beijing1\x120\x10\x06\x03U\x04\n\x13\tByteDance1\x120\x10\x06\x03U\x04\x0b\x13\tByteDance1\x120\x10\x06\x03U\x04\x03\x13\tMicro Cao\x02\x04N\xfe\xc9j0\t\x06\x05+\x0e\x03\x02\x1a\x05\x000\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x04\x82\x01\x005\xbf( \xfb\x1a\x85\xa3\x02\xf4\x89\xab\xa9\xda\xb6\xaeX:\x05\x11\xe3a7\xde\xd1\xe9\x92\xf3\xe9h#\x8e\x90\x86vKG"\xb4\r5\xf9\x11[\\\xe3\x17\xe4\xbe\xed\xe7\x91\x87\x97\xd1\xc5\x10,U\xc7\x81\xce\'x?\x863\x12\x8a%\x9a\xdd\x98\xd5S\xd6\xd0Ph\xc1UI\x11g\x12|w\xa9\xfd}P\x19\xf7\xe9\\\x83\x93\xc6\x17\r\xc4\x95\xfbZ\xe5iP2\x1fA\xef\xe9\xaf\x98\xc0\xb5\xb5\x07\xf0Q?Gm\xb7\xe0\xdf\xc5\x0e \xfc\x9dOR\xe2\x11o\xa6bhY=\xf3\xd3H<\xa8\xc6\xedHJ\xb7\xb6J\xaf\xc1\xf5\xe0p\xf9w\\@\xd0\xd2\xc5zE\xae$\xcen\x88\x02\xe3%\xe3\xe9\xb4\x1cQ<\x04N\xd0\xad\x01\xf0\xa1`t\xed8X88\x8bj\xd3{\xcd6\xbd\x08\xfd\xee\xc9g\xe0\x17\x04\xc5\x8d\xe8\xe1\x86\xc7\x06\xb7\xd2\xafl\xf1J\xfb\x95n\xe6E\x02fp\x98\xae\x08}%\x94\x01i\x10=Yo\xa5f$\xcd\xf0\xcdN\xb1\xdbb*\xa1\xa5']
```
- 如果找到v1或v2（或两者）签名，则返回true
```bash
In [29]: a.is_signed()
Out[29]: True
```
- 如果APK有效则返回true，否则返回false。如果AndroidManifest.xml可以成功解析，则APK被视为有效。这并不意味着APK具有有效签名，也不意味着APK可以安装在Android系统上。
```bash
In [30]: a.is_valid_APK()
Out[30]: True
```
- 获取apk内的文件名
```bash
In [33]: a.get_files()
Out[33]: 
['AndroidManifest.xml',
 'META-INF/android.arch.core_runtime.version',
 'META-INF/android.arch.lifecycle_extensions.version',
 'META-INF/android.arch.lifecycle_livedata-core.version',
 'META-INF/android.arch.lifecycle_livedata.version',
 'META-INF/android.arch.lifecycle_reactivestreams.version',
 'META-INF/android.arch.lifecycle_runtime.version',
 'META-INF/android.arch.lifecycle_viewmodel.version',
 'META-INF/android.arch.paging_runtime.version',
 'META-INF/android.arch.persistence.room_runtime.version',
 'META-INF/android.arch.persistence.room_rxjava2.version',
 'META-INF/android.arch.persistence_db-framework.version',
 'META-INF/android.arch.persistence_db.version',
 'META-INF/aweme_release.kotlin_module',
 'META-INF/com.android.support_animated-vector-drawable.version',
 'META-INF/com.android.support_appcompat-v7.version',
 'META-INF/com.android.support_design.version',
 'META-INF/com.android.support_recyclerview-v7.version',
 'META-INF/com.android.support_support-compat.version',
 'META-INF/com.android.support_support-core-ui.version',
 'META-INF/com.android.support_support-core-utils.version',
 'META-INF/com.android.support_support-fragment.version',
 'META-INF/com.android.support_support-media-compat.version',
 'META-INF/com.android.support_support-v4.version',
 'META-INF/com.android.support_support-vector-drawable.version',
 'META-INF/com.android.support_transition.version',
 'META-INF/commerce.impl_release.kotlin_module',
 'META-INF/commerce.service_release.kotlin_module',
 'META-INF/kotlin-stdlib-common.kotlin_module',
 'META-INF/kotlin-stdlib-jdk7.kotlin_module',
 'META-INF/kotlin-stdlib.kotlin_module',
 'META-INF/proguard/com.ss.android.vesdk.VEAudioRecorder.pro',
 'META-INF/proguard/com.ss.android.vesdk.VEEditor.pro',
 'META-INF/proguard/com.ss.android.vesdk.VERecorder.pro',
 'META-INF/rxjava.properties',
 'META-INF/services/com.google.protobuf.GeneratedExtensionRegistryLoader',
 'META-INF/services/javax.annotation.processing.Processor',
 'META-INF/tools-library_release.kotlin_module',
 'assets/3scountdown.json',
 'assets/AZURE2d.png',
 'assets/AkzidenzGrotesk-BoldCondAlt.otf',
 'assets/BLUE2d.png',
 'assets/CYAN2d.png',
...]
```
a还有很多方法可供探索，只需看看API即可 [APK](https://androguard.readthedocs.io/en/latest/api/androguard.core.bytecodes.html#androguard.core.bytecodes.apk.APK)

## 使用analysis对象
该~androguard.core.analysis.analysis.Analysis对象包含有关一个或多个DEX文件中的类，方法，字段和字符串的所有信息。

此外，它还允许您为每个方法，类，字段和字符串获取调用图和交叉引用（XREF）。

这意味着您可以调查某些API调用的应用程序或创建图形以查看不同类的依赖关系。

作为第一个例子，我们将从Analysis中获取所有类：
```bash
In [2]: dx.get_classes()
Out[2]:
[<analysis.ClassAnalysis Ljava/io/FileNotFoundException; EXTERNAL>,
 <analysis.ClassAnalysis Landroid/content/SharedPreferences; EXTERNAL>,
 <analysis.ClassAnalysis Landroid/support/v4/widget/FocusStrategy$BoundsAdapter;>,
 <analysis.ClassAnalysis Landroid/support/v4/media/MediaBrowserCompat$MediaBrowserServiceCallbackImpl;>,
 <analysis.ClassAnalysis Landroid/support/transition/WindowIdImpl;>,
 <analysis.ClassAnalysis Landroid/media/MediaMetadataEditor; EXTERNAL>,
 <analysis.ClassAnalysis Landroid/support/v4/app/BundleCompat$BundleCompatBaseImpl;>,
 <analysis.ClassAnalysis Landroid/support/transition/MatrixUtils$1;>,
 <analysis.ClassAnalysis Landroid/support/v7/widget/ShareActionProvider;>,
 ...
```
如您所见，get_classes()返回一个[ClassAnalysis](https://androguard.readthedocs.io/en/latest/api/androguard.core.analysis.html#androguard.core.analysis.analysis.ClassAnalysis)对象列表 。其中一些标记为EXTERNAL，这意味着此类的源代码未在Analysis内部加载的DEX文件中定义。例如，第一个类java.io.FileNotFoundException是API类。

A ClassAnalysis不包含实际代码，但[ClassDefItem](https://androguard.readthedocs.io/en/latest/api/androguard.core.bytecodes.html#androguard.core.bytecodes.dvm.ClassDefItem)可以使用以下代码加载 get_vm_class()：
```bash
In [41]: list(dx.get_classes())[2].get_vm_class()
Out[41]: <dvm.ClassDefItem Ljava/lang/Object;->La/b;>
```
如果类是EXTERNAL，ExternalClass则返回a 

该ClassAnalysis还包含了所有的XREF的信息，这些信息更详细的下一节

## 使用会话
如果您正在处理更大的APK，您可能希望保存当前的工作并稍后再回来。这就是会话的原因：它们允许您将工作保存在磁盘上并随时恢复。会话还可用于将分析存储在磁盘上，例如，如果您进行自动分析并希望稍后分析某些文件。

有几种方法可以使用会话。最简单的方法是使用AnalyzeAPK()会话：
```python
from androguard import misc
from androguard import session

# get a default session
sess = misc.get_default_session()

# Use the session
a, d, dx = misc.AnalyzeAPK("examples/android/abcore/app-prod-debug.apk", session=sess)

# Show the current Session information
sess.show()

# Do stuff...

# Save the session to disk
session.Save(sess, "androguard_session.p")

# Load it again
sess = session.Load("androguard_session.p")
```
会话信息如下所示：
```bash
APKs in Session: 1
    d5e26acca809e9cdfaece18afd8e63c60a26d7b6d566d70bd9f44d6934d5c433: [<androguard.core.bytecodes.apk.APK object at 0x7fcecf4f3f10>]
DEXs in Session: 2
    8bd7e9f48a6ed29e4c678633364e8bfd4e6ae76ef3e50c43a5ec3c00eb10a5bc: <analysis.Analysis VMs: 2, Classes: 3092, Strings: 3293>
    e2a1e46ecd03b701ce72c31057581e0104279d142fca06cdcdd000dd94a459e0: <analysis.Analysis VMs: 2, Classes: 3092, Strings: 3293>
Analysis in Session: 1
    d5e26acca809e9cdfaece18afd8e63c60a26d7b6d566d70bd9f44d6934d5c433: <analysis.Analysis VMs: 2, Classes: 3092, Strings: 3293>
```
注意，会话对象存储了大量数据并且可以变得非常大！建议不要在自动环境中使用会话，其中加载了hundrets或数千个APK。

如果您想使用会话但仅为一个或多个APK保持会话活动，您可以reset()在会话上调用该方法，以删除所有存储的分析数据。
```python
from androguard import misc
from androguard import session
import os

# get a default session
sess = misc.get_default_session()

for root, dirs, files in os.walk("examples"):
    for f in files:
        if f.endswith(".apk"):
            # Use the session
            a, d, dx = misc.AnalyzeAPK(os.path.join(root, f), session=sess)

            # Do your stuff

            # Maybe save the session to disk...

            # But now reset the session for the next analysis
            sess.reset()
```
## 使用JADX作为反编译器
您也可以使用[JADX](https://github.com/skylot/jadx)，而不是使用内部反编译器DAD 。

按照其网站上的说明安装JADX。确保jadx可执行文件在$PATH。否则，您可以在调用时设置参数 [DecompilerJADX()](https://androguard.readthedocs.io/en/latest/api/androguard.decompiler.html#androguard.decompiler.decompiler.DecompilerJADX)。

如何使用JADX:
```python
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
from androguard.decompiler.decompiler import DecompilerJADX
from androguard.core.androconf import show_logging
import logging

# Enable log output
show_logging(level=logging.DEBUG)

# Load our example APK
a = APK("examples/android/TestsAndroguard/bin/TestActivity.apk")

# Create DalvikVMFormat Object
d = DalvikVMFormat(a)
# Create Analysis Object
dx = Analysis(d)

# Load the decompiler
# Make sure that the jadx executable is found in $PATH
# or use the argument jadx="/path/to/jadx" to point to the executable
decompiler = DecompilerJADX(d, dx)

# propagate decompiler and analysis back to DalvikVMFormat
d.set_decompiler(decompiler)
d.set_vmanalysis(dx)

# Now you can do stuff like:
for m in d.get_methods()[:10]:
    print(m)
    print(decompiler.get_source_method(m))
```
## Android签名证书
Androguard能够获取有关APK中发现的签名证书的信息。在Androguard的最新版本中，已使用不同的解析器来获取证书信息。第一解析器是[奇尔卡特](https://www.chilkatsoft.com/)，然后混合物[pyasn1](https://pypi.org/project/pyasn1/)和[密码](https://pypi.org/project/cryptography/)被使用，而最近的解析器使用[asn1crypto](https://pypi.org/project/asn1crypto/)库。并非所有x509解析器都适用于所有证书，因为有很多示例证明证书创建者不遵循RFC来创建证书。某些解析器不接受此类损坏的证书，并且无法解析它们。

Androids签名过程的目的不是提供有关作者的验证信息，例如JAR签名，而是仅提供检查APK完整性的方法，以及通过比较证书指纹来检查是否可以升级APK。在某种意义上，证书信息可用于查找来自同一作者的其他APK - 只要签名密钥保密即可！还有公共可用的签名密钥，例如来自AOSP的签名密钥，因此两个APK的相同指纹并不总是告诉您它是由同一个人签名的。

如果您想了解有关APK签名过程的更多信息，请阅读有关[签名](https://source.android.com/security/apksigning/)的官方文档。还有一个官方工具来验证和签署名为[apksigner](https://developer.android.com/studio/command-line/apksigner)的 APK 。

### 使用证书
在APK内部，有两个证书位置：

- v1 aka JAR签名：文件META-INF夹中的PKCS＃7文件
- v2 aka APK签名：ZIP中包含DER编码证书的特殊部分

获取证书信息的最简单方法是androsign。它为[apksigner](https://developer.android.com/studio/command-line/apksigner)提供类似的输出，但仅使用androguard。但它无法验证文件的完整性。
```bash
$ androsign.py --all --show examples/signing/apksig/golden-aligned-v1v2-out.apk
golden-aligned-v1v2-out.apk, package: 'android.appsecurity.cts.tinyapp'
Is signed v1: True
Is signed v2: True
Found 1 unique certificates
Issuer: CN=rsa-2048
Subject: CN=rsa-2048
Serial Number: 0x8e35306cdd0115f7L
Hash Algorithm: sha256
Signature Algorithm: rsassa_pkcs1v15
Valid not before: 2016-03-31 14:57:49+00:00
Valid not after: 2043-08-17 14:57:49+00:00
sha1 0aa07c0f297b4ae834dc85a17eea8c2cf9380ff7
sha256 fb5dbd3c669af9fc236c6991e6387b7f11ff0590997f22d0f5c74ff40e04fca8
sha512 4da6e6744a4dabef192b198be13b4492b0ce97469f3ce223dd9b7e8df2ee952328e06651e5e65dd3b60ac5e3946e16cf7059b20d4d4a649957c1e3055c2e1fb8
md5 e995a5ed7137307661f854e66901ee9e
```
作为比较，这是apksigner的输出:
```bash
$ apksigner verify -verbose --print-certs examples/signing/apksig/golden-aligned-v1v2-out.apk
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Number of signers: 1
Signer #1 certificate DN: CN=rsa-2048
Signer #1 certificate SHA-256 digest: fb5dbd3c669af9fc236c6991e6387b7f11ff0590997f22d0f5c74ff40e04fca8
Signer #1 certificate SHA-1 digest: 0aa07c0f297b4ae834dc85a17eea8c2cf9380ff7
Signer #1 certificate MD5 digest: e995a5ed7137307661f854e66901ee9e
Signer #1 key algorithm: RSA
Signer #1 key size (bits): 2048
Signer #1 public key SHA-256 digest: 8cabaedf32f1052f6bc5edbeb84d1c500f8c1aa15f8944bf22c46e44c5c4f7e8
Signer #1 public key SHA-1 digest: a708f9a777bac814e6634b02521224537ec3e019
Signer #1 public key MD5 digest: c0c8801fabf2ad970282be1c41584003
```

最有趣的部分是probaby证书的指纹（不是公钥的指纹！）。您可以使用它来搜索类似的APK。有时会对这个指纹产生混淆：指纹不是整个PKCS＃7文件的校验和，而只是它的某个部分！从两个不同但同样签名的APK计算PKCS＃7文件的哈希值将导致不同的哈希值。指纹将保持不变。

Androguard提供了[androguard.core.bytecodes.apk.APK](https://androguard.readthedocs.io/en/latest/api/androguard.core.bytecodes.html#androguard.core.bytecodes.apk.APK) 类中的方法来迭代那里找到的证书。
```bash
from androguard.core.bytecodes.apk import APK

a = APK('examples/signing/apksig/golden-aligned-v1v2-out.apk')

# first check if this APK is signed
print("APK is signed: {}".format(a.is_signed()))

if a.is_signed():
    # Test if signed v1 or v2 or both
    print("APK is signed with: {}".format("both" if a.is_signed_v1() and
    a.is_signed_v2() else "v1" if a.is_signed_v1() else "v2"))

# Iterate over all certificates
for cert in a.get_certificates():
    # Each cert is now a asn1crypt.x509.Certificate object
    # From the Certificate object, we can query stuff like:
    cert.sha1  # the sha1 fingerprint
    cert.sha256  # the sha256 fingerprint
    cert.issuer.human_friendly  # issuer
    cert.subject.human_friendly  # subject, usually the same
    cert.hash_algo  # hash algorithm
    cert.signature_algo  # Signature algorithm
    cert.serial_number  # Serial number
    cert.contents  # The DER coded bytes of the certificate itself
    # ...
```
有关该类功能的更多信息，请参阅asn1crypto [文档](https://github.com/wbond/asn1crypto#documentation)Certificate！

## androgui - Androguard GUI
```bash
usage: androgui.py [-h] [-d] [-i INPUT_FILE] [-p INPUT_PLUGIN]

Androguard GUI

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug
  -i INPUT_FILE, --input_file INPUT_FILE
  -p INPUT_PLUGIN, --input_plugin INPUT_PLUGIN
```
## androcg - 从APK创建调用图
[文档](https://androguard.readthedocs.io/en/latest/tools/androcg.html)

## androdd -反编译APK及创建CFG
[文档](https://androguard.readthedocs.io/en/latest/tools/androdd.html#androdd-decompile-apks-and-create-cfg)

## androdis - DEX的反汇编程序
```bash
Usage: androdis.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        file : use this filename (DEX/ODEX)
  -o OFFSET, --offset=OFFSET
                        offset to disassemble
  -s SIZE, --size=SIZE  size
```

## androauto - 运行自己的分析
使用androauto进入自动模式。
```bash
Usage: androauto.py [options]

Options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory=DIRECTORY
                        directory input
  -v, --verbose         add debug
```