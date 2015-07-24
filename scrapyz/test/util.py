import os

from scrapy.http import HtmlResponse, Request


def fake_response(file, url=None):
    if not url:
        url = "http://www.test.com/offers"
    file = os.path.join(os.path.dirname(__file__), file)
    return HtmlResponse(url=url, request=Request(url=url), body=open(file, 'r').read())