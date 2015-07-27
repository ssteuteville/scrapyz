import unittest
from scrapy.exceptions import DropItem
from scrapyz.pipelines import RequiredFields, MinTargets
from util import fake_response
from spiders import *


class TestSpiders(unittest.TestCase):
    """
        Tests the basic functionality of GenericSpider.
    """
    expected_items = [
        {
             'disclaimer': u'Disclaimer One',
             'discount': u'Discount One',
             'image_url': u'Image One',
             'offer_url': 'http://www.test.com/offer_1',
             'title': u'Title One'
        },
        {
             'disclaimer': u'Disclaimer Two',
             'discount': u'Discount Two',
             'image_url': u'Image Two',
             'offer_url': 'http://www.test.com/offer_2',
             'title': u'Title Two'
        },
        {
             'disclaimer': u'Disclaimer Three',
             'discount': u'Discount Three',
             'image_url': u'Image Three',
             'offer_url': 'http://www.test.com/offer_3',
             'title': u'Title Three'
        }
    ]

    """
        Test a full parse on a static html document.
    """
    def test_basic_parse(self):
        spider = BasicParseFirstElementTestSpider()
        response = fake_response("basic_parse.html")
        results = [item for item in spider.parse(response)]
        self.assertEqual(len(results), 3)
        for result, expected in zip(results, self.expected_items):
            for key in result.keys():
                self.assertEqual(result[key], expected[key])

    """
        Test GenericSpider's helper function.
    """
    def test_start_requests(self):
        spider = BasicParseFirstElementTestSpider()
        spider.start_urls = ["http://abc.com", "http://123.com", "http://abc.com"]
        for i, request in enumerate(spider.start_requests()):
            self.assertEqual(request.url, spider.start_urls[i])

    """
        Test that the proper exceptions are raised in the right situations.
    """
    def test_bad_spider(self):
        classes = [NoMetaSpider, NoStartSpider]
        for cls in classes:
            with self.assertRaises(AttributeError):
                spider = cls()

    def test_good_spider(self):
        try:
            spider = GoodSpider()
        except Exception:
            self.fail()


class TestPipelines(unittest.TestCase):
    """
        Test that pipelines.RequiredFields functions properly
    """
    def test_required_fields_fail(self):
        spider = BasicParseTestSpider()
        spider.Meta.required_fields = ["disclaimer", "discount", "image_url", "offer_url", "title"]
        spider.pipelines = [RequiredFields]
        pipeline = RequiredFields()
        response = fake_response("basic_some_missing.html")
        with self.assertRaises(DropItem):
            for item in spider.parse(response):
                    pipeline.process_item(item, spider)


    def test_required_fields_success(self):
        spider = BasicParseTestSpider()
        spider.Meta.required_fields = ["disclaimer", "discount", "image_url", "offer_url", "title"]
        spider.pipelines = [RequiredFields]
        response = fake_response("basic_parse.html")
        pipeline = RequiredFields()
        try:
            results = [pipeline.process_item(item, spider) for item in spider.parse(response)]
        except DropItem:
            self.fail("Valid required fields dropped item.")
        self.assertEqual(len(results), 3)

    def test_required_fields_attribute_exception(self):
        spider = BasicParseTestSpider()
        spider.pipelines = [RequiredFields]
        pipeline = RequiredFields()
        response = fake_response("basic_parse.html")
        with self.assertRaises(AttributeError):
            results = [pipeline.process_item(item, spider) for item in spider.parse(response)]

    def test_min_target_fail(self):
        spider = BasicParseTestSpider()
        spider.pipelines = [MinTargets]
        spider.Meta.min_targets = 4
        pipeline = MinTargets()
        response = fake_response("basic_some_missing.html")
        with self.assertRaises(DropItem):
            results = [pipeline.process_item(item, spider) for item in spider.parse(response)]

    def test_min_target_success(self):
        spider = BasicParseTestSpider()
        spider.pipelines = [MinTargets]
        spider.Meta.min_targets = 4
        pipeline = MinTargets()
        response = fake_response("basic_parse.html")
        try:
            results = [pipeline.process_item(item, spider) for item in spider.parse(response)]
        except DropItem:
            self.fail("min_target dropeed item when it shouldn't.")

class TestUtil(unittest.TestCase):
    pass
