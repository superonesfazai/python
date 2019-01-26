# appium vs ios

## 依赖库安装
```bash
# 如果没有安装 libimobiledevice，会导致Appium无法连接到iOS的设备，所以必须要安装
# 如果要在iOS10+的系统上使用appium，则需要安装ios-deploy
$ brew install libimobiledevice --HEAD
$ npm install -g ios-deploy  

# 报错处理: stderr: xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
1. Install Xcode
2. $ sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

### appium-doctor安装
```bash
$ npm install appium-doctor -g
# 安装后执行appium-doctor --ios指令，可以查看与iOS相关配置是否完整，下图是全部配置都成功,如果有那一项是打叉的，则进行安装就可以了
$ appium-doctor --ios 

# 报错处理: WARN AppiumDoctor  ✖ Carthage was NOT found!
$ brew install carthage

# WARN AppiumDoctor  ✖ opencv4nodejs cannot be found.
$ brew install cmake && npm install -g opencv4nodejs

# ARN AppiumDoctor  ✖ ffmpeg cannot be found
https://www.ffmpeg.org/ 

# WARN AppiumDoctor  ✖ applesimutils cannot be found
$ brew tap wix/brew && brew install applesimutils

# WARN AppiumDoctor  ✖ idevicelocation cannot be found
1. $ brew install ideviceinstaller
2. $ brew update && brew uninstall --ignore-dependencies libimobiledevice && brew uninstall --ignore-dependencies usbmuxd 
3. $ brew install --HEAD usbmuxd && brew unlink usbmuxd && brew link usbmuxd
4. $ brew install --HEAD libimobiledevice && brew unlink libimobiledevice && brew install libimobiledevice
5. # 然后在clone https://github.com/JonGabilondoAngulo/idevicelocation进行相应安装

# 可选配置(更好的实现定位)
# WARN AppiumDoctor  ✖ fbsimctl cannot be found
$ brew tap facebook/fb && brew install fbsimctl --HEAD
```
![](https://i.loli.net/2019/01/26/5c4bc499bdfbb.png)

## 更新Appium中的WebDriverAgent
1. 到[WebDriverAgent](https://github.com/facebook/WebDriverAgent)下载最新版本的WebDriverAgent($ git clone git@github.com:facebook/WebDriverAgent.git)
2. 进入下载后的WebDriverAgent文件
3. 执行 ./Scripts/bootstrap.sh
4. 直接用Xcode打开WebDriverAgent.xcodepro文件
5. 配置WebDriverAgentLib和WebDriverAgentRunner的证书
![](https://i.loli.net/2019/01/26/5c4bc77409ba9.png)
![](https://i.loli.net/2019/01/26/5c4bc7933cdc2.png)
6. 连接并选择自己的iOS设备，然后按Cmd+U，或是点击Product->Test
7. 运行成功时，在Xcode控制台应该可以打印出一个Ip地址和端口号
![](https://i.loli.net/2019/01/26/5c4bc7c96c0b6.png)
8. 在网址上输入http://(iP地址):(端口号)/status，如果网页显示了一些json格式的数据，说明运行成功。
9. 进入到Appium中的WebDriverAgent目录，目录路径如下(/Applications/Appium.app/Contents/Resources/app/node_modules/appium/node_modules/appium-xcuitest-driver/
)
10. 将自己下载并编译后的WebDriverAgent替换Appium原有的WebDriverAgent

## 运行Appium-Desktop

### 准备工作
1. 需要一个.app 或是一个 .ipa 安装包，这个安装包是你要进行测试的应用程序
2. 测试应用程序对应的bundleId
3. 测试设备的udid,电脑连接上手机后，可以在Xcode的Window->Deriver中查看
![](https://i.loli.net/2019/01/26/5c4bc87eab379.png)

### 安装appium的python依赖库
```bash
$ git clone git@github.com:appium/python-client.git 
$ cd python-client
$ python setup.py install
```

### 测试文件
在git上下载测试文件[appiumSimpleDemo](https://link.jianshu.com/?t=https://github.com/zhshijie/appiumSimpleDemo.git)
1. 一个简单的iOS工程文件
2. 一个简单的python测试文件

### 开始自动化测试
1. 打开下载后的appiumSimpleDemo文件，打开appiumSimpleDemo.xcodepro程序,配置下TARGET的签名
2. 在appiumSimpleDemo的根目录执行编译指令，编译出一个app文件xcodebuild -sdk iphoneos -target appiumSimpleDemo -configuration Release，编译成功后app文件的地址会打印在命令行中
![](https://i.loli.net/2019/01/26/5c4bc93998629.png)
3. 将手机连接上电脑，在Xcode的Window->Devices中获取到设备的UDID
![](https://i.loli.net/2019/01/26/5c4bc97e9e6ba.png)

### 配置python文件
打开appiumSimpleDemo中的appiumSimpleDemo.py文件,将，修改setup中的几个参数，将app的路径，设备的相关信息修改成当前连接设备的信息。
![](https://i.loli.net/2019/01/26/5c4bc9b881f4a.png)
,保存。
### 运行Appium程序
打开之前下载安装的Appium，并开启服务。
### 运行python测试文件
在appiumSimpleDemo.py所在的目录运行python appiumSimpleDemo.py，如果之前设置都没有出错，那么程序应该会在手机上成功运行，并自动点击了entry next view进入到了下一个界面，过了2s后会重新返回第一个界面
