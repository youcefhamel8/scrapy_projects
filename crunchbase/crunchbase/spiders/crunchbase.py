#! /usr/bin/env python3
# coding: utf-8

"""Crunchbase
"""

from scrapy.spiders import SitemapSpider
from ..items import CrunchbaseItem


class PersonSpider(SitemapSpider):
    name = "personnes"

    # sitemap_urls = [
    #    f"https://www.crunchbase.com/www-sitemaps/sitemap-people-{i}.xml.gz" for i in range(0, 23)
    # ]

    sitemap_urls = ["https://www.crunchbase.com/www-sitemaps/sitemap-people-0.xml.gz"]
    #for i in range(0, 23):
    #    sitemap_urls.append("https://www.crunchbase.com/www-sitemaps/sitemap-people-" + str(i) + ".xml.gz")

    sitemap_rules = [('', 'parse')]

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        personne = CrunchbaseItem()
        personne['url'] = response.url
        personne['crunch_id'] = response.url.split('/')[-1]
        personne['name'] = response.css('.profile-name ::text').extract_first()
        personne['current_jobs'] = self.get_cards(response, "jobs")
        personne['social_urls'] = {
            'linkedin': response.xpath(
                "//*[contains(.//span/span/text(), 'LinkedIn')]/following-sibling::field-formatter//a/@href").get(),
            'twitter': response.xpath(
                "//*[contains(.//span/span/text(), 'Twitter')]/following-sibling::field-formatter//a/@href").get(),
            'facebook': response.xpath(
                "//*[contains(.//span/span/text(), 'Facebook')]/following-sibling::field-formatter//a/@href").get(),
        }
        personne['education'] = self.get_cards(response, "education")
        personne['description'] = response.css(
            '.description.has-overflow ::text').extract_first()
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
        """
        get all li as cards ad return result as dict
        @param response:
        @param id:
        @return: dictionary {key : details }
        """

        res = {}
        # for i in response.xpath(f"//*[contains(@id, '{id}')]/following-sibling::section-card//li"):
        for i in response.xpath("//*[contains(@id, '" + str(id) + "')]/following-sibling::section-card//li"):
            res[i.css('a::text').get()] = i.css(
                'field-formatter ::text').extract()
        return res

