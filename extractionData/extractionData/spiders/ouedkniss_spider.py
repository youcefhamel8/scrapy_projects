# -*- coding: utf-8 -*-
from scrapy import Spider

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

from extractionData.items import ExtractiondataItem


class annonceSpider(Spider):
	name = 'annonce'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://www.ouedkniss.com/immobilier/vente/',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					'https://www.ouedkniss.com/immobilier/vente/2' 
				   ]

	def parse(self, response):
		#captcha_url = 'https://www.ouedkniss.com/captcha/'
		#if str(response.url) == captcha_url:
		#	yield Request(url, callback=self.parse_captchad,
		#			errback=self.parse_fail)
		annonces_stores = response.css('.annonce_store > ul > li.annonce_titre > a ::attr(href)').extract()
		annonces = response.css('.annonce > ul > li.annonce_titre > a ::attr(href)').extract()
		for annonce in annonces_stores or annonces:
			absolute_url = response.urljoin(annonce)
			#yield {'from url ': response.url ,'url' : absolute_url}
			yield Request(absolute_url, callback=self.parse_annonce )

		# process next page
		next_page_url = response.css('#divPages > a:nth-child(5) ::attr(href)').extract_first()
		absolute_next_page_url = response.urljoin(next_page_url)
		yield  Request(absolute_next_page_url)
	

	def parse_annonce(self, response):
		SET_SELECTOR = '#annonce'
		annonce = response.css(SET_SELECTOR)
		title_selector = 'h1 ::text'
		id_selector = '#Description > p:nth-child(1) > a > span ::text'
		other_selector = '#GetDescription ::text'
		price_selector = '#Prix > span ::text'
		echange_selector = '#Echange ::text'
		#price_selector = ''

		details = ExtractiondataItem()
		details['id'] = annonce.css(id_selector).extract_first()
		details['title'] = annonce.css(title_selector).extract_first()
		details['url'] = response.url
		
		description = {}

		for i in range(2,15):
			label_tags_selector = '#Description > p:nth-child('+str(i)+') > label ::text'
			desc_tags_selector = '#Description > p:nth-child('+str(i)+') > span ::text'
			if annonce.css(label_tags_selector):
				description[annonce.css(label_tags_selector).extract_first()] = annonce.css(desc_tags_selector).extract_first()

		description['Echange'] = annonce.css(echange_selector).extract_first()
		description['other_detail'] = str(annonce.css(other_selector).extract())
		details['description'] = description
		details['price'] = annonce.css(price_selector).extract_first()

				
		yield details
