# coding=utf-8

from __future__ import unicode_literals

import datetime
import warnings

import requests.packages.urllib3 as urllib3

from .zhcls.activity import Activity, ActType
from .zhcls.generator import BaseGenerator, ActivityGenerator
from .zhcls.streaming import StreamingJSON
from .zhcls.utils import SimpleEnum
from .exception import ZhihuException, ZhihuWarning


__all__ = ['ActivityFormatter', 'SHIELD_ACTION', 'act2str', 'shield', 'ts2str']

SHIELD_ACTION = SimpleEnum(
    ['EXCEPTION', 'PASS', 'STOP']
)
"""
ActType 是用于表示 shield 抵挡 Exception 达到最大次数后的动作的枚举类，取值如下：

================= ====================
常量名              说明
================= ====================
EXCEPTION          抛出异常
PASS               跳过，获取下一个数据
STOP               结束处理
================= ====================
"""


def shield(inner, durability=3, start_at=0, action=SHIELD_ACTION.EXCEPTION):
    """
    shield 函数用于自动处理知乎的各种生成器
    （如 :any:`People.followers`, :any:`Question.answers`） 在获取分页数据时出错的情况。

    ..  warning:: 用户动态的生成器因为获取方式比较特殊，无法被 shield 保护

    用法：

    比如我们想获取关注了某个专栏的用户分别关注了哪些话题……

    ..  code-block:: python

        column = client.column('zijingnotes')
        result = []
        for user in shield(column.followers, action=SHIELD_ACTION.PASS):
            L = []
            print('Start proc user', user.name)
            if user.over:
                print(user.over_reason)
                continue
            for topic in shield(user.following_topics):
                print('Add topic', topic.name)
                L.append(topic.name)
            result.append(L)

        # output result

    :param inner: 需要被保护的生成器
    :param int durability: 耐久度，表示获取同一数据最多连续出错几次
    :param int start_at: 从第几个数据开始获取
    :param action: 当耐久度消耗完后的动作，参见 :any:`SHIELD_ACTION`，默认动作是抛出异常
    :return: 新的生成器……
    """
    if not isinstance(inner, BaseGenerator):
        raise ValueError('First argument must be Zhihu Generator Classes')
    if isinstance(inner, ActivityGenerator):
        raise ValueError('Activity Generator is the only one can\'t be shield')
    offset = start_at
    hp = durability
    while True:
        i = -1
        try:
            for i, x in enumerate(inner.jump(offset)):
                yield x
                hp = durability
            break
        except (ZhihuException, urllib3.exceptions.MaxRetryError) as e:
            offset += i + 1
            hp -= 1
            warnings.warn(
                '[{type}: {e}] be shield when get NO.{offset} data'.format(
                    type=e.__class__.__name__,
                    e=e,
                    offset=offset
                ),
                ZhihuWarning
            )
            if hp == 0:
                if action is SHIELD_ACTION.EXCEPTION:
                    raise e
                elif action is SHIELD_ACTION.PASS:
                    offset += 1
                    hp = durability
                elif action is SHIELD_ACTION.STOP:
                    break
                else:
                    raise e


def ts2str(ts, fmt=None, offset=8):
    """
    将时间戳转换为表示时间的字符串。

    :param int ts: 精确到秒的 unix timestamp
    :param fmt: 格式化文本，默认值 ``%Y-%m-%d %H:%M:%S``
    :param offset: 当前时区偏移，单位小时，默认为 8 小时
    :return: 时间戳转换为时间的字符串表示
    :rtype: str
    """
    offset *= 3600    # 时区偏移
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.utcfromtimestamp(ts + offset).strftime(fmt)


_DEFAULT_ACTIVITY_FORMATTER_MANY_ONE = [
    ({
        ActType.CREATE_ARTICLE, ActType.CREATE_QUESTION,
        ActType.FOLLOW_COLLECTION, ActType.FOLLOW_COLUMN,
        ActType.FOLLOW_QUESTION, ActType.JOIN_LIVE, ActType.PUBLISH_LIVE,
        ActType.VOTEUP_ARTICLE, ActType.VOTEUP_EBOOK
    }, '{act.action_text} 「{act.target.title}」'),
    ({
        ActType.FOLLOW_ROUNDTABLE,
        ActType.FOLLOW_TOPIC
    }, '{act.action_text} 「{act.target.name}」'),
]

_DEFAULT_ACTIVITY_FORMATTER_ONE_ONE = {
    ActType.CREATE_ANSWER: '{act.action_text} 「{act.target.question.title}」',
    ActType.VOTEUP_ANSWER: '{act.action_text} 「{act.target.question.title}」'
                           ' by 「{act.target.author.name}」',
    ActType.CREATE_PIN: '{act.action_text} {act.target.excerpt_title}',
    ActType.LIKE_PIN: '{act.action_text} {act.target.excerpt_title}'
                      ' by 「{act.target.author.name}」',
    ActType.COLLECT_ANSWER: '{act.action_text} '
                            '「{act.target[answer].question.title}」'
                            ' by 「{act.target[answer].author.name}」'
                            ' 到收藏夹 「{act.target[collection].title}」',
    ActType.COLLECT_ARTICLE: '{act.action_text} 「{act.target[article].title}」'
                             ' 到收藏夹 「{act.target[collection].title}」'
}


class ActivityFormatter(object):
    """
    这是将 Activity 转换为字符串的辅助类，一般情况下不需要使用，直接使用辅助函数
    :any:`act2str` 即可。

    如果你需要自定义格式化模板，请参考下面的用法：

    ..  code-block:: python

        class MyActivityFormatter(ActivityFormatter):
            def __init__(self, user_name):
                self._user_name = user_name

            def like_pin_formatter(self, act):
                content_summary = next(act.target.contents).content[:20]
                return '{i} 赞了 {act.target.author.name} 的分享： {content}'.format(
                    i=self._user_name, act=act, content=content_summary,
                )

            create_pin_formatter = '{act.action_text} 一些东西'

        guxizhao = client.people('guxizhao')

        formatter = MyActivityFormatter(guxizhao.name)

        for act in guxizhao.activities:
            print(ts2str(act.created_time), formatter(act))


    ..  note:: 执行结果

        除了发表分享和对分享点赞这两个类型的 Activity 之外，其他类型的格式化结果均和
        :any:`act2str` 函数一致。

        ActType.LIKE_PIN 类型的会被转换成 ``xxx 赞同了 yyy 的分享：<分享内容的前20字>``

        ActType.CREATE_PIN 类型的会被转换成 ``xxx 分享了 一些东西``

    简单来说就是你可以继承 :any:`ActivityFormatter` 类，然后定义一些函数或者常量，名称是
    ActType 类型的小写形式 + ``_formatter``。

    如果它是个函数，需要接受一个 :any:`ActType` 或者 :any:`StreamingJSON` 对象，
    返回一个字符串模板。如果直接是个变量那就直接被当成模板使用。

    模板里一律用 ``act`` 代表 :any:`Activity` 对象。
    """
    @staticmethod
    def __check_type(act):
        return isinstance(act, Activity) \
               or (
                   isinstance(act, StreamingJSON) and
                   hasattr(act, 'type') and
                   act.type in ActType
               )

    def __call__(self, act):
        if not self.__check_type(act):
            raise ValueError('Only support Activity objects.')

        attr_name = act.type.lower() + '_formatter'

        if hasattr(self, attr_name):
            fmt = getattr(self, attr_name)
            if hasattr(fmt, '__call__'):
                fmt = fmt(act)
            assert isinstance(fmt, str), \
                'Formatter must be a str of a function like ' \
                'func(act: Activity) -> str'
        elif act.type in _DEFAULT_ACTIVITY_FORMATTER_ONE_ONE:
            fmt = _DEFAULT_ACTIVITY_FORMATTER_ONE_ONE[act.type]
        else:
            found = False
            for ks, v in _DEFAULT_ACTIVITY_FORMATTER_MANY_ONE:
                if act.type in ks:
                    found = True
                    fmt = v
            assert found, 'Unknown ActType ' + act.type

        # noinspection PyUnboundLocalVariable
        return fmt.format(act=act)

act2str = ActivityFormatter()
"""
一个将 ``xxx.activities`` 返回的 :any:`Activity` 或 :any:`StreamingJSON`
对象转换为可读的字符串的辅助函数。例子：

..  code-block:: python

    guxizhao = client.people('guxizhao')

    for act in guxizhao.activities:
        print(ts2str(act.created_time), act2str(act))

..  note:: 结果

    2016-12-08 01:18:20 顾惜朝关注了问题
    「如何评价美剧《西部世界》（Westworld）第一季第十集（S01E10）?」

    2016-12-07 23:18:02 顾惜朝赞同了回答
    「如何看待民生银行性骚扰事件？」 by 「meta」

    2016-12-07 13:20:32 顾惜朝赞了文章
    「冒牌高校教授，正版绝命毒师」

    2016-12-07 10:59:43 顾惜朝赞同了回答
    「你最喜欢的故事是什么？」 by 「胡不归」

    2016-12-07 01:30:51 顾惜朝赞了文章
    「专访 | 关于《西部世界》季终集，死过一千次的泰迪这样说」

    2016-12-06 20:23:59 顾惜朝赞同了回答
    「如何看待知乎上「一知半解」也要强行回答的回答者？」 by 「河森堡」

    2016-12-06 01:57:30 顾惜朝关注了收藏夹 「你丫竟然在图片里下毒？！！」
    2016-12-05 22:23:25 顾惜朝赞同了回答
    「《你的名字。》中彗星碎片撞击地面的影响是否合理？」 by 「Macro kuo」

    2016-12-04 00:36:24 顾惜朝赞了文章 「Google Earth: 这才是真·情怀」

如果想自定义描述模板，请参见 :any:`ActivityFormatter` 类。
"""
