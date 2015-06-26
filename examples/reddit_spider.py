from scrapyz.core import GenericSpider, Target

class RedditSpider(GenericSpider):
    name = "reddit"
    start_urls = ["https://www.reddit.com/"]

    class Meta:
        elements = ".thing"
        targets = [
            Target("rank", ".rank::text"),
            Target("upvoted", ".upvoted::text"),
            Target("dislikes", ".dislikes::text"),
            Target("likes", ".likes::text"),
            Target("title", "a.title::text"),
            Target("domain", ".domain > a::text"),
            Target("tagline", ".tagline > time::attr(datetime)"),
            Target("author", ".tagline > .author::text"),
            Target("subreddit", ".tagline > .subreddit::text"),
            Target("comments", ".comments::text")
        ]