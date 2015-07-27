from scrapyz.core import *
from scrapyz.pipelines import RequiredFields
from scrapyz.util import absolute_url


def join(value, response):
    if isinstance(value, (list, tuple)):
        value = " ".join(value)
    return value


class RedditSpider(GenericSpider):
    name = "reddit"
    start_urls = ["https://www.reddit.com/"]

    class Meta:
        items = CssTarget("items", ".thing")
        targets = [
            CssTarget("rank", ".rank::text"),
            CssTarget("upvoted", ".upvoted::text"),
            CssTarget("dislikes", ".dislikes::text"),
            CssTarget("likes", ".likes::text"),
            CssTarget("title", "a.title::text"),
            CssTarget("domain", ".domain > a::text"),
            CssTarget("datetime", ".tagline > time::attr(datetime)"),
            CssTarget("author", ".tagline > .author::text"),
            CssTarget("subreddit", ".tagline > .subreddit::text"),
            CssTarget("comments", ".comments::text")
        ]


class RedditSpider2(IndexDetailSpider):
    name = "reddit2"
    start_urls = ["https://www.reddit.com/"]

    class Meta:
        detail_path = [
            CssTarget("detail_path", ".title > a::attr(href)", [absolute_url])
        ]
        detail_targets = [
            CssTarget("content", ".usertext-body > div > p::text", [join]),
        ]
        items = CssTarget("items", ".thing")
        targets = [
            CssTarget("rank", ".rank::text"),
            CssTarget("upvoted", ".upvoted::text"),
            CssTarget("dislikes", ".dislikes::text"),
            CssTarget("likes", ".likes::text"),
            CssTarget("title", "a.title::text"),
            CssTarget("domain", ".domain > a::text"),
            CssTarget("datetime", ".tagline > time::attr(datetime)"),
            CssTarget("author", ".tagline > .author::text"),
            CssTarget("subreddit", ".tagline > .subreddit::text"),
            CssTarget("comments", ".comments::text")
        ]
