import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy import Request
from ..items import WoocommerceItem

from scrapy_splash import SplashRequest

class marocstore(Spider):
	name = 'marocstore'
	
	def start_requests(self):

		start_urls = [
			'https://marocstore.nl/shop/fashion.html',
			'https://marocstore.nl/shop/beauty-health.html',
			'https://marocstore.nl/shop/cadeau-woondecoratie.html',
			'https://marocstore.nl/shop/islamitische-artikelen.html',
			'https://marocstore.nl/shop/aanbiedingen.html',
		]

		for url in start_urls:
			yield SplashRequest(
				url=url, 
				args={ 'wait': 0.5 }, 
				callback=self.parse_page
			)
	
	def parse_page(self, response):
		path_category = '#narrow-by-list2 > dd > ol > li > a ::attr(href)'
		urls_category = response.css(path_category).extract()
		
		for url in urls_category:
			category_name = url.split('/shop/')[1]
			
			yield SplashRequest(	
				url=url,
				args={ 'wait': 0.5 }, 
				meta={ 'category_name' : category_name,},
				callback=self.parse_list
			)
	
	def parse_list(self, response):
		path_urls_cards ='.product-item-link ::attr(href)'
		urls_cards = response.css(path_urls_cards).extract()
		
		for url_crad in urls_cards:
			category_name = response.meta['category_name']
			yield SplashRequest(url=url_crad, args={ 'wait': 3 }, meta={'category_name' : category_name,}, callback=self.parse_cards)

		next_page = response.css('.action.next ::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield SplashRequest(url=next_page, args={ 'wait': 0.5 }, meta={'category_name' : category_name,}, callback=self.parse_list)

	def parse_cards(self, response):
		
		details = WoocommerceItem()

		#path_articles = ".product-description"
		#articles = response.css(path_articles)

		path_name = '.base ::text'
		path_sale_path = '.product-info-price > div > span:nth-child(1) > span ::attr(data-price-amount)'
		path_regular_price = '.product-info-price > div > span:nth-child(2) > span ::attr(data-price-amount)'
		path_short_description = ''

		path_descreption = "div[itemprop='description'] > p::text"
		path_currency = ''
		path_image = '.product.media ::attr(src)'
		#path_tags = ''
		#path_attribute_1_name = '.form-control-label ::text'
		#path_attribute_1_values = '.float-left.input-container ::attr(title)'

		#for article in articles:
		details['name'] = str(response.css(path_name).extract_first()).strip()
		
		if response.css(path_sale_path).css('.price ::text').extract_first() is not None:
			details['sale_price'] = str(response.css(path_sale_path).get()).strip().replace('\u20ac\u00a0','')
		else :
			details['sale_price'] = str(response.css('.price-container.price-final_price.tax.weee').css('.price ::text').extract_first()).strip().replace('\u20ac\u00a0','')
		
		details['regular_price'] = str(response.css(path_regular_price).css('.price ::text').extract_first()).strip().replace('\u20ac\u00a0','')
		details['currency'] = str("EUR").strip()

		# det response of those path
		details['categories'] =  ' > '.join(str(e.strip()) for e in response.url.split('https://marocstore.nl/')[1].split('/')[:-1])
		details['description'] = ' '.join(str(e.strip()) for e in response.css(path_descreption).getall())
		#details['tags'] = response.css(path_tags).getall()
		details['images'] = response.css(path_image).getall()
		details['url'] = response.url
		details['parent'] = response.request.headers.get('Referer', None)
		details['published'] = 1
		
		details['in_stock'] = response.css('#qty ::attr(value)').get()
		
		details['sku'] = 0
		
		yield details
