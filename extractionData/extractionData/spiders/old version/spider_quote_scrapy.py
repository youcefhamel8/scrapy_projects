"""import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import time

# to interprete -$ scrapy crawl ouedkniss -o ouedkniss.csv

class ouedkniss(scrapy.Spider):
	name = 'ouedkniss'
	start_urls = ['https://www.ouedkniss.com/immobilier/vente/2']

	def parse(self, response):
		end = '19 Avril 2018'
		date = ''

		SET_SELECTOR = '//*[@id="resultat"]'
		for brickset in response.xpath(SET_SELECTOR).css('.annonce') or response.xpath(SET_SELECTOR).css('.annonce_store'):

			id_selector = 'ul > li.annonce_text > span.annonce_numero ::text'
			date_selector = 'div.annonce_right > p.annonce_date ::text'
			name_selector = 'ul > li.annonce_titre > a > h2 ::text'
			price_selector = 'ul > li.annonce_text > span.annonce_prix > span ::text'
			desc_selector = 'ul > li.annonce_text > span.annonce_get_description ::text' #ul > li.annonce_text > span.annonce_get_description > br:nth-child(1)

#            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
#            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
#            IMAGE_SELECTOR = 'img ::attr(src)'
			date = brickset.css(date_selector).extract_first()

			yield {
				'id'	: 	brickset.css(id_selector).extract_first(),
				'date'	: 	brickset.css(date_selector).extract_first(),
				'name'	: 	brickset.css(name_selector).extract_first(),
				'price'	: 	brickset.css(price_selector).extract_first(),
				'desc'	: 	brickset.css(desc_selector).extract_first(),
			}
			#if date == end:
			#	break

		#if date != end:
		NEXT_PAGE_SELECTOR = '#divPages > a:nth-child(6) ::attr(href)' ##divPages > a:nth-child(6)
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
		
		if next_page:
			time.sleep(1)
			yield scrapy.Request(
				response.urljoin(next_page),
				callback = self.parse
			)


"""

