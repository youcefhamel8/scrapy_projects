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
class lkeria(Spider):
	name = 'lkeria'
	#allowed_domains = ['ouedkniss.com']
	start_urls = [	
					#'https://www.ouedkniss.com/immobilier/vente/',
					#'https://www.ouedkniss.com/immobilier/vente/2',
					#'https://www.ouedkniss.com/immobilier/vente/3',
					'https://www.lkeria.com/annonces/immobilier/' 
				   ]

	def parse(self, response):
		url_tags = response.url+'bien-P'
		
		for i in range(1,256):
			print(str(i))
			next_url = url_tags+str(i)
			yield Request(next_url, callback=self.parse_pages, meta = {'url_source': next_url} )
			#yield {'url_source': next_url}

	def parse_pages(self, response):
		annonces = response.css('.property-title > a ::attr(href)').extract()
		for annonce in annonces:
			absolute_url = response.urljoin(annonce)
			#yield {'url_source' : response.meta['url_source'],'url' : absolute_url}
			yield Request(absolute_url, callback = self.parse_details)

# #fResultat_location > div:nth-child(14) > div > div.noo-mainbody-inner > div:nth-child(3) > div.noo-content.col-xs-11.col-md-7 > div > div > div.properties-content > article:nth-child(2) > div.property-wrap > div.property-title.hidden-xs > a
#[itemprop="Address"]
	def parse_details(self, response):
		# process next page
		#print('-->   ',response.url)
		
		details = {}

		details['url'] =response.url
		
		try :
			l = response.css('li[itemprop="itemListElement"] > a > span::text').extract()
			del l[0]
			details['categorie'] = l
		except :
			print("An exception occurred")

		try :
			l = response.css('li[itemprop="itemListElement"] > a > span::text').extract()
			del l[0]
			details['categorie_str'] = ' '.join( str(elem).strip() for elem in l)
		except :
			print("An exception occurred")	
		
		try : 
			details['lieu'] = ' '.join( str(elem) for elem in response.css('.titre > span::text').extract_first().split() )
		except:
			details['lieu'] = "Null"
			print("An exception occurred")
		
		try : 
			details['prix'] = response.css('.prix-resume > b::text').extract_first()
		except:
			details['prix'] = "Null"
			print("An exception occurred")
		
		try : 
			details['prix_offre'] = response.css('span[itemprop="price"] > b::text').extract_first().strip()
		except:
			details['prix_offre'] = "Null"
			print("An exception occurred")
		
		try : 
			details['ref'] = response.css('div.row > div:nth-child(2) > div.g-row.droit.col-sm-12.col-md-6 ::text').extract_first().strip()
		except:
			details['ref'] = "Null"
			print("An exception occurred")
		
		try : 
			details['nbr_pieces'] = response.css('.resume > li ::text').extract()[2]
		except:
			details['nbr_pieces'] = "Null"
			print("An exception occurred")
		
		try : 
			details['superf'] = response.css('.resume > li ::text').extract()[0]
		except:
			details['superf'] = "Null"
			print("An exception occurred")
		
		try : 
			details['desc'] = (' '.join( str(elem).strip() for elem in response.css('section[itemprop="description"]::text').extract())).replace(',',' ')
		except:
			details['desc'] = "Null"
			print("An exception occurred")
		
		try : 
			details['num'] = response.css('div.noo-sidebar.noo-sidebar-right.col-xs-12.col-md-4 > div > div > div > div > div > article > div > div > div > div ::text').extract()[0]
		except:
			details['num'] = "Null"
			print("An exception occurred")
		
		try : 
			details['num2'] =response.css('div.noo-sidebar.noo-sidebar-right.col-xs-12.col-md-4 > div > div > div > div > div > article > div > div > div > div ::text').extract()[1]
		except:
			details['num2'] = "Null"
			print("An exception occurred")

		yield details
#		return details








