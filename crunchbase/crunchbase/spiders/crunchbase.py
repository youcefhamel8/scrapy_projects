#! /usr/bin/env python3
# coding: utf-8
"""
CRUNCHBASE
"""

from scrapy import Request
from scrapy.spiders import SitemapSpider


class PersonSpider(SitemapSpider):
    name = "personnes"
    sitemap_urls = [
        'file:///Users/mac/Documents/dev/scrapy_projects/crunchbase'
        '/crunchbase/spiders/draft/people.xml']
    sitemap_rules = [('/person', 'parse')]

    def parse(self, response):
        yield Request(url=response.url, meta={'dont_merge_cookies': True},
                      callback=self.parse_p)
