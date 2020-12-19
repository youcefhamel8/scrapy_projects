import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy import Request
from ..items import WoocommerceItem

from scrapy_splash import SplashRequest


class sunnah(Spider):
	name = 'sunnah'

	def start_requests(self):

		start_urls = [
			'https://www.sunnahcenter.com/3-boeken',
			'https://www.sunnahcenter.com/12-islamitische-kleding',
			'https://www.sunnahcenter.com/73-cosmetica',
			'https://www.sunnahcenter.com/87-eten-drinken',
			'https://www.sunnahcenter.com/151-cadeau-decoratie',
			"https://www.sunnahcenter.com/343-ramadan-",
			"https://www.sunnahcenter.com/344-eid",
			"https://www.sunnahcenter.com/280-hadj-umrah-",
			"https://www.sunnahcenter.com/91-aanbieding",
		]

		for url in start_urls:
			yield SplashRequest(
				url=url,
				args={'wait': 0.5},
				callback=self.parse_page
			)

	def parse_page(self, response):
		path_category = '#left-column > div > div > ul > li > a ::attr(href)'
		urls_category = response.css(path_category).extract()

		for url in urls_category:
			category_name = url.split('/')[-1]

			yield SplashRequest(
				url=url,
				args={'wait': 0.5},
				meta={'category_name': category_name, },
				callback=self.sub_page
			)

	def sub_page(self, response):
		path_category = '#left-column > div > div > ul > li > a ::attr(href)'
		urls_category = response.css(path_category).extract()

		category_name = response.meta['category_name']

		for url in urls_category:
			sub_category_name = url.split('/')[-1]

			yield SplashRequest(
				url=url,
				args={'wait': 0.5},
				meta={
					'sub_category_name': sub_category_name,
					'category_name': category_name,
				},
				callback=self.parse_list
			)

	def parse_list(self, response):
		path_urls_cards = '.h3.product-title > a ::attr(href)'
		urls_cards = response.css(path_urls_cards).extract()

		for url_crad in urls_cards:
			category_name = response.meta['category_name']
			sub_category_name = response.meta['sub_category_name']
			yield SplashRequest(url=url_crad,
								args={'wait': 0.5},
								meta={
									'sub_category_name': sub_category_name,
									'category_name': category_name,
								},
								callback=self.parse_cards)

		next_page = response.css('#infinity-url ::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield SplashRequest(url=next_page,
								args={'wait': 0.5},
								meta={
									'sub_category_name': sub_category_name,
									'category_name': category_name,
								},
								callback=self.parse_list)


	def parse_cards(self, response):
		category = ""
		try :
			category = '/'.join(response.css('ol').css("span[itemprop='name'] ::text").getall()[1:-1])
		except :
			pass

		yield {
				'ID': '',
				'Type': '',
				'SKU': response.css("#product_page_product_id ::attr(value)").get(), 
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
				'In stock?': 1 if 'InStock' in response.css("link[itemprop='availability'] ::attr(href)").get() else 0,
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
				'Categories': category,
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
				'Attribute 1 name': 'Kleur',
				'Attribute 1 value(s)': response.css('.col-md-6.col-product-info').css(".clearfix.product-variants-item.product-variants-item-3").css(".sr-only ::text").getall() ,
				'Attribute 1 visible': '',
				'Attribute 1 global': '',
				'Attribute 2 name': 'Maat',
				'Attribute 2 value(s)': response.css('.col-md-6.col-product-info').css(".clearfix.product-variants-item.product-variants-item-1 ::attr(title)").getall(),
				'Attribute 2 visible': '',
				'Attribute 2 global': '',
				'Meta: _wpcom_is_markdown': '',
				'Download 1 name': '',
				'Download 1 URL	': '',
				'Download 2 name': '',
				'Download 2 URL': '',
			}