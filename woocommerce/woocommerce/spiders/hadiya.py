import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import json


class HadiyaSpider(scrapy.Spider):
	name = 'hadiya'
	allowed_domains = ['hadiya.eu']

	def start_requests(self):

		for p in range(1, 50):
			yield scrapy.Request(
				url=f'https://www.hadiya.eu/nl/10-hadiya-eidmubarak?page={p}',
				callback=self.parse_lists
			)

	def parse_lists(self, response):
		urls = response.css('.h3.product-title ::attr(href)').getall()
		for url in urls:
			yield scrapy.Request(
				url=url,
				callback=self.parse_products
			)

	def parse_products(self, response):
		data = json.loads(response.css(
			"#product-details ::attr(data-product)").get())

		yield {
			'ID': '',
			'Type': '',
			'SKU': data['id_product'],
			'Name': data['name'],
			'Published': '',
			'Is featured?': '',
			'Visibility in catalog': '',
			'Short description': data['description_short'],
			'Description': data['description'],
			'Date sale price starts': data['date_add'],
			'Date sale price ends': '', # data['date_upd'],
			'Tax status': '',
			'Tax class': '',
			'In stock?': 1 if data['quantity'] > 0 else 0,
			'Stock': data['quantity'],
			'Backorders allowed?': '',
			'Sold individually?': '',
			'Weight (lbs)': '',
			'Length (in)': '',
			'Width (in)': '',
			'Height (in)': '',
			'Allow customer reviews?': '',
			'Purchase note': '',
			'Sale price': data['price_amount'],
			'Regular price': data['price_without_reduction'],
			'Categories': data['category_name'],
			'Tags': data['meta_keywords'],
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
