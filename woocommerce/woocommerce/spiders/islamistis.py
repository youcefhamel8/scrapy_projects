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


class IslamistisdSpider(scrapy.Spider):
	name = 'islamistis'
	allowed_domains = ['islamitischekleding.nl']

	def start_requests(self):
		for p in range(1, 92): #92			
			yield scrapy.Request(
				url=f'https://islamitischekleding.nl/nl/2-home?page={p}&content_only=1&infinitescroll=1',
				#args={'wait': 0.5},
				callback=self.parse_product
			)

	def parse_product(self, response):
		urls = response.css('#content-wrapper').css('.h3.product-title > a ::attr(href)').getall()
		for url in urls:
			yield scrapy.Request(
				url=url,
			#	args={'wait': 0.5},
				callback=self.parse_details,
			)

	def parse_details(self, response):
		print('PRODUCT : ',response.url)
		yield {
			'ID': '',
			'Type': '',
			'SKU': response.css("meta[property='product:retailer_item_id'] ::attr(content)").get(), 
			'Name': response.css("meta[property='og:title'] ::attr(content)").get(),
			'Published': '',
			'Is featured?': '',
			'Visibility in catalog': '',
			'Short description': response.css("meta[property='og:description'] ::attr(content)").get(),
			'Description': response.css('#ui-accordion-accordion-panel-0 ::text').getall(),
			'Date sale price starts': '',#resp.get('date_add'),
			'Date sale price ends': '',#resp.get('date_upd'),
			'Tax status': '',
			'Tax class': '',
			'In stock?': 1 if response.css("meta[property='product:availability'] ::attr(content)").get() == "In stock" else 0,
			'Stock': response.css('.product-quantities.col-sm-6 ::attr(data-stock)').get(),
			'Backorders allowed?': '',
			'Sold individually?': '',
			'Weight (lbs)': '',
			'Length (in)': '',
			'Width (in)': '',
			'Height (in)': '',
			'Allow customer reviews?': '',
			'Purchase note': '',
			'Sale price': response.css("meta[property='product:price:amount'] ::attr(content)").get() ,
			'Regular price': response.css("span[itemprop='price'] ::attr(content)").get(),
			'Categories': response.css("meta[itemprop='category'] ::attr(content)").get(),
			'Tags': '',
			'Shipping class': '',
			'Images': response.css("meta[property='og:image'] ::attr(content)").get(),
			'Download limit': '',
			'Download expiry days': '',
			'Parent': '',
			'Grouped products': '',
			'Upsells': '',
			'Cross-sells': '',
			'External URL': response.url,
			'Button text': '',
			'Position': '',
			'Attribute 1 name': '',
			'Attribute 1 value(s)': '',
			'Attribute 1 visible': '',
			'Attribute 1 global': '',
			'Attribute 2 name': '',
			'Attribute 2 value(s)': '',
			'Attribute 2 visible': '',
			'Attribute 2 global': '',
			'Meta: _wpcom_is_markdown': '',
			'Download 1 name': '',
			'Download 1 URL	': '',
			'Download 2 name': '',
			'Download 2 URL': '',
		}
