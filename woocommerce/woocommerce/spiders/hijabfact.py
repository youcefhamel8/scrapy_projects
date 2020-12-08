import scrapy
import json
import re
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy import Request
from ..items import WoocommerceItem
from scrapy.selector import Selector

from scrapy_splash import SplashRequest
import xml.dom.minidom as minidom


class HijabfactdSpider(scrapy.Spider):
	name = 'hijabfact'
	allowed_domains = ['hijabfactory.nl']

	def start_requests(self):
		doc = minidom.parse('./data/sitepam/sitemap.xml')
		urls = doc.getElementsByTagName('url')
		for url in urls: 			
			yield SplashRequest(
				url= url.getElementsByTagName('loc')[0].firstChild.data ,
				args={'wait': 0.5},
				callback=self.parse_products
			)

	def parse_products(self, response):
		
		if response.css("meta[property='product:retailer_item_id'] ::attr(content)").get():
			yield {
				'ID': '',
				'Type': '',
				'SKU': response.css("meta[property='product:retailer_item_id'] ::attr(content)").get(), 
				'Name': response.css("meta[property='og:title'] ::attr(content)").get(),
				'Published': '',
				'Is featured?': '',
				'Visibility in catalog': '',
				'Short description': response.css("meta[property='og:description'] ::attr(content)").get(),
				'Description': '',
				'Date sale price starts': '',#resp.get('date_add'),
				'Date sale price ends': '',#resp.get('date_upd'),
				'Tax status': '',
				'Tax class': '',
				'In stock?': 1 if response.css("meta[property='product:availability'] ::attr(content)").get() == "instock" else 0,
				'Stock':'',
				'Backorders allowed?': '',
				'Sold individually?': '',
				'Weight (lbs)': '',
				'Length (in)': '',
				'Width (in)': '',
				'Height (in)': '',
				'Allow customer reviews?': '',
				'Purchase note': '',
				'Sale price': response.css("meta[property='product:price:amount'] ::attr(content)").get() ,
				'Regular price': response.css("meta[property='product:original_price:amount'] ::attr(content)").get(),
				'Categories': ''.join(response.css("ol ::text").getall()[2:-1]),
				'Tags': '',
				'Shipping class': '',
				'Images': response.css("meta[property='og:image'] ::attr(content)").getall(),
				'Download limit': '',
				'Download expiry days': '',
				'Parent': '',
				'Grouped products': '',
				'Upsells': '',
				'Cross-sells': '',
				'External URL': response.url,
				'Button text': '',
				'Position': '',
				'Attribute 1 name': 'kleuren',
				'Attribute 1 value(s)': response.css('.l-product-col-2').css('a ::attr(alt)').getall(),
				'Attribute 1 visible': '',
				'Attribute 1 global': '',
				'Attribute 2 name': 'Afmeting',
				'Attribute 2 value(s)': response.css('.l-product-col-2').css('label ::text').getall(),
				'Attribute 2 visible': '',
				'Attribute 2 global': '',
				'Meta: _wpcom_is_markdown': '',
				'Download 1 name': '',
				'Download 1 URL	': '',
				'Download 2 name': '',
				'Download 2 URL': '',
			}
