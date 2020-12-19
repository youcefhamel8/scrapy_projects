# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrunchbaseItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    current_jobs = scrapy.Field()
    social_urls = scrapy.Field()
    education = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()
    gender = scrapy.Field()
    title_job = scrapy.Field()
    rank = scrapy.Field()
    region = scrapy.Field()
    investor_type = scrapy.Field()
    url = scrapy.Field()
    crunch_id = scrapy.Field()