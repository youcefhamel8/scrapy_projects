import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy import Request
from ..items import WoocommerceItem

from scrapy_splash import SplashRequest

class libasi(Spider):
	name = 'libasi'
	
	def start_requests(self):

		start_urls = [
			'https://www.libasi.nl/106-schoenen',
			'https://www.libasi.nl/103-tassen',
			'https://www.libasi.nl/105-kinderkleding',
			'https://www.libasi.nl/101-kleding',
			'https://www.libasi.nl/100-spelden-en-sieraden',
			'https://www.libasi.nl/102-hijab',
		]

		for url in start_urls:
			yield SplashRequest(url=url, args={ 'wait': 0.5 }, callback=self.parse_list)
	
	def parse_list(self, response):
		path_urls_cards = '.h3.product-title > a ::attr(href)'
		urls_cards = response.css(path_urls_cards).extract()

		for url_crad in urls_cards:
			yield SplashRequest(url=url_crad,
								args={'wait': 3},
								callback=self.parse_cards)

		next_page = response.css('#infinity-url ::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield SplashRequest(url=next_page,
								args={'wait': 0.5},
								callback=self.parse_list)

	def parse_cards(self, response):

		details = WoocommerceItem()

		# define path
		path_name = '.h1.page-title ::text'
		path_sale_path = '.current-price > .product-price ::attr(content)'
		path_regular_price = '.product-discount > .regular-price ::text'
		path_category = ''
		path_short_description = 'div[itemprop="description"] ::text'
		path_descreption = '.section-content > .product-description > div > p ::text'
		path_currency = ''
		path_image = "img[itemprop='image'] ::attr(src)"
		path_tags = '.iqitproducttags > ul > li ::text'
		path_attribute_1_name = '.form-control-label ::text'
		path_attribute_1_values = '.float-left.input-container ::attr(title)'


		# det response of those path
		details['name'] = str(response.css(path_name).get()).strip()
		details['sale_price'] = str(response.css(path_sale_path).get()).strip().replace('\u20ac\u00a0','')
		details['regular_price'] = str(response.css(path_regular_price).get()).strip().replace('\u20ac\u00a0','')
		details['currency'] = str("EUR").strip()
		details['categories'] = ' > '.join(str(e.strip()) for e in response.css("span[itemprop='name'] ::text").getall()[:-1])
		details['short_description'] = str(response.css(path_short_description).extract_first()).strip()
		details['description'] = ' '.join(str(e.strip()) for e in response.css(path_descreption).getall())
		details['tags'] = response.css(path_tags).getall()
		details['images'] = response.css(path_image).getall()
		details['url'] = response.url
		details['parent'] = response.request.headers.get('Referer', None)
		details['published'] = 1
		
		if response.css('.btn.btn-primary.btn-lg.add-to-cart ::attr(disabled)').get() is not None:
			details['in_stock'] = 1
		
		details['sku'] = response.url.split('/')[-1].split('-')[0]
		details['attribute_1_name'] = str(response.css(path_attribute_1_name).get()).strip()
		
		# if size or color
		values = response.css(path_attribute_1_values).getall() or response.css('.form-control.form-control-select ::attr(title)').getall()
		details['attribute_1_values'] = ', '.join(str(e.strip()) for e in values) 

		yield details