#coding: utf-8
import htmlentitydefs
from sgmllib import SGMLParser

class BaseHTMLParser(SGMLParser):
    def reset(self):        #reset 由 SGMLParser.__init__ 来调用
        self.pieces = []    #在调用父类方法之前将 self.pieces 初始化为空列表
                            #self.pieces 是一个数据属性,将用来保存将要构造的 HTML 文档的片段
                            #每个处理器方法都将重构 SGMLParser 所分析出来的 HTML,并且每个方法将生成的字符串追加到 self.pieces 之后
                            #self.pieces 是一个 list
        SGMLParser.reset(self)

    def unknown_starttag(self, tag, attrs):     #SGMLParser 将对每一个开始标记调用 unknown_starttag 方法。这个方法接收标记 ( tag ) 和属性的名字/值对的 list( attrs ) 两参数,重新构造初始的HTML,接着将结果追加到 self.pieces 后
        strattrs = ''.join(['%s="%s"' % (key, value) for key, value in attrs])
        self.pieces.append('<%(tag)s%(strattrs)s>' % locals())

    def unknown_endtag(self, tag):      #重构结束标记要简单得多,只是使用标记名字,把它包在 </...> 括号中
        self.pieces.append('</%(tag)s>' % locals())

    def handle_charref(self, ref):      #当 SGMLParser 找到一个字符引用时,会用原始的引用来调用
                                        #handle_charref 。如果
                                        #HTML 文档包含 &#160; 这个引用, ref 将为 160 。重构
                                        #原始的完整的字符引用只要将 ref 包装在 &#...; 字符中间
        self.pieces.append('&#%(ref)s;' % locals())

    def handle_entityref(self, ref):        #实体引用同字符引用相似,但是没有#号。重建原始的实体引用只要将 ref包装在 &...; 字符串中间。(实际上,一位博学的读者曾经向我指出,除些之外还稍微有些复杂。仅有某种标准的 HTML 实体以一个分号结束;其它看上去差不多的实体并不如此。幸运的是,标准 HTML 实体集已经定义在Python 的一个叫做 htmlentitydefs 的模块中了。从而引出额外的 if 语句。)
        self.pieces.append("&%(ref)s" % locals())
        if htmlentitydefs.entitydefs.has_key(ref):
            self.pieces.append(";")

    def handle_data(self, text):        #文本块则简单地不经修改地追加到 self.pieces 后
        self.pieces.append(text)

    def handle_comment(self, text):     #HTML 注释包装在 <!--...--> 字符中
        self.pieces.append("<!--%(text)s-->" % locals())

    def handle_pi(self, text):          #处理指令包装在 <?...> 字符中
        self.pieces.append("<?%(text)s>" % locals())

    def handle_decl(self, text):
        self.pieces.append("<!%(text)s>" % locals())

    #BaseHTMLProcessor 输出结果
    def output(self):
        """Return processed HTML as a single string"""
        return "".join(self.pieces)

# if __name__ == '__main__':
#     for k ,v in globals().items():
#         print(k, ' = ', v)

'''
这是在 BaseHTMLProcessor 中的一个方法,它永远不会被父类 SGMLParser 所
调用。因为其它的处理器方法将它们重构的 HTML 保存在 self.pieces 中,
这个函数需要将所有这些片段连接成一个字符串。正如前面提到的,
Python 在处理列表方面非常出色,但对于字符串处理就逊色了。所以我们
只有在某人确实需要它时才创建完整的字符串
'''

'''
Important: 包含植 入脚本的 HTML 处理
HTML 规范要求所有非 HTML (像客户端的 JavaScript) 必须包括在 HTML 注释
中,但不是所有的页面都是这么做的 (而且所有的最新的浏览器也都容许不这
样做) 。 BaseHTMLProcessor 不允许这样,如果脚本嵌入得不正确,它将被当作
HTML 一样进行分析。例如,如果脚本包含了小于和等于号, SGMLParser 可能
会错误地认为找到了标记和属性。 SGMLParser 总是把标记名和属性名转换成小
写,这样可能破坏了脚本,并且 BaseHTMLProcessor 总是用双引号来将属性封闭
起来 (尽管原始的 HTML 文档可能使用单引号或没有引号) ,这样必然会破坏
脚本。应该总是将您的客户端脚本放在 HTML 注释中进行保护
'''