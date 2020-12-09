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

# to interprete -$ scrapy crawl ouedkniss -o ouedkniss.csv
class ouedkniss(scrapy.Spider):
	
	DEFAULT_REQUEST_HEADERS = {
    'referer': 'https://www.ouedkniss.com/'
	}
	
	name = 'ouedkniss'
	start_urls = ['https://www.ouedkniss.com/annonces/index.php?c=immobilier&sc=vente&sc2=&trier=0003&p=3']

	def parse(self, response):
		SET_SELECTOR = '//*[@id="resultat"]'
		for brickset in response.xpath(SET_SELECTOR).css('.annonce') or response.xpath(SET_SELECTOR).css('.annonce_store'):
			ref_selector = 'ul > li.annonce_titre > a ::attr(href)' #divPages > a:nth-child(6)
			url = brickset.css(ref_selector).extract_first()
			#print('----------------- '+str(url)+' -----------------')
			if url:
				req = scrapy.Request( 
					response.urljoin( url ), 
					callback = self.parse_element
				) 
				
				yield req
				#yield scrapy.Request(response.url,                  
                #            cookies={'PHPSESSID': 'xyz'}, callback = self.parse_captcha)
				
	
		NEXT_PAGE_SELECTOR = '#divPages > a:nth-child(7) ::attr(href)' ##divPages > a:nth-child(6) #divPages > a:nth-child(7)
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
		#ex_page = response.request.headers.get('Referer', None)

		if next_page:
			next_url = scrapy.Request(
				response.urljoin(next_page),
				callback = self.parse
			)

			url_tags = dict(parse.parse_qsl(parse.urlsplit(next_url.url).query))			
			yield { 
					'tags ' : url_tags['p'],
					'details ' : next_url
					}

			yield next_url

			#yield scrapy.Request(response.url,                  
            #                 cookies={'PHPSESSID': 'xyz'}, callback = self.parse_captcha)
			
			print('my tags : ',str(url_tags['p']))
			#if str(url_tags['p']) == str('100'):
			#	raise CloseSpider('stoped ')
		


			

	def parse_element(self, response):
		SET_SELECTOR = '#annonce'
		brickset = response.css(SET_SELECTOR)
		title_selector = 'h1 ::text'
		
		details = {}
		label_selector = []
		desc_tags = []
		for i in range(2,10):
			label_tags_selector = '#Description > p:nth-child('+str(i)+') > label ::text'
			desc_tags_selector = '#Description > p:nth-child('+str(i)+') > span ::text'
			#print(label_tags_selector)
			#print(desc_tags_selector)
			if brickset.css(desc_tags_selector):
		
				details['title'] = brickset.css(title_selector).extract_first()
				details[brickset.css(label_tags_selector).extract_first()] = brickset.css(desc_tags_selector).extract_first()
				#print(details)
		
		
		yield details
		#yield scrapy.Request(response.url,                  
        #                     cookies={'PHPSESSID': 'xyz'}, callback = self.parse_captcha)
		
		
	def parse_captcha(self, response):

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
				callback=self.parse)

		yield scrapy.Request( response.request.headers.get('Referer', None).decode("utf-8"),
				callback = self.parse
			)

		yield scrapy.Request( response.url,
				callback = self.parse_element
			)


	def after_captcha(self, response):                                          
		print ('Result:', response.body)
		yield response.url



