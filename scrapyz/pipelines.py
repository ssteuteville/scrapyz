import functools
from scrapy.exceptions import DropItem

"""
    Helper Functions
"""


def check_spider_pipelines(process_item_method):
    """
        I can't remember where I found this but
    """

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        if hasattr(spider, "pipelines") and self.__class__ in spider.pipelines:
            return process_item_method(self, item, spider)
        else:
            return item

    return wrapper

def get_scrapyz_pipelines():
    return {
        'scrapyz.pipelines.RequiredFields': 300,
        'scrapyz.pipelines.MinTargets': 300,
    }

"""
    Pipeline Classes
"""


class FilterBase(object):
    """
        Abstract class. Override the validate function to suit your needs.
    """

    @check_spider_pipelines
    def process_item(self, item, spider):
        if self.validate(item, spider):
            return item
        raise DropItem("Item failed in filter pipeline.")

    def validate(self, item, spider):
        """
            Override this function to return true if an item passes the filter and false otherwise.
            You can use attributes on the spider or the item for your filtering.
        """
        return item


class RequiredFields(FilterBase):
    """
        Requires the spider to implement Meta.required_fields. Drops any item that doesn't have a value for each
        required field.
    """

    def validate(self, item, spider):
        missing = []
        for field in spider.Meta.required_fields:
            if field not in item:
                missing.append(field)
        return not missing


class MinTargets(FilterBase):
    """
        Filters out items that weren't able to hit a minimum number for Targets.
    """

    def validate(self, item, spider):
        return len(item.keys()) >= spider.Meta.min_targets

