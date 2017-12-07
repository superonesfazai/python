# coding=utf-8

from __future__ import unicode_literals

import importlib
import functools
import os

from .urls import RE_TYPE_MAP
from ..exception import (
    MyJSONDecodeError,
    UnexpectedResponseException,
    UnimplementedException,
)

try:
    # Py3
    # noinspection PyCompatibility
    from html.parser import HTMLParser
except ImportError:
    # Py2
    # noinspection PyCompatibility,PyUnresolvedReferences
    from HTMLParser import HTMLParser

__all__ = [
    'zhihu_obj_url_parse',
    'DEFAULT_INVALID_CHARS', 'EXTRA_CHAR_FOR_FILENAME',
    'remove_invalid_char', 'add_serial_number',
    'SimpleHtmlFormatter',
    'SimpleEnum', 'ConstValue', 'OneValueCache',
]


def get_class_from_name(name, module_filename=None):
    cls_name = name.capitalize()
    file_name = module_filename or cls_name.lower()
    try:
        module = importlib.import_module(
            '.' + file_name,
            'zhihu_oauth.zhcls'
        )
        return getattr(module, cls_name)
    except (ImportError, AttributeError):
        raise UnimplementedException(
            'Unknown zhihu obj type [{}]'.format(name)
        )


def build_zhihu_obj_from_dict(data, session, use_cache=True):
    cls = get_class_from_name(data['type'])
    return cls(data['id'], data if use_cache else None, session)


def zhihu_obj_url_parse(url):
    for pattern, val in RE_TYPE_MAP.items():
        match = pattern.match(url)
        if match:
            return match.group(1), val[0], val[1]
    return None, None, None


def can_get_from(name, data):
    return name in data and not isinstance(data[name], (dict, list))

DEFAULT_INVALID_CHARS = {':', '*', '?', '"', '<', '>', '|', '\r', '\n'}
EXTRA_CHAR_FOR_FILENAME = {'/', '\\'}


def remove_invalid_char(dirty, invalid_chars=None, for_path=False):
    if invalid_chars is None:
        invalid_chars = set(DEFAULT_INVALID_CHARS)
    else:
        invalid_chars = set(invalid_chars)
        invalid_chars.update(DEFAULT_INVALID_CHARS)
    if not for_path:
        invalid_chars.update(EXTRA_CHAR_FOR_FILENAME)

    return ''.join([c for c in dirty if c not in invalid_chars]).strip()


def add_serial_number(file_path, postfix):
    full_path = file_path + postfix
    if not os.path.isfile(full_path):
        return full_path
    num = 1
    while os.path.isfile(full_path):
        # noinspection PyUnboundLocalVariable
        try:
            # noinspection PyCompatibility,PyUnresolvedReferences
            serial = unicode(str(num))
        except NameError:
            serial = str(num)
        full_path = file_path + ' - ' + serial.rjust(3, '0') + '.' + postfix
        num += 1
    return full_path


_BASE_HTML_HEADER = """<meta name="referrer" content="no-referrer" />
<meta charset="utf-8" />
"""


class SimpleHtmlFormatter(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._level = 0
        self._last = ''
        self._in_code = False
        self._prettified = [_BASE_HTML_HEADER]

    def handle_starttag(self, tag, attrs):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('<' + tag)
        for name, value in attrs:
            self._prettified.append(' ' + name + '="' + value + '"')
        self._prettified.append('>')
        if not self._in_code:
            self._prettified.append('\n')
        if tag != 'br' and tag != 'img':
            self._level += 1
        if tag == 'code':
            self._in_code = True
        self._last = tag

    def handle_endtag(self, tag):
        if tag != 'br' and tag != 'img':
            self._level -= 1
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('</' + tag + '>')
        if not self._in_code:
            self._prettified.append('\n')
        self._last = tag
        if tag == 'code':
            self._in_code = False

    def handle_startendtag(self, tag, attrs):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
        self._prettified.append('<' + tag)
        for name, value in attrs:
            self._prettified.append(' ' + name + '="' + value + '"')
        self._prettified.append('/>')
        self._last = tag

    def handle_data(self, data):
        if not self._in_code:
            self._prettified.extend(['\t'] * self._level)
            if self._last == 'img':
                self._prettified.append('<br>\n')
                self._prettified.extend(['\t'] * self._level)
        self._prettified.append(data)
        if not self._in_code:
            self._prettified.append('\n')

    def handle_charref(self, name):
        self._prettified.append('&#' + name)

    def handle_entityref(self, name):
        self._prettified.append('&' + name + ';')

    def error(self, message):
        self._prettified = ['error when parser the html file.']

    def prettify(self):
        return ''.join(self._prettified)


class SimpleEnum(set):
    def __getattr__(self, item):
        if item in self:
            return item
        raise AttributeError('No {0} in this enum class.'.format(item))


class ConstValue(object):
    def __init__(self, value=None):
        self._value = value

    def __get__(self, instance, cls):
        return self._value

    def __set__(self, instance, value):
        raise TypeError('Can\'t change value of a const var')


def get_result_or_error(url, res):
    try:
        json_dict = res.json()
        if 'error' in json_dict:
            return False, json_dict['error']['message']
        elif 'success' in json_dict:
            if json_dict['success']:
                return True, ''
            else:
                return False, 'Unknown error'
        else:
            return True, ''
    except (KeyError, MyJSONDecodeError):
        raise UnexpectedResponseException(
            url, res, 'a json contains voting result or error message')


def common_save(path, filename, content, default_filename, invalid_chars):
    filename = filename or default_filename
    filename = remove_invalid_char(filename, invalid_chars)
    filename = filename or 'untitled'

    path = path or '.'
    path = remove_invalid_char(path, invalid_chars, True)
    path = path or '.'

    if not os.path.isdir(path):
        os.makedirs(path)
    full_path = os.path.join(path, filename)
    full_path = add_serial_number(full_path, '.html')
    formatter = SimpleHtmlFormatter()
    formatter.feed(content)
    with open(full_path, 'wb') as f:
        f.write(formatter.prettify().encode('utf-8'))


class OneValueCache(object):
    def __init__(self, func):
        self._func = func
        self._values = {}

    def __get__(self, instance, owner):
        return functools.partial(self, instance)

    @staticmethod
    def gen_key(obj):
        return '/'.join([str(obj.id), str(hash(obj))])

    def __call__(self, obj, *args, **kwargs):
        key = self.gen_key(obj)
        if key not in self._values:
            self._values[key] = self._func(obj, *args, **kwargs)
            self._has_value = True
        return self._values[key]
