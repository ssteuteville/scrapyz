from scrapy import Item


def gen_item(fields):
    return type("GenericItem", (Item,), fields)
