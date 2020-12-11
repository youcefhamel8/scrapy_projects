#! /usr/bin/env python3
# coding: utf-8
"""
CRUNCHBASE
"""

from crunchbase.spiders import postman as postman
# from scrapy import Spider
from scrapy import Request
from scrapy import Spider
from scrapy.spiders import SitemapSpider
#from scrapy_selenium import SeleniumRequest
import json
import xml.dom.minidom as minidom

class PersonSpider(SitemapSpider):
    name = "personnes"
    sitemap_urls = ['file:///Users/mac/Documents/dev/scrapy_projects/crunchbase/crunchbase/spiders/draft/people.xml']
    sitemap_rules = [('/person','parse')]
    
    def parse(self, response):
        yield Request(url=response.url, meta={'dont_merge_cookies': True}, callback=self.parse_p)
    
    def parse_p(self, response):
        pass
        #yield {'url': response.url}

        
