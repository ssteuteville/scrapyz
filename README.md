
## Scrapyz
##### "scrape easy" is an extension for the python web scraping framework scrapy. The aim of this package is to cut down on the amount of code needed to create simple spiders with scrapy.
---
###Installation:

pip install scrapyz

[![PyPI version](https://img.shields.io/pypi/v/scrapyz.svg)](https://img.shields.io/pypi/v/scrapyz.svg)
[![PyPi downloads](https://img.shields.io/pypi/dm/scrapyz.svg)](https://img.shields.io/pypi/dm/scrapyz.svg)
[![PyPi status](https://img.shields.io/pypi/status/scrapyz.svg)](https://img.shields.io/pypi/status/scrapyz.svg)
[![PyPi python version](https://img.shields.io/pypi/pyversions/scrapyz.svg)](https://img.shields.io/pypi/pyversions/scrapyz.svg)
[![PyPi license](https://img.shields.io/pypi/l/scrapyz.svg)](https://img.shields.io/pypi/l/scrapyz.svg)
Usage:
------
For scraping items off a single page:
```python

  class RedditSpider(GenericSpider):
      name = "reddit"
      start_urls = ["https://www.reddit.com/"]
  
      class Meta:
          items = ".thing"
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

For scraping data off of an index page, following a link and collecting data off of a details page:  
```python

  class RedditSpider2(IndexDetailSpider):
      name = "reddit2"
      start_urls = ["https://www.reddit.com/"]
  
      class Meta:
          detail_path = CssTarget("detail_path", ".title > a::attr(href)", [absolute_url])
          detail_targets = [
              CssTarget("content", ".usertext-body > div > p::text", [join]),
          ]
          items = ".thing"
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
