#! /usr/bin/env python3
# coding: utf-8

"""Ouedkniss spider
"""

from scrapy.spiders import SitemapSpider
from lxml import html
import requests


class OuedlnissSpider(SitemapSpider):
    name = "ouedkniss"
    sitemap_urls = [
        'http://www.ouedkniss.com/sitemap/annonces.php',
    ]

    sitemap_rules = [
        ('-automobiles-', 'parse')
    ]

    def parse(self, response, **kwargs):
        """
        parcourir l'annonce
        @param response:
        @param kwargs:
        @return:
        """
        # ids : les champs de cette annnonce
        ids = response.xpath("//div[@id='annonce']//label/text()").getall()
        # values : les valeurs de cette annonce
        values = response.xpath(
            "//div[@id='annonce']//div[@id='Description']//label//following-sibling::span/text()").getall()
        # resultat en dict {id: value}
        data = dict(zip(ids, values))
        # details customisés
        data['prix'] = response.xpath(
            "//div[@id='annonce']//p[@id='Prix']//label//following-sibling::span/text()").get()
        data['prix du neuf'] = response.xpath(
            "//div[@id='annonce']//div[@id='fiche_technique_auto']//label//following-sibling::span/text()").get()
        data['url'] = response.url
        data['name'] = response.css('#Title ::text').extract_first()
        data['annee'] = self.data_validation(data['name'].split(' ')[-1])
        data['marque'] = data['name'].split(' ')[0]
        data['version'] = ' '.join(data['name'].split()[1:-1])

        profile = {}
        if response.css('.Pseudo >a[target="_blank"] ::attr(href)').extract_first():
            url_profile = "https://www.ouedkniss.com/" + response.css(
                '.Pseudo >a[target="_blank"] ::attr(href)').extract_first()
            profile = self.parse_profile(url_profile)

        data['vendeur'] = {
            'numero': response.xpath("//a[contains(@href,'tel:')]/@href").get(),
            'pseudo': response.css('.Pseudo ::text').extract_first(),
            'url': response.css('.Pseudo >a[target="_blank"] ::attr(href)').extract_first(),
            'profile': profile
        }
        data['adresse'] = response.css(".Adresse ::text").extract_first()

        data['images'] = response.css('.gallery_image > img ::attr(src)').extract()
        data['ref ft'] = response.css('#a_fiche_detaillee ::attr(href)').extract_first()
        data['Description'] = response.css('#GetDescription ::text').extract()

        yield data

    def data_validation(self, data):
        try:
            return int(data)
        except Exception:
            return None

    def parse_profile(self, url):
        """
        parcourir le profile du vendeur
        @param url:
        @return data parcouru:
        """
        page = requests.get(url)
        response = html.fromstring(page.content)
        ids = response.xpath("//div[@id='page_left']//label/text()")
        values = response.xpath("//div[@id='page_left']//label//following-sibling::span")
        corrected_values = []
        for value in values:
            corrected_values.append(value.text)

        data = dict(zip(ids, corrected_values))
        return data
