# coding=utf-8

from __future__ import unicode_literals

import itertools

from .base import Base
from .generator import generator_of
from .normal import normal_attr
from .other import other_obj
from .streaming import streaming, StreamingJSON
from .urls import (
    PIN_COMMENTS_URL,
    PIN_DETAIL_URL,
    PIN_VOTERS_URL,
    ZHIHU_WEB_ROOT,
)
from .utils import (
    get_class_from_name,
    zhihu_obj_url_parse,
    SimpleEnum,
)

from ..exception import UnimplementedException

__all__ = ['Pin', 'PinContent', 'PCType']


class Pin(Base):

    def __init__(self, pid, cache, session):
        super(Pin, self).__init__(pid, cache, session)

    def _build_url(self):
        return PIN_DETAIL_URL.format(self.id)

    # ----- simple attrs -----

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def comment_count(self):
        return None

    @property
    @normal_attr()
    def comment_permission(self):
        return None

    @property
    @normal_attr('created')
    def created_time(self):
        return None

    @property
    @normal_attr()
    def excerpt_title(self):
        """
        简要标题文字
        """
        return None

    @property
    @normal_attr()
    def like_count(self):
        return None

    @property
    @normal_attr('updated')
    def updated_time(self):
        return None

    @property
    @streaming('content')
    def _contents(self):
        return []

    @property
    def contents(self):
        """
        因为一个分享里含有多个内容，所以 contents 属性是迭代器，需要这样使用：

        ..  code-block:: Python

            for act in someone.activities.filter(ActType.LINK_PIN):
                pin = act.target
                for pc in pin.contents:
                    # do something with pc

        迭代器返回 :any:`PinContent` 类型的对象，具体用法参看
        :any:`_pin_content_type_map` 和 any:`PinContent`。
        """
        for data in self._contents:
            yield PinContent(data, self._session)

    @property
    @normal_attr()
    def content_html(self):
        return None

    # ----- generators -----

    @property
    @generator_of(PIN_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(PIN_VOTERS_URL, 'people')
    def voters(self):
        return None


_pin_content_type_map = {
    'text': 'TEXT',
    'image': 'IMAGE',
    'link': 'LINK',
    'quote': 'QUOTE',
}
"""
:any:`PinContent` 的类型，每种类型能够使用的属性都不一样，具体请看下表：

+--------+---------------+------------------------------------+
|  类型  |      属性     |               含义                 |
+========+===============+====================================+
| TEXT   |      text     | 用户对分享的评论文字               |
+--------+---------------+------------------------------------+
|        |      src      | 图片地址                           |
| IMAGE  +---------------+------------------------------------+
|        | width, height | 图片宽高                           |
+--------+---------------+------------------------------------+
|        |     title     | 网页的标题                         |
|        +---------------+------------------------------------+
|  LINK  |      url      | 网页地址                           |
|        +---------------+------------------------------------+
|        |   image_url   | 网页的 ICON 地址                   |
+--------+---------------+------------------------------------+
|  QUOTE |     quote     | 引用的文字                         |
+--------+---------------+------------------------------------+
|        |     type      | 类型，可用 is PcType.TEXT 判断     |
|        +---------------+------------------------------------+
|        |    subtype    | 表示内容中包含的知乎对象类型，     |
|        |               | 参见 :any:`_subtype_zhihu_obj_map` |
|  通用  +---------------+------------------------------------+
|        |       obj     | 分享内容是知乎相关链接的话         |
|        |               | 可使用此属性获取到对应知乎类对象   |
|        +---------------+------------------------------------+
|        |               | 获取主要的数据                     |
|        |     content   | TEXT -> text, LINK -> url          |
|        |               | IMAGE -> src, QUOTE -> quote       |
+--------+---------------+------------------------------------+
"""

_subtype_zhihu_obj_map = {
    '问题': 'QUESTION',
    '回答': 'ANSWER',
    '专栏': 'COLUMN',
    '文章': 'ARTICLE',
    '收藏夹': 'COLLECTION',
    '话题': 'TOPIC',
    '个人主页': 'PEOPLE',
    'Live': 'LIVE',
    # ----- no zhihu object -----
    'none': 'NONE',
}
"""
:any:`PinContent.obj_type` 的取值枚举。

使用方法大概如下：

..  code-block:: Python

    for act in someone.activities.filter(ActType.LIKE_PIN):
        pin = act.target
        for content in pin.contents:
            if content.obj_type not is PCType.NONE:
                print(content.obj)
"""

_type_zhihu = 'zhihu'

PCType = SimpleEnum(
    itertools.chain(
        _pin_content_type_map.values(),
        _subtype_zhihu_obj_map.values(),
    )
)
"""
参见 :any:`_pin_content_type_map` 和 :any:`_subtype_zhihu_obj_map`。
"""

_type_content_method_map = {
    PCType.TEXT: 'text',
    PCType.IMAGE: 'src',
    PCType.QUOTE: 'quote',
    PCType.LINK: 'url'
}
"""
从 :any:`PinContent` 的类型对应到 :any:`PinContent.content` 属性需要使用的方法名
"""


class PinContent(object):
    """
    PinContent 是表示分享的内容的类，因为其类型很多，所以单独成类，设计理念和
    :any:`Activity` 类似。

    每一个 :any:`Pin` 可能含有多个 :any:`PinContent`，
    一般第一个是用户自对自己分享的东西的评论，余下的是 TA 分享的东西。

    :any:`PinContent` 主要有四个类型，具体请看 :any:`_pin_content_type_map`。

    使用方法如下：

    ..  code-block:: Python

        for act in me.activities.filter(ActType.LIKE_PIN):
            for content in act.target.contents:
                print(content.type, content.obj_type, end=' ')
                if content.type is PCType.TEXT:
                    print(content.text)
                elif content.type is PCType.QUOTE:
                    print(content.quote)
                elif content.type is PCType.LINK:
                    print(content.title, content.url, content.image_url)
                elif content.type is PCType.IMAGE:
                    print(content.src, content.width, content.height)
            print('-' * 20)

    或者使用 :any:`PinContent.content` 获取对于每种类型的主要内容。
    参见 :any:`_type_content_method_map`
    """
    def __init__(self, data, session):
        assert isinstance(data, StreamingJSON)
        self._data = data
        self._session = session

    # ----- Text type ----

    @property
    def text(self):
        assert self.type is PCType.TEXT
        return self._data.content

    # ----- Image type -----

    @property
    def src(self):
        assert self.type is PCType.IMAGE
        return self._data.url

    @property
    def width(self):
        assert self.type is PCType.IMAGE
        return self._data.width

    @property
    def height(self):
        assert self.type is PCType.IMAGE
        return self._data.height

    # ----- Normal link type -----

    @property
    def title(self):
        assert self.type is PCType.LINK
        return self._data.title

    @property
    def url(self):
        assert self.type is PCType.LINK or self.type is PCType.QUOTE
        return self._data.url

    @property
    def image_url(self):
        assert self.type is PCType.LINK
        return self._data.image_url

    # ----- Quote -----

    @property
    def quote(self):
        assert self.type is PCType.QUOTE
        return self._data.content

    # ------ Common -----

    @property
    def type(self):
        if self._data.type not in _pin_content_type_map:
            raise UnimplementedException(
                'Unknown pin content type [{}]'.format(self._data.type)
            )

        return getattr(PCType, _pin_content_type_map[self._data.type])

    @property
    def obj_type(self):
        if self.type is PCType.LINK and self._data.link_type == _type_zhihu:
            subtype = self._data.subtype
            if subtype not in _subtype_zhihu_obj_map:
                raise UnimplementedException(
                    'Unknown pin link obj_type [{}]'.format(subtype)
                )
            return getattr(PCType, _subtype_zhihu_obj_map[subtype])

        if self.type is PCType.QUOTE:
            obj_id, obj_type, _ = zhihu_obj_url_parse(self._data.url)
            if obj_id:
                return getattr(PCType, obj_type.upper())
            elif self._data.url.startswith(ZHIHU_WEB_ROOT):
                raise UnimplementedException(
                    'Unknown pin quote obj_type, data [{}]'.format
                    (self._data)
                )

        return PCType.NONE

    @property
    def content(self):
        return getattr(self, _type_content_method_map[self.type])

    @property
    def obj(self):
        assert self.obj_type is not PCType.NONE

        if self.type is PCType.LINK:
            obj_id = self._data.token
        else:
            assert self.type is PCType.QUOTE
            obj_id, _, _ = zhihu_obj_url_parse(self.url)

        cls = get_class_from_name(self.obj_type)
        return cls(obj_id, None, self._session)
