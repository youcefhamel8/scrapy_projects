# -*- coding: utf-8 -*-
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
import re

#from extractionData.items import ExtractiondataItem

#regions > div > div > ul > li > a
class pass_sante(Spider):
	name = 'pass2'
	next_tags = 'following-sibling::*'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://www.ouedkniss.com/immobilier/vente/',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					'https://www.passeportsante.net/fr/Maux/Problemes/Index.aspx' 
				   ]

	def parse(self, response):
		
		maladies = [response.css('.glossary > div > div > ul > li > span > a ::attr(href)').extract()[0]]

		for maladie in maladies:
			absolute_url = response.urljoin(maladie)
			yield SplashRequest(absolute_url, callback = self.parse_maladie, meta = {'url': absolute_url})

	def parse_maladie(self, response):
		
		form = {}
		name = response.url.split('doc=')[1]
		main = response.css('.main_content')
		annuaire = response.css('#tmat > tbody > tr > td > ul > li > a ::attr(href)').extract()
		
		
		for url_id in annuaire:
			absolute_url = response.urljoin(url_id)
			yield SplashRequest(absolute_url, callback = self.parse_by_id, meta = {'titre': absolute_url, 'url_id' : url_id})

	def parse_by_id(self, response):
		
		h = response.xpath("//a[ contains(@name , '"+str(response.meta['url_id']).replace('#','')+"') ] /.. / ..")
		titre = h.xpath('child::*/text()').get()
		next_element = h.xpath(self.next_tags)[0]
		
		while not self.find_tag(next_element, 'h2'):
			print('\n\nparse_by_id ' , next_element)

			if next_element.xpath(self.next_tags):

				if self.find_tag(next_element, 'h3'):
					print("\n\ncondition h3")
					blocs = self.parse_h3_bloc(next_element)
					for bloc in blocs:
						bloc['h2'] = titre
						yield bloc

				elif self.find_tag(next_element, 'p'):
					print("\n\ncondition p")
					blocs = self.parse_h2_bloc(next_element)
					blocs['h2'] = titre
					yield blocs
				
				if next_element.xpath(self.next_tags):
					print("\n\nSTOP")
					next_element = next_element.xpath(self.next_tags)[0]
			else : 
				break
			
			#yield html_dict

	def find_tag(self, next_element, tag):
		if next_element.get().find(tag) == -1:
			return False
		else :
			return True
	
	def parse_h3_bloc(self, next_element):
		tab = []
		html_dict = {}
		
		while not self.find_tag(next_element, 'h2'):
			print('parse_h3_bloc')
			if self.find_tag(next_element, 'h3'):
				html_dict['h3'] = next_element.xpath('self::*/text()').get().strip()
				data = self.get_p(next_element.xpath(self.next_tags)[0])
				html_dict['p'] = data['paragraphe']
				if not data['end']:
					next_element = data['next_element']
					tab.append(html_dict)
				else :
					break
		
		print('\n\nh3')
		return tab
		

	def parse_h2_bloc(self, next_element):
		html_dict = {}
		data = self.get_p(next_element)
		html_dict['p'] = data['paragraphe']
		#html_dict['next_element'] = data['next_element']
		print('\n\nh2')
		return html_dict
		

	def get_p(self, next_element):
		paragraphe = " "
		end = False
		# init
		#next_element = next_element.xpath(self.next_tags)[0]
		
		while next_element.get().find('<p>') != -1 or next_element.get().find('<ul>') != -1 or next_element.get().find('<div') != -1:
			#print('\n\n\nnext_element ',next_element.get(),'\n\n\n')
			# paragraphe
			if next_element.get().find('<ul>') != -1 :
				paragraphe = paragraphe + '\n - ' + '\n - '.join(self.get_ul_list(next_element))
			elif next_element.get().find('<p>') != -1 :
				paragraphe = paragraphe + " --- \n" + next_element.xpath('self::*/text()').get().strip()

			# dernier element
			if next_element.xpath(self.next_tags):
				next_element = next_element.xpath(self.next_tags)[0]
			else:
				#next_element = next_element.xpath(self.next_tags)
				end = True
				break
			print('#get_p >> next_element : ', next_element)

		return {'paragraphe' : paragraphe, 'next_element' : next_element, 'end' : end }

	def get_ul_list(self, next_element):
		next_element = next_element.xpath('.//text()').getall()
		ul = []
		for li in next_element:
			if li.strip():
				ul.append(li.strip().replace(';','; #'))
			#print('next_element ',li)

		str_ul = ' '.join(ul)
		ul = str_ul.split('#')
		#print('\n\n\nget_ul_list ',' '.join(ul),'\n\n\n')
		return ul
		








