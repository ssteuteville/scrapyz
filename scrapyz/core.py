from scrapy.loader.processors import TakeFirst
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapyz.util import gen_item, gen_request


class GenericSpider(Spider):

    def __init__(self, name=None, **kwargs):
        if not hasattr(self, "Meta"):
            raise AttributeError("GenericSpider must implement a Meta inner class.")
        if not hasattr(self, "start_urls"):
            raise AttributeError("Generic spider must implement start_urls.")

        super(GenericSpider, self).__init__(name, **kwargs)
        self.item_class = self.get_item_class()
        self._items = None

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.get_parse())

    def parse(self, response):
        for item in self.find_items(response):
            loader = ItemLoader(item=self.item_class())
            for target in self.get_targets():
                loader.add_value(target.name, target.get_value(item, response))
            yield loader.load_item()

    def find_items(self, response):
        if not self._items:
            self._items = Selector(response).css(self.Meta.items)
        return self._items

    def get_targets(self):
        return self.Meta.targets

    def get_parse(self):
        return self.parse

    def get_item_class(self):
        return gen_item(self.gen_fields())

    def gen_fields(self):
        fields = {target.name: target.field_class(output_processor=TakeFirst()) for target in self.get_targets()}
        if hasattr(self.Meta, "extra_fields"):
            fields.update(self.Meta.extra_fields)
        return fields



class IndexDetailSpider(GenericSpider):

    def __init__(self, name=None, **kwargs):
        super(IndexDetailSpider, self).__init__(name, **kwargs)

        if not hasattr(self.Meta, "detail_path"):
            raise AttributeError("IndexDetailSpider's Meta class must implement detail_path")
        if not hasattr(self.Meta, "detail_targets"):
            raise AttributeError("IndexDetailSpider's Meta class must implement detail_targets")

    def parse(self, response):
        for item in self.find_items(response):
            loader = ItemLoader(item=self.item_class())
            for target in self.get_targets():
                loader.add_value(target.name, target.get_value(item, response))

            val = self.Meta.detail_path.get_value(item, response)
            yield gen_request(val, self.parse_details, loader.load_item())

    def parse_details(self, response):
        dom = Selector(response)
        loader = ItemLoader(item=response.meta['item'])
        for target in self.Meta.detail_targets:
            loader.add_value(target.name, target.get_value(dom, response))
        yield loader.load_item()

    def gen_fields(self):
        fields = super(IndexDetailSpider, self).gen_fields()
        fields.update({target.name: target.field_class(output_processor=TakeFirst()) for target in self.Meta.detail_targets})
        return fields


class Target(object):

    def __init__(self, name, path, processors=None, field_class=Field):
        self.name = name
        self.path = path
        self.processors = processors if processors else []
        self.field_class = field_class

    def get_value(self, selector, response):
        if isinstance(self.path, (list, tuple)):
            return self.process(" ".join(selector.css(_).extract() for _ in self.path), response)
        return self.process(self.select(selector), response)

    def process(self, value, response):
        for processor in self.processors:
            value = processor(value, response)
        return value

    def select(self, selector):
        raise NotImplementedError("Target is meant as a base class. Use CssTarget, RegexTarget,"
                                  " or XPathTarget instead.")


class RegexTarget(Target):

    def select(self, selector):
        return selector.re(self.path)


class XPathTarget(Target):

    def select(self, selector):
        return selector.xpath(self.path).extract()


class CssTarget(Target):

    def select(self, selector):
        return selector.css(self.path).extract()
