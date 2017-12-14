# coding=utf-8

from .client import ZhihuClient
from .exception import (
    ZhihuWarning, IgnoreErrorDataWarning, CantGetTicketsWarning,
    ZhihuException, UnexpectedResponseException, GetDataErrorException,
    NeedCaptchaException, NeedLoginException, IdMustBeIntException,
    UnimplementedException,
)
from .helpers import act2str, ActivityFormatter, shield, SHIELD_ACTION, ts2str
from .zhcls import (
    Activity, ActType, Answer, ANONYMOUS, Article, Badge, Comment, Collection,
    Column, Comment, Live, LiveBadge, LiveTag, LiveTicket, Me, Message, People,
    Pin, PinContent, PCType, Question, SearchResult, SearchResultSection,
    SearchType, Topic, Whisper,
)

__all__ = [
    'Activity', 'ActType', 'Answer', 'ANONYMOUS', 'Article',
    'Collection', 'Column', 'Comment', 'Live', 'LiveBadge', 'LiveTag',
    'LiveTicket', 'Me', 'Message', 'People', 'Question', 'SearchResult',
    'SearchResultSection', 'SearchType', 'Topic', 'Whisper', 'ZhihuClient',
    'ZhihuException', 'ZhihuWarning',
    'NeedCaptchaException', 'UnexpectedResponseException',
    'GetDataErrorException',
    'act2str', 'shield', 'ts2str', 'ActivityFormatter', 'SHIELD_ACTION'
]

__version__ = '0.0.36'

# TODO: remove all magic number and magic string
