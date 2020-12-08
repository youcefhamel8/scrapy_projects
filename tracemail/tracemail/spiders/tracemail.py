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
from scrapy import FormRequest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import string

#from extractionData.items import ExtractiondataItem

#regions > div > div > ul > li > a
class tracemail(Spider):
	name = 'name'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://www.ouedkniss.com/immobilier/vente/',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					'http://www.prenoms-musulmans.com/' 
				   ]

	def parse(self, response):

		for i in response.css('#author_alphabetic2 > ul > li > a ::attr(href)').extract():
			#url = response.url+'2016/02/prenom-musulman-garcon-commencant-par-'+i+'.html'
			#url = response.url+'?char=A'
			absolute_url = response.urljoin(i)
			yield Request(absolute_url, callback=self.parse_pages)

	def parse_pages(self, response):
		annuaire = {}
		names =  response.css('tr > td > p > strong > span::text').extract()

		for name in names:
			sub_name = name.replace('-',',').split(',')
			for name in sub_name:
				if len(name.strip()) > 3 and ('mixte' in name) == False:
					annuaire['name'] = name.strip()
					annuaire['gender'] = 2
			
				yield annuaire 

	



