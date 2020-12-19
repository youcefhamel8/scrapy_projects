#! /usr/bin/env python3
# coding: utf-8

"""Concilio spider
"""

from scrapy.spiders import SitemapSpider


class ConcilioSpider(SitemapSpider):
    name = "concilio"
    
    sitemap_urls = [
        'https://www.concilio.com/sitemap.xml'
    ]

    sitemap_rules = [
        ('','parse'),
    ]

    def parse(self, response):
        """Parse peer page
        Args:
            response (htmlResponse): html page
        Yields:
            item : title
        """

        yield {
            'title': response.css('meta[name="title"] ::attr(content)').get(),
        }
