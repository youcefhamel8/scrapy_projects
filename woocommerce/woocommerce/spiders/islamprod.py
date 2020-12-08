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


class IslamProdSpider(scrapy.Spider):
	name = 'islamprod'
	allowed_domains = ['www.islamproducten.nl']

	def start_requests(self):

		for p in range(1, 45):

			headers = {
				':authority': 'www.islamproducten.nl',
				':method': 'GET',
				':path': f'/Winkel?order=product.position.asc&page={p}&from-xhr',
				':scheme': 'https',
				'accept': 'application/json, text/javascript, */*; q=0.01',
				'accept-encoding': 'gzip, deflate',
				'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
				'cache-control': 'no-cache',
				'cookie': '__cfduid=d6c2fe1a2bf9d533ad04d8857e8cf85121606514312; _gcl_au=1.1.597660472.1606514315; rrpvid=467267190402739; rcuid=5fc1768e08718b000151b7ad; PHPSESSID=mp9870jmn3c941piqs66v50gre; _hjTLDTest=1; _hjid=fdd66ed9-ba27-486f-aebc-a5bc6d8304a1; mtc_id=369421; mtc_sid=h08d1cfzee317nc0idprepi; mautic_device_id=h08d1cfzee317nc0idprepi; _ga=GA1.2.73702135.1607280935; _gid=GA1.2.769116499.1607280935; _hjAbsoluteSessionInProgress=0; _dc_gtm_UA-1374679-1=1; _gat_UA-1374679-1=1; __atuvc=1%7C50; _hjIncludedInPageviewSample=1; PrestaShop-ec0298640d470f574feedd17a4863133=def50200db17b682add4b3b01e0cb84670365752ad1c803fff82b852e3bcbbf710e0641d3a647df57191c2b4c48e823121b2a7fce85360304971cbcbc145727b8c4d687ac0b77a970c80c7b35f64530a20a2f473959b2ca3a4c37937cd6418e46ca5ddf9d6428478f32e68acd4aeef0721991621581646a7e100ee988c044a657a681e1dbd3884a798360f686651711629fc44742f789fa386984f6dcc075f74a92c3971228e81e8b03e2368bb3a73a3923425750a6119f69c18c95be57c589b015ed15537feb6c17888e8',
				'pragma': 'no-cache',
				'referer': 'https://www.islamproducten.nl/Winkel?order=product.position.asc',
				'sec-fetch-dest': 'empty',
				'sec-fetch-mode': 'cors',
				'sec-fetch-site': 'same-origin',
				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
				'x-requested-with': 'XMLHttpRequest',
			}
			yield scrapy.Request(
				url=f'https://www.islamproducten.nl/Winkel?order=product.position.asc&page={p}&from-xhr',
				headers=headers,
				body=f'order=product.position.asc&page={p}&from-xhr',
				callback=self.parse_product
			)

	def parse_product(self, response):

		resp = json.loads(response.body)

		products = resp.get('products')

		for product in products:
			print(product.get('url'))
			yield scrapy.Request(
				url=product.get('url'),
				callback=self.parse_cards
			)

	def parse_cards(self, response):
		print('url ***** ', response.url)
		#resp = json.loads(response.body)
		#data = re.findall("var prestashop =(.+?);\n", response.body.decode("utf-8"), re.S)
		data = response.css(
			'#product-details ::attr(data-product)').extract()[0]
		resp = json.loads(data)
		urls = []
		for image in resp.get('cover').get('bySize'):
			urls.append(resp.get('cover').get('bySize').get(image).get('url'))
		
		urls.append(resp.get('cover').get('small').get('url'))
		urls.append(resp.get('cover').get('medium').get('url'))
		urls.append(resp.get('cover').get('large').get('url'))

		print(urls)
		yield {
			'ID': '',
			'Type': '',
			'SKU': resp.get("id_product"),
			'Name': resp.get('name'),
			'Published': '',
			'Is featured?': '',
			'Visibility in catalog': '',
			'Short description': response.css('.product-information > div:nth-child(1) ::text').getall(),
			'Description': response.css('#description > div ::text').getall() ,
			'Date sale price starts': '',#resp.get('date_add'),
			'Date sale price ends': '',#resp.get('date_upd'),
			'Tax status': '',
			'Tax class': '',
			'In stock?': 1 if resp.get('available_now') == "In Stock" else 0,
			'Stock': resp.get('quantity'),
			'Backorders allowed?': '',
			'Sold individually?': '',
			'Weight (lbs)': '',
			'Length (in)': '',
			'Width (in)': '',
			'Height (in)': '',
			'Allow customer reviews?': resp.get('rate'),
			'Purchase note': '',
			'Sale price': resp.get('price'),
			'Regular price': resp.get('price_without_reduction'),
			'Categories': resp.get('category_name'),
			'Tags': '',
			'Shipping class': '',
			'Images': urls,
			'Download limit': '',
			'Download expiry days': '',
			'Parent': '',
			'Grouped products': '',
			'Upsells': '',
			'Cross-sells': '',
			'External URL': resp.get('link'),
			'Button text': '',
			'Position': resp.get("position"),
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
