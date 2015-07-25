import unittest
from util import fake_response
from spiders import *


class TestGenericSpiders(unittest.TestCase):
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

    def test_basic_parse(self):
        spider = BasicParseTestSpider()
        response = fake_response("basic_parse.html")
        results = [item for item in spider.parse(response)]
        self.assertEqual(len(results), 3)
        for result, expected in zip(results, self.expected_items):
            for key in result.keys():
                self.assertEqual(result[key], expected[key])

    def test_start_requests(self):
        spider = BasicParseTestSpider()
        spider.start_urls = ["http://abc.com", "http://123.com", "http://abc.com"]
        for i, request in enumerate(spider.start_requests()):
            self.assertEqual(request.url, spider.start_urls[i])


class TestSpiderExceptions(unittest.TestCase):
    """
        Tests that the proper exceptions are raised in the right situations.
    """
    def test_bad_spider(self):
        classes = [NoMetaSpider, NoStartSpider]
        for cls in classes:
            with self.assertRaises(AttributeError):
                spider = cls()
        try:
            spider = GoodSpider()
        except AttributeError:
            self.fail("GoodSpider raised SWOSpiderValidationError when it shouldn't.")

    def test_good_spider(self):
        try:
            spider = GoodSpider()
        except Exception:
            self.fail()


class TestUtil(unittest.TestCase):
    pass
