# buildbot
Buildbot是开源的自动化软件构建，测试，发布流程的框架。

Buildbot支持跨平台，分布式，并行执行jobs，与版本控制系统的灵活集成，丰富的状态报告等等。

Buildbot是一个作业调度系统：它会对作业进行排队，在所需要的资源可用时执行任务，并报告结果。

Buildbot有一个或多个主机和从机。主机监控源代码库的变化，调配从机，并给用户和开发者报告结果。从机可在多种操作系统上运行。

可以配置Python脚本到主机。这个脚本可以简单到只配置内置组件，也可以充分发挥python所长，可以动态生成的配置，定制的组件及其他任何你能想到的。

该框架基于Twisted实现，并与所有主要的操作系统兼容。

Buildbot支持持续集成，持续部署，发布管理等的。Buildbot支持持续集成测试，自动化复杂的编译系统，应用程序部署和复杂的软件发布流程管理。比CruiseControl或Jenkins更适合混合语言的环境。在 Chromium,WebKit, Firefox, Python和Twisted等有广泛的使用。

[github](https://github.com/buildbot/buildbot)

[官网](http://buildbot.net)