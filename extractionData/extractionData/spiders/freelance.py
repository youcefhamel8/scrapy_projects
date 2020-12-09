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


class freelance(Spider):
	name = 'freelance'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://lawyers.findlaw.com/lawyer/stateallcities/arizona',
					'https://lawyers.findlaw.com/lawyer/stateallcities/california',
					'https://lawyers.findlaw.com/lawyer/stateallcities/nevada',
					'https://lawyers.findlaw.com/lawyer/stateallcities/illinois' 
				   ]

	def parse(self, response):
		#captcha_url = 'https://www.ouedkniss.com/captcha/'
		#if str(response.url) == captcha_url:
		#	yield Request(url, callback=self.parse_captchad,
		#			errback=self.parse_fail)
		
		annonces = response.css('body > div.directory-pages > section > div.medium-10.medium-centered.large-9.large-uncentered.columns > div:nth-child(4) > div > div > a ::attr(href)').extract()
		#body > div.directory-pages > section > div.medium-10.medium-centered.large-9.large-uncentered.columns > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > a
		#body > div.directory-pages > section > div.medium-10.medium-centered.large-9.large-uncentered.columns > div:nth-child(4) > div:nth-child(3) > div:nth-child(89) > a
		for annonce in annonces:
			absolute_url = response.urljoin(annonce)
			#yield {'from url ': response.url}
			yield Request(absolute_url, callback=self.parse_calog)
	
	def parse_calog(self, response):
		
		annonces = response.css('body > div.directory-pages > section > div.medium-10.medium-centered.large-9.large-uncentered.columns > div:nth-child(4) > ul > h3 > a ::attr(href)').extract()
		annonces_a = response.css('body > div.directory-pages > section > div.medium-10.medium-centered.large-9.large-uncentered.columns > div:nth-child(4) > ul > li > a ::attr(href)').extract()
		for annonce in annonces or annonces_a:
			absolute_url = response.urljoin(annonce)
			#yield {'from url ': response.url}
			yield Request(absolute_url, callback=self.parse_annonce, meta={	'state': response.url.split('/')[5],
																			'city' : response.url.split('/')[6],
																			'categ': annonce.split('/')[3]} )

		# process next page
		next_page_url = response.css('#dynamic_results_nav > div > ul > li.pagination-next > a ::attr(href)').extract_first() 
		absolute_next_page_url = response.urljoin(next_page_url)
		#yield {'from url ': response.url}
		yield  Request(absolute_next_page_url)

	def parse_annonce(self, response):
		annonces = set(response.css('.directory_profile ::attr(href)').extract())
		for annonce in annonces:
			absolute_url = response.urljoin(annonce)
			#yield {'from url ': response.url}
			yield Request(absolute_url, callback=self.parse_details, meta={	'from url' : response.url,
																			'state': response.meta['state'],
																			'city' : response.meta['city'],
																			'categ': response.meta['categ']} )

	def parse_details(self, response):
		annonces = response.css('#panel2 > div > div > div:nth-child(4) > div')
		details = {}
		details['state'] = response.meta['state']
		details['city'] = response.meta['city']
		details['categ'] = response.meta['categ']
		details['from url'] = response.meta['from url']
		details['url'] = response.url
		details['name'] = response.css('.listing-details-header ::text').extract_first()
		details['firm_name'] = response.css('h2 ::text').extract_first()
		details['addresse'] =  " ".join(str(x) for x in response.css('.pp_card_street > span ::text').extract())
		details['phone'] = " ".join(str(x) for x in response.css('.profile-phone-body ::text').extract())
		details['fax'] = " ".join(str(x) for x in response.css('li[itemprop=faxNumber] ::text').extract())
		details['website'] = response.css('.profile-website-body ::text').extract_first()
		
		yield details

		

