# node.js

## simple

### 代码模块化
编写稍大一点的程序时一般都会将代码模块化。在NodeJS中，一般将代码合理拆分到不同的JS文件中，每一个文件就是一个模块，而文件路径就是模块名。

在编写每个模块时，都有require、exports、module三个预先定义好的变量可供使用。

#### require
require函数用于在当前模块中加载和使用别的模块，传入一个模块名，返回一个模块导出对象。模块名可使用相对路径（以./开头），或者是绝对路径（以/或C:之类的盘符开头）。另外，模块名中的.js扩展名可以省略。
```nashorn js
var foo1 = require('./foo');
var foo2 = require('./foo.js');
var foo3 = require('/home/user/foo');
var foo4 = require('/home/user/foo.js');

// foo1至foo4中保存的是同一个模块的导出对象。
```
另外，可以使用以下方式加载和使用一个JSON文件。
```nashorn js
var data = require('./data.json');
```

#### exports
exports对象是当前模块的导出对象，用于导出模块公有方法和属性。别的模块通过require函数使用当前模块时得到的就是当前模块的exports对象。
```nashorn js
// 以下例子中导出了一个公有方法。
exports.hello = function () {
    console.log('Hello World!');
};
```

#### module
通过module对象可以访问到当前模块的一些相关信息，但最多的用途是替换当前模块的导出对象。

例如模块导出对象默认是一个普通对象，如果想改成一个函数的话，可以使用以下方式。
```nashorn js
module.exports = function () {
    console.log('Hello World!');
};
```

### 二进制模块
虽然一般我们使用JS编写模块，但NodeJS也支持使用C/C++编写二进制模块。编译好的二进制模块除了文件扩展名是.node外，和JS模块的使用方式相同。虽然二进制模块能使用操作系统提供的所有功能，拥有无限的潜能.

### Stream（数据流）
当内存中无法一次装下需要处理的数据时，或者一边读取一边处理更加高效时，我们就需要用到数据流。NodeJS中通过各种Stream来提供对数据流的操作。

以上边的大文件拷贝程序为例，我们可以为数据来源创建一个只读数据流，示例如下：
```nashorn js
var rs = fs.createReadStream(pathname);

rs.on('data', function (chunk) {
    doSomething(chunk);
});

rs.on('end', function () {
    cleanUp();
});
```