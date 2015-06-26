from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader


class GenericSpider(Spider):

    def __init__(self, name=None, **kwargs):
        super(GenericSpider, self).__init__(name, **kwargs)
        self.item_class = self.gen_item_class()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.get_parse())

    def parse(self, response):
        for element in self.get_elements(response):
            loader = ItemLoader(item=self.item_class())
            for target in self.get_targets():
                loader.add_value(target.name, target.get_value(element, response))
            yield loader.load_item()

    def get_elements(self, response):
        return Selector(response).css(self.Meta.elements)

    def get_targets(self):
        return self.Meta.targets

    def get_parse(self):
        return self.parse

    def gen_item_class(self):
        fields = {target.name: Field() for target in self.get_targets()}
        return type("GenericItem", (Item,), fields)


class Target(object):

    def __init__(self, name, path, processors=None):
        self.name = name
        self.path = path
        self.processors = processors if processors else []

    def get_value(self, selector, response):
        if isinstance(self.path, (list, tuple)):
            return self.process(" ".join(selector.css(_).extract() for _ in self.path), response)
        return self.process(self.select(selector), response)

    def process(self, value, response):
        for processor in self.processors:
            value = processor(value, response)
        return value

    def select(self, selector):
        return selector.css(self.path).extract()


class RegexTarget(Target):

    def select(self, selector):
        return selector.re(self.path)


class XPathTarget(Target):

    def select(self, selector):
        return selector.xpath(self.path).extract()