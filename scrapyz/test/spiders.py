from scrapyz.core import GenericSpider, CssTarget
from scrapyz.util import nth, strip, absolute_url


class BasicParseTestSpider(GenericSpider):
    name = "test"
    start_urls = ["http://www.test.com"]

    class Meta:
        items = CssTarget("items", ".offer")
        targets = [
            CssTarget("title", ".title::text", [nth(0), strip]),
            CssTarget("discount", ".discount::text", [nth(0), strip]),
            CssTarget("disclaimer", ".disclaimer::text", [nth(0), strip]),
            CssTarget("offer_url", ".offer_url::attr(href)", [nth(0), strip, absolute_url]),
            CssTarget("image_url", ".image::attr(src)", [nth(0), strip])
        ]


class NoMetaSpider(GenericSpider):
    pass


class NoStartSpider(GenericSpider):
    name = "nostart"

    class Meta:
        pass


class GoodSpider(GenericSpider):
    name = "good"
    start_urls = []

    class Meta:
        items = ""
        targets = []
