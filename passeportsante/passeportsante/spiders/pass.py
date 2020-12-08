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
	name = 'pass'
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


	def parse_maladie__test(self, response):
		# process next page
		#print('-->   ',response.url)
		#container = response.css('#page_contenuFiche_col1').extract()
		#colonnes = response.css('#page_contenuFiche_col1 > h2 ::text').extract()
		#blocs = container[0].split('<h2>')
		#blocs_cleaned = []
		name = response.url.split('doc=')[1]
		print(name)
		details = {}
		details_ids = response.css('#tmat > tbody > tr > td > ul > li > a ::attr(href)').extract()
		details_ids.reverse()
		print(details_ids)
		ex_data = response.xpath( "//a[ contains(@name , 'qui-est-concerne-') ] / ../ ../ following-sibling::*  ").css('p ::text').extract()
		
		details['name'] = name

		precend_data = []
		if details_ids :
			for detail in details_ids:
				detail = detail.replace('#','')
				#les-symptomes-de-l-oedeme-pulmonaire
				path = "//a[ contains(@name , '"+str(detail)+"') ] / ../ ../ following-sibling::*  "
				data = response.xpath(path).extract()
				data_nettoye = self.clean_data(precend_data, data)
				details['titre'] = detail
				details['details'] = " ".join(data_nettoye)
				precend_data = precend_data + data_nettoye
				yield details


		table_traduction = { ord('\t') : ' ', ord('\f') : ' ', ord('\r') : None }
		#for colonne, bloc in zip(colonnes, blocs_cleaned):
		#	details[colonne.strip()] = bloc.strip()
		#details['url'] = response.meta['url']
		#for 
		#details['name'] = response.meta['maladie']
		#details['Fiche'] = ''.join(self.cleanhtml(response.css('#page_contenuFiche_col1').extract()[0]))
		#
		#details['id'] = "0"

	def parse_maladie(self, response):
		form = {}
		name = response.url.split('doc=')[1]

		main = response.css('.main_content')
		
		annaire = response.css('#tmat > tbody > tr > td > ul > li > a ::attr(href)').extract()
		
		h2 = response.xpath("//a[ contains(@name , '"+str(annaire[0]).replace('#','')+"') ] /.. / ..")
		h2_str = h2.xpath('child::*/text()').get()

		
		next_element = h2.xpath(self.next_tags)[0]
		
		while True:
			if next_element.get().find('<h3>') != -1:
				print('next_element :: ', next_element.get())
				form['name'] = name 
				form['h2'] = h2_str
				form['h3'] = next_element.xpath('self::*/text()').get().strip()
				
				res_get_p = self.get_p(next_element)				
				form['p'] = res_get_p['paragraphe']
				next_element = res_get_p['next_element'].xpath('preceding-sibling::*')[-1]

			elif next_element.get().find('<p>') != -1:
				print('P NEXT')
				form['name'] = name 
				form['p'] = h2.xpath(self.next_tags)[0].xpath('following-sibling::*')[0].xpath('self::*/text()').get().strip()

			elif next_element.get().find('<h2>') != -1:
				print('H2 NEXT ELEMENT')
				form['name'] = name 
				form['h2'] = next_element.xpath('child::*/text()').get()
				form['h3'] = 'none'
				
				res_get_p = self.get_p(next_element)				
				form['p'] = res_get_p['paragraphe']
				next_element = res_get_p['next_element'].xpath('preceding-sibling::*')[-1]
				#break
			
			if next_element.xpath(self.next_tags):
				next_element = next_element.xpath(self.next_tags)[0]

			yield form

	def get_p(self, next_element):
		paragraphe = " "
		
		# init
		next_element = next_element.xpath(self.next_tags)[0]
		
		while next_element.get().find('<p>') != -1 or next_element.get().find('<ul>') != -1 or next_element.get().find('<div') != -1:
			print('\n\n\nnext_element ',next_element.get(),'\n\n\n')
			# paragraphe
			if next_element.get().find('<ul>') != -1 :
				paragraphe = paragraphe + '\n - ' + '\n - '.join(self.get_ul_list(next_element))
			elif next_element.get().find('<p>') != -1 :
				paragraphe = paragraphe + " --- \n" + next_element.xpath('self::*/text()').get().strip()

			# dernier element
			if next_element.xpath(self.next_tags):
				next_element = next_element.xpath(self.next_tags)[0]
			else:
				next_element = next_element.xpath(self.next_tags)

		return {'paragraphe' : paragraphe, 'next_element' : next_element }

	def get_ul_list(self, next_element):
		next_element = next_element.xpath('.//text()').getall()
		ul = []
		for li in next_element:
			if li.strip():
				ul.append(li.strip().replace(';','; #'))
			print('next_element ',li)

		str_ul = ' '.join(ul)
		ul = str_ul.split('#')
		print('\n\n\nget_ul_list ',' '.join(ul),'\n\n\n')
		return ul
		

		# next
		# .xpath('following-sibling::*/text()')


		# model
		# response.css('.main_content').css('h2')[0].xpath('following-sibling::h3')[0].xpath('following-sibling::p')[0].get()

		
 
	def cleanhtml(self,raw_html):
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext

	def netoyer_name(self,listName):
		res = []
		for i in listName:
			if i.strip():
				res.append(i.strip())
		return res

	def clean_data(self, precend_data, data):
		if precend_data :
			new_data = data
			for element in precend_data:
				new_data.remove(element)
			return new_data
		return data










