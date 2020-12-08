import requests
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import json
import pandas as pd
from linkedin_api import Linkedin


class linkedin_api(Spider):
	name = 'linkedin_profile'
	start_urls = [
		"https://www.linkedin.com/",
	]
	
	def parse(self,response):
		
		# Authenticate using any Linkedin account credentials
		api = Linkedin('youcef.hamel8@gmail.com', 'youcef1994' )
		df = pd.read_csv('/Users/mac/Documents/dev/scrapy projects/linkedin/linkedin/spiders/data/linkedin_tech.csv',sep=',' )		
		urls_profile = df['Link'].to_list()
		
		for link in urls_profile:
			try:
				profile_id = link.split('/in/')[-1]
				profile = api.get_profile(profile_id)
				#print(profile_id)


				yield {
					'data': profile,
				} 

			except Exception as e:
				print("Wrong ID ", e)
		