from scrapyz.core import GenericSpider, CssTarget

class RedditSpider(GenericSpider):
    name = "reddit"
    start_urls = ["https://www.reddit.com/"]

    class Meta:
        elements = ".thing"
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