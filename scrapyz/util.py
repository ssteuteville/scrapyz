from scrapy import Item
from scrapy.http.request import Request
from scrapy.utils.response import get_base_url
import urlparse


def gen_item(fields):
    return type("GenericItem", (Item,), fields)


def gen_request(url, callback, item=None):
    r = Request(url, callback=callback)
    if item:
        r.meta['item'] = item
    return r


def absolute_url(link, response):
    if isinstance(link, list):
        link = link[0] if len(link) else ""
    return urlparse.urljoin(get_base_url(response), link)


def nth(n):
    def processor(field, response):
        return field[n]
    return processor


def strip(field, response):
    if isinstance(field, list) and field:
        field = field[0]
    return field.strip()


class JsonSelector(dict):

    def __init__(self, **kwargs):
        super(JsonSelector, self).__init__()
        data = kwargs.get("data", False)
        self.data = data if data else dict()

    def __getitem__(self, item):
        _ = self.data
        exprs = item.split('.')
        for expr in exprs:
            if "[" in expr:
                parts = expr.split("[")
                _ = _[parts[0]][int(parts[1].strip("]"))]
            else:
                _ = _[expr]
        return _

    def __setitem__(self, key, value):
        self.data[key] = value