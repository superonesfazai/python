# coding=utf-8

from copy import deepcopy

from ..exception import UnimplementedException
from .utils import ConstValue, build_zhihu_obj_from_dict, SimpleEnum


__all__ = ['SearchResult', 'SearchResultSection', 'SearchType']

_search_type_t_map = {
    'GENERAL': 'general',
    'PEOPLE': 'people',
    'TOPIC': 'topic',
    'COLUMN': 'column',
    'LIVE': 'live',
    # 'EBOOK': 'publication',
    # EBOOK 是电子书搜索，目前电子书类还没写，暂时不开放。
}

SearchType = SimpleEnum(_search_type_t_map.keys())
"""
================= ================ ======================
常量名              说明              备注
================= ================ ======================
GENERAL            综合搜索         * 见下备注
PEOPLE             搜索用户
TOPIC              搜索话题
COLUMN             搜索专栏
LIVE               搜索 Live
EBOOK              搜索电子书        现在电子书类还没写，所以此常量暂时不能使用
================= ================ ======================

* 综合搜索是最复杂的一个，但是只有它能搜索到问题和答案。
  一般情况下综合搜索会返回几个除了问题和答案类型之外的 :any:`SearchResultSection`，
  然后返回 Answer，Article，Question 型的 :any:`SearchResult`，具体处理方法看后面文档吧。
"""


def search_type_to_t(search_type):
    return _search_type_t_map[search_type]


class SearchResult(object):
    _TYPE_KEY = ConstValue('type')
    _RESULT_INDICATOR = ConstValue('search_result')
    _RESULT_INDICATOR_TYPO = ConstValue('searach_result')

    _RESULT_HIGHLIGHT_KEY = ConstValue('highlight')
    _RESULT_OBJ_KEY = ConstValue('object')
    _HIGHLIGHT_TITLE_KEY = ConstValue('title')
    _HIGHLIGHT_DESC_KEY = ConstValue('description')

    def __init__(self, data, session):
        if data[self._TYPE_KEY] != self._RESULT_INDICATOR and \
                data[self._TYPE_KEY] != self._RESULT_INDICATOR_TYPO:
            raise ValueError("Must be a {} type dict, {} provided".format(
                self._RESULT_INDICATOR, data
            ))

        self._data = data
        self._session = session
        self._highlight = self._data.get(self._RESULT_HIGHLIGHT_KEY, {})

    @property
    def highlight_title(self):
        """
        标题，其中搜索关键词被高亮，是 HTML 格式的字符串，特殊字符被 escape 了，高亮的部分在 <em> 标签之间。
        print 出来的话不是很好读……
        """
        return self._highlight[self._HIGHLIGHT_TITLE_KEY] \
            if self._HIGHLIGHT_TITLE_KEY in self._highlight \
            else ''

    @property
    def highlight_desc(self):
        """
        description，搜索结果的内容。
        同 :any:`highlight_title`。
        """
        return self._highlight[self._HIGHLIGHT_DESC_KEY] \
            if self._HIGHLIGHT_DESC_KEY in self._highlight \
            else ''

    @property
    def obj(self):
        """
        搜索结果对应的知乎类对象，可能是各种类型，使用前需要自行判断，
        """
        obj = self._data[self._RESULT_OBJ_KEY]
        # 因为搜索结果里的用户属性，比如标题，名字等，都会被 <em> 标签标记成高亮，所以
        # 这里不使用他们当作 cache
        return build_zhihu_obj_from_dict(obj, self._session, use_cache=None)

    def raw_data(self):
        """
        返回搜索结果的原始数据的拷贝，是个 dict。
        """
        return deepcopy(self._data)


class SearchResultSection(object):
    _TYPE_KEY = ConstValue('type')
    _SECTION_INDICATOR = ConstValue('search_section')

    _SECTION_DATA_LIST_KEY = ConstValue('data_list')
    _SECTION_TYPE_KEY = ConstValue('section_type')
    _SECTION_HAS_MORE_KEY = ConstValue('has_more')

    def __init__(self, data, session):
        """
        :any:`SearchResultSection` 对象是可迭代的，`for xxx in results`
        一般会生成 :any:`SearchResult` 型数据。
        """
        if data[self._TYPE_KEY] != self._SECTION_INDICATOR:
            raise ValueError("Must be a {} type dict, {} provided".format(
                self._SECTION_INDICATOR, data
            ))

        self._data = data
        self._session = session

        self._index = 0
        self._len = len(self._data[self._SECTION_DATA_LIST_KEY])

    @property
    def type(self):
        """
        表示这一 Section 里的 :any:`SearchResult` 的知乎类对象是什么类型。
        :rtype: str|unicode
        """
        return self._data[self._SECTION_TYPE_KEY]

    @property
    def has_more(self):
        """
        如果用 type 类型进行搜索，能否得到更多结果。

        比如：::

            self.type == "people", self. has_more == True

        那么表示：::

            client.search('something', SearchType.PEOPLE)

        能获取到此 Section 的更多结果。

        :rtype: bool
        """
        return self._data[self._SECTION_HAS_MORE_KEY]

    def raw_data(self):
        """
        同 :any:`SearchResult.raw_data`
        """
        return deepcopy(self._data)

    def __iter__(self):
        self._index = 0
        return self

    def __len__(self):
        return self._len

    def __next__(self):
        try:
            obj = self[self._index]
        except IndexError:
            self._index = 0
            raise StopIteration
        self._index += 1
        return obj

    next = __next__

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Need an int as index, not {0}'.format(type(item)))

        if item >= self._len:
            raise IndexError()

        data = self._data[self._SECTION_DATA_LIST_KEY][item]
        return data_to_section_or_result(data, self._session)


def data_to_section_or_result(data, session):
    try:
        return SearchResult(data, session)
    except ValueError:
        pass

    try:
        return SearchResultSection(data, session)
    except ValueError:
        raise UnimplementedException(
            "Unknown search result dict [{}]".format(data))
