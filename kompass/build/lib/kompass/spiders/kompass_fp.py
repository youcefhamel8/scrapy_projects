# -*- coding: utf-8 -*-
from scrapy import Spider

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import time
#import dask.dataframe as dd
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
                                                           
from scrapy.http import Request
#from bs4 import BeautifulSoup

from scrapy_splash import SplashRequest

#from extractionData.items import ExtractiondataItem

#regions > div > div > ul > li > a
class kompass(Spider):
	name = 'kompass_fp'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://www.ouedkniss.com/immobilier/vente/',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					'https://dz.kompass.com/' 
				   ]


	def parse(self, response):
		
		villes = response.css('#regions > div > div > ul > li > a::attr(href)').extract()
		for ville in villes:
			absolute_url = response.urljoin(ville)
			#urls.append({'from url ': response.url ,'url' : absolute_url})
			#yield { 'ville' : ville }
			yield Request(absolute_url, callback = self.parse_entrp, meta = {'url': absolute_url,})


	def parse1(self, response):
		print('-->   parse_ville $ ',response.url)
		#pages = response.css('.paginatorDivId > li > a ::attr(href)').extract()
		url = response.url
		absolute_url = response.urljoin(url)
		yield Request(absolute_url, callback=self.parse_entrp)
		#yield {'url': response.url, 'data': SplashRequest(absolute_url, callback=self.parse_entrp_details)}


	def parse_entrp(self, response):
		print('-->   parse_entrp $ ',response.url)
		#titres = response.css('.product-list-data > h2 > a ::attr(href)').extract_first()
		titres = response.xpath('//*[@class="product-list-data"]/h2/a/@href').extract()
		#print(titres)
		for titre in range(1,len(titres)-1):
			absolute_url = response.urljoin(titres[titre])
			yield Request(absolute_url, callback=self.parse_entrp_details)
		#absolute_next_page_url = response.urljoin(titres)
		#for titre in titres:
			#yield SplashRequest(titre, callback=self.parse_entrp_details)
		#yield {'url': response.url, 'data': Request(absolute_next_page_url, callback=self.parse_entrp_details)}

	
	def parse_entrp_details(self, response):
		print('-->   parse_entrp_details $ ',response.url)
		details = {}
		details['LastUpdate'] = response.css('*[id=lastUpdate] > span ::text').extract_first()
		details['Name'] = response.css('.blockNameCompany > h1 ::text').extract_first().strip()
		details['Wilaya'] = response.css('span[itemprop="name"] ::text').extract_first()
		details['Address'] = self.format_clean(response.css('.blockAddress > span:nth-child(2) ::text').extract())
		details['Faxnumber'] = str(response.css('.faxNumber ::text').extract_first()).strip()
		details['Banque'] = response.css('.blockInfoGenerales > div > div > p ::text').extract()
		details['ImportZones'] = response.css('*[id="importZones"] ::text').extract()
		details['ImportCountries'] = response.css('*[id="importCountries"] ::text').extract()
		details['Dirigeants'] = response.css('.executiveName ::attr(title)').extract()
		details['Resume'] = response.css('*[itemprop="description"] ::text').extract_first()
		details['Phone'] = response.css('.freePhoneNumber-hiconnect ::text').extract()
				
		for i in range(1,10):
			if response.css('tr:nth-child('+str(i)+') > th ::text').extract():
				details[response.css('tr:nth-child('+str(i)+') > th ::text').extract_first()] = response.css('tr:nth-child('+str(i)+') > td ::text').extract_first()
		
		details['Cat1'] = response.css('.activitiesTree > ul > li >  a ::text').extract()
		details['Cat2'] = response.css('.activitiesTree > ul > li > ul > li > a  ::text').extract()

		#print('------>   ',details)
		return details

	def format_clean(self, data):
		#print('debut', data)
		res = []
		for i in data:
			isstr = False
			for j in i:
				if j.isalpha():
					isstr = True
					break
			if isstr != False:
				res.append(i.strip())
		#print('debut', data)
		return res

	def is_data(self, data):
		for i in data:
			if i.isalpha():
				return True
		return False






