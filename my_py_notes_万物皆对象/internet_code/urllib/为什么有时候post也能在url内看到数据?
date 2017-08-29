```html
* GET方式是直接以链接形式访问，链接中
  包含了所有的参数，服务器端用Request.QueryString获取变量的值。
  如果包含了密码的话是一种不安全的选择，
  不过你可以直观地看到自己提交了什么内容。

* POST则不会在网址上显示所有的参数，
  服务器端用Request.Form获取提交的数据，
  在Form提交的时候。但是HTML代码里如果不指定 method 属性，
  则默认为GET请求，Form中提交的数据将会附加在url之后，
  以?分开与url分开。

* 表单数据可以作为 URL 字段（method="get"）
  或者 HTTP POST （method="post"）的方式来发送。
  比如在下面的HTML代码中，表单数据将因为 （method="get"） 而附加到 URL 上：
```