# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import time
import dask.dataframe as dd
from scrapy.exceptions import CloseSpider
import random

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

import io                                                                       
#import urllib2  
from urllib.request import urlopen
from urllib import parse                                                                

from PIL import Image                                                           
import pytesseract                                                              
from scrapy.http import Request


class annonceSpider(Spider):
	name = 'annonce'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					'https://www.ouedkniss.com/immobilier/vente',
					'https://www.ouedkniss.com/immobilier/vente/2',
					'https://www.ouedkniss.com/immobilier/vente/3',
					'https://www.ouedkniss.com/immobilier/vente/4' 
				   ]

	def parse(self, response):

		#if response.request.headers.get('Referer'):
		#	print('---------------------- > ' ,response.request.headers.get('Referer'))
		#	Request(response.request.headers.get('Referer').decode("utf-8") , callback=self.parse_captcha)
		#	Request(response.url, callback=self.parse_captcha)
		

		annonces_stores = response.css('.annonce_store > ul > li.annonce_titre > a ::attr(href)').extract()
		annonces = response.css('.annonce > ul > li.annonce_titre > a ::attr(href)').extract()
		for annonce in annonces_stores or annonces:
			absolute_url = response.urljoin(annonce)
			#yield {'from url ': response.url ,'url' : absolute_url}
			yield Request(absolute_url, callback=self.parse_annonce, meta={	'from_url': response.url } )

		# process next page
		next_page_url = response.css('#divPages > a:nth-child(5) ::attr(href)').extract_first()
		absolute_next_page_url = response.urljoin(next_page_url)
		yield  Request(absolute_next_page_url)

	def parse_annonce(self, response):
		if response.request.headers.get('Referer'):
			print('---------------------- > ' ,response.request.headers.get('Referer'))
			yield Request(response.request.headers.get('Referer').decode("utf-8") , callback=self.parse_captcha)
		SET_SELECTOR = '#annonce'
		annonce = response.css(SET_SELECTOR)
		title_selector = 'h1 ::text'
		details = {}
		from_url = response.meta['from_url']

		for i in range(2,10):
			label_tags_selector = '#Description > p:nth-child('+str(i)+') > label ::text'
			desc_tags_selector = '#Description > p:nth-child('+str(i)+') > span ::text'
			if annonce.css(desc_tags_selector):
				details['from_url'] = from_url
				details['title'] = annonce.css(title_selector).extract_first()
				details[annonce.css(label_tags_selector).extract_first()] = annonce.css(desc_tags_selector).extract_first()
				
		yield details

	def parse_captcha(self, response):
		try:
			img_url = response.urljoin(response.css('#captcha_img ::attr(src)').extract_first())
			print('URL IMAGE :   '+img_url)            
			img_bytes = urlopen(img_url).read()                             
			img = Image.open(io.BytesIO(img_bytes))                                 
			captcha = pytesseract.image_to_string(img)                              
			print ('Captcha solved:', captcha)                                        

			yield scrapy.FormRequest.from_response(                                
					response, formdata={'captcha': captcha},                            
					callback=self.parse_annonce)
		except Exception as e:
			print("can't resolve captcha !!!!")

	def after_captcha(self, response):                                          
		print ('Result:', response.body)
		yield response.url



# deuxieme spider utilise une boucle pour parcourir les pages 



class annonceSpider2(Spider):
	name = 'annonce2'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					'https://www.ouedkniss.com/immobilier/vente',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					#'https://www.ouedkniss.com/immobilier/vente/4' 
				   ]

	def parse(self, response):

		#if response.request.headers.get('Referer'):
		#	print('---------------------- > ' ,response.request.headers.get('Referer'))
		#	Request(response.request.headers.get('Referer').decode("utf-8") , callback=self.parse_captcha)
		#	Request(response.url, callback=self.parse_captcha)
		for i in range(505,10000):
			absolute_next_page_url = 'https://www.ouedkniss.com/immobilier/vente/'+str(i)
			yield Request(absolute_next_page_url, callback=self.parse_page)

			if (i % 100) == 0:
				time.sleep(10)

	def parse_page(self, response):
		annonces_stores = response.css('.annonce_store > ul > li.annonce_titre > a ::attr(href)').extract()
		annonces = response.css('.annonce > ul > li.annonce_titre > a ::attr(href)').extract()
		for annonce in annonces_stores or annonces:
			absolute_url = response.urljoin(annonce)
			yield {'from url ': response.url ,'url' : absolute_url}
#			yield Request(absolute_url, callback=self.parse_annonce, meta={	'from_url': response.url } )

	def parse_annonce(self, response):
		if response.request.headers.get('Referer'):
			print('---------------------- > ' ,response.request.headers.get('Referer'))
			yield Request(response.request.headers.get('Referer').decode("utf-8") , callback=self.parse_captcha)
		SET_SELECTOR = '#annonce'
		annonce = response.css(SET_SELECTOR)
		title_selector = 'h1 ::text'
		details = {}
		from_url = response.meta['from_url']

		for i in range(2,10):
			label_tags_selector = '#Description > p:nth-child('+str(i)+') > label ::text'
			desc_tags_selector = '#Description > p:nth-child('+str(i)+') > span ::text'
			if annonce.css(desc_tags_selector):
				details['from_url'] = from_url
				details['title'] = annonce.css(title_selector).extract_first()
				details[annonce.css(label_tags_selector).extract_first()] = annonce.css(desc_tags_selector).extract_first()
				
		yield details

	def parse_captcha(self, response):
		try:
			img_url = response.urljoin(response.css('#captcha_img ::attr(src)').extract_first())
			print('URL IMAGE :   '+img_url)
			#url_opener = urllib2.build_opener()                                     
			#url_opener.addheaders.append(('Cookie', 'PHPSESSID=xyz'))               
			img_bytes = urlopen(img_url).read()                             
			img = Image.open(io.BytesIO(img_bytes))                                 

			captcha = pytesseract.image_to_string(img)                              
			print ('Captcha solved:', captcha)                                        

			yield scrapy.FormRequest.from_response(                                
					response, formdata={'captcha': captcha},                            
					callback=self.parse_annonce)
		except Exception as e:
			print("can't resolve captcha !!!!")

	def after_captcha(self, response):                                          
		print ('Result:', response.body)
		yield response.url
