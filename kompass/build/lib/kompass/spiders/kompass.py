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
	name = 'kompass'
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
			yield Request(absolute_url, callback = self.parse_ville, meta = {'url': absolute_url,})


	def parse_ville(self, response):
		# process next page
		#print('-->   ',response.url)
		pages = response.css('.paginatorDivId > li > a ::attr(href)').extract()
		indexs = [1]
		for page in pages:
			page_tb = page.split('/')[6]
			if len(page_tb) > 1:
				index = int(page_tb.split('-')[1])
				indexs.append(index)
	
		index_page_end = max(indexs)
		
		for i in range(1,index_page_end):
			url = response.url+'page-'+str(i)
			#url = response.url+'?char=A'
			absolute_url = response.urljoin(url)
			#yield {'test': absolute_url}
			yield Request(absolute_url, callback=self.parse_entrp)


	def parse_entrp(self, response):
		print('-->   parse_entrp $ ',response.url)
		data = {}
		#titres = response.css('.prod_list > div > h2 > a ::text').extract()
		titres = response.css('.product-list-data > h2 > a ::attr(href)').extract()
		for titre in titres:
			absolute_next_page_url = response.urljoin(titre)
			#data['titre'] = titre
			#data['url_w']= response.url
			#print('------>   ',titre)
			try:
				yield Request(absolute_next_page_url, callback=self.parse_entrp_details)
			except:
				print('javascript exceptions')
			#print(data)
			#yield  data
	
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











