# requirejs
RequireJS是一个非常小巧的JavaScript模块载入框架，是AMD规范最好的实现者之一。最新版本的RequireJS压缩后只有14K，堪称非常轻量。它还同时可以和其他的框架协同工作，使用RequireJS必将使您的前端代码质量得以提升。

在浏览器中可以作为js文件的模块加载器，也可以用在Node和Rhino环境，这段话描述了requirejs的基本功能"模块化加载"

优点:
- 防止js加载阻塞页面渲染
- 使用程序调用的方式加载js, 防出现如下丑陋的场景
```html
<script type="text/javascript" src="a.js"></script>
<script type="text/javascript" src="b.js"></script>
<script type="text/javascript" src="c.js"></script>
<script type="text/javascript" src="d.js"></script>
<script type="text/javascript" src="e.js"></script>
<script type="text/javascript" src="f.js"></script>
```

[官网](https://requirejs.org/docs/node.html)

## simple use
### 基本API
require会定义三个变量：define,require,requirejs，其中require === requirejs，一般使用require更简短

- define 从名字就可以看出这个api是用来定义一个模块
- require 加载依赖模块，并执行加载完后的回调函数
