#! /usr/bin/env python3
# coding: utf-8

"""CRUNCHBASE
"""
from scrapy.spiders import SitemapSpider
from ..items import CrunchbaseItem


class PersonSpider(SitemapSpider):
    name = "personnes"
    
    def urls(self):
        urls = []
        for i in range(0, 23):
            res = f"https://www.crunchbase.com/www-sitemaps/sitemap-people-"+str(i)+".xml.gz"
            ulrs.append(res)
        return urls

    sitemap_urls = self.urls()

    sitemap_rules = [('', 'parse')]

    def parse(self, response):
        personne = CrunchbaseItem()
        personne['url'] = response.url
        personne['crunch_id'] = response.url.split('/')[-1]
        personne['name'] = response.css('.profile-name ::text').get()
        personne['current_jobs'] = self.get_cards(response, "jobs")
        personne['social_urls'] = {
            'linkedin': response.xpath("//*[contains(.//span/span/text(), 'LinkedIn')]/following-sibling::field-formatter//a/@href").get(),
            'twitter': response.xpath("//*[contains(.//span/span/text(), 'Twitter')]/following-sibling::field-formatter//a/@href").get(),
            'facebook': response.xpath("//*[contains(.//span/span/text(), 'Facebook')]/following-sibling::field-formatter//a/@href").get(),
        }
        personne['education'] = self.get_cards(response, "education")
        personne['description'] = response.css(
            '.description.has-overflow ::text').get()
        personne['location'] = response.xpath(
            "//*[contains(.//span/span/text(), 'Location')]/following-sibling::field-formatter//a/@title").getall()
        personne['region'] = response.xpath(
            "//*[contains(.//span/span/text(), 'Regions')]/following-sibling::field-formatter//a/@title").get()
        personne['gender'] = response.xpath(
            "//*[contains(.//span/span/text(), 'Gender')]/following-sibling::field-formatter//span/@title").get()
        personne['title_job'] = response.xpath(
            "//*[contains(.//span/span/text(), 'Primary Job')]/following-sibling::field-formatter//span/@title").get()
        personne['rank'] = response.xpath(
            "//*[contains(.//span/span/text(), 'CB Rank')]/following-sibling::field-formatter//a/text()").get()
        personne['investor_type'] = response.xpath(
            "//*[contains(.//span/span/text(), 'Type')]/following-sibling::field-formatter//span/@title").getall()
        yield personne

    def get_cards(self, response, id):  # id : education or jobs
        res = {}
        for i in response.xpath(f"//*[contains(@id, '{id}')]/following-sibling::section-card//li"):
            res[i.css('a::text').get()] = i.css(
                'field-formatter ::text').getall()

        return res
