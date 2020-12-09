import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import json
from scrapy.spiders import SitemapSpider
import re

class islamitischeSpider(SitemapSpider):
	name = 'islamitische'
	allowed_domains = ['islamitische-boekhandel.nl']

	sitemap_urls = [
		'https://www.islamitische-boekhandel.nl/sitemap.xml',
	]

	sitemap_rules = [
		('/about/', 'denied'),
		('/tag/', 'denied'),
		('/about/', 'denied'),
	]

	def denied(self,response):
		pass

	def parse(self, response):
		yield scrapy.Request(
			url=response.url, callback=self.parse_product)
		print(response.url)

	def parse_product(self, response):
		#data = re.findall("var shopCategories =(.+?);\n", response.body.decode("utf-8"), re.S)
		#print(data)
		try:
			yield {
				'ID': '',
				'Type': '',
				'SKU': response.css('.active > a ::attr(href)').get().split('/')[-1], 
				'Name': response.css("meta[property='og:title'] ::attr(content)").get(),
				'Published': '',
				'Is featured?': '',
				'Visibility in catalog': '',
				'Short description': '',
				'Description': response.css("meta[property='og:description'] ::attr(content)").get(),
				'Date sale price starts': '',#resp.get('date_add'),
				'Date sale price ends': '',#resp.get('date_upd'),
				'Tax status': '',
				'Tax class': '',
				'In stock?': 1 if response.css('.stock ::text').get() else 0,
				'Stock':'',
				'Backorders allowed?': '',
				'Sold individually?': '',
				'Weight (lbs)': '',
				'Length (in)': '',
				'Width (in)': '',
				'Height (in)': '',
				'Allow customer reviews?': '',
				'Purchase note': '',
				'Sale price': response.css('.price > .new-price ::text').get(),
				'Regular price': response.css('.price > .old-price ::text').get(),
				'Categories': '/'.join(response.css('.breadcrumbs ::text').getall()[1:-1]),
				'Tags': response.css("meta[name='keywords'] ::attr(content)").get() ,
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

		except Exception as e:
			print(f"Warning #001 exception {response.url}; {e}.")
