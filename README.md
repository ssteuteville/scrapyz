
## Scrapyz
##### "scrape easy" is an extension for the python web scraping framework scrapy. The aim of this package is to cut down on the amount of code needed to create simple spiders with scrapy.
---
###Installation:

pip install scrapyz

[![PyPI version](https://img.shields.io/pypi/v/scrapyz.svg)](https://img.shields.io/pypi/v/scrapyz.svg)
[![PyPi status](https://img.shields.io/pypi/status/scrapyz.svg)](https://img.shields.io/pypi/status/scrapyz.svg)
[![PyPi python version](https://img.shields.io/pypi/pyversions/scrapyz.svg)](https://img.shields.io/pypi/pyversions/scrapyz.svg)
# Usage:
##### These examples apply to the current version released to Pypi. See examples/tests for updated usage. See core.py for target classes and util.py for helpers.
For scraping items off a single page:
```python

  class RedditSpider(GenericSpider):
      name = "reddit"
      start_urls = ["https://www.reddit.com/"]
  
      class Meta:
          items = CssTarget("items", ".thing")
          targets = [   # scrapyz also has XpathTarget and RegexTarget classes for extraction
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
```

For scraping data off of an index page, following a link and collecting data off of a details page:  
```python

  class RedditSpider2(IndexDetailSpider):
      name = "reddit2"
      start_urls = ["https://www.reddit.com/"]
  
      class Meta:
          detail_path = [CssTarget("detail_path", ".title > a::attr(href)", [absolute_url])]
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
```

pipelines:
```python
class RedditSpider(GenericSpider):
    name = "reddit"
    start_urls = ["https://www.reddit.com/"]
    pipelines = [scrapyz.pipelines.RequiredFields]

    class Meta:
        items = CssTarget("items", ".thing")
        required_fields = ["rank", "author", "domain", "comments"]
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
```
To include all scrapyz pipelines to your project add this to the bottom of your project's settings.py:
```
ITEM_PIPELINES.update(pipelines.get_scrapyz_pipelines())
```
note: scrapyz pipelines will only execute if you include a field called pipelines in your spider and the appropriate meta fields. Documentation for this might come later. For now use the code and comments.
Contribution
-----------
Please feel free to submit pull requests or create issues. If you have a feature request create an issue with the label Feature Request.
