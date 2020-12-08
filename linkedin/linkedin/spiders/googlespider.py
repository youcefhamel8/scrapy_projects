import requests
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
import json
import pandas as pd


class GoogleSpider(Spider):
	name = 'linkedin'

	headers = {
		'x-rapidapi-key': "5989395367msh09e4a03d87c1386p1160d5jsn389f9b0f866a",
		'x-rapidapi-host': "google-search3.p.rapidapi.com"
	}

	def start_requests(self):
		df = pd.read_csv('/Users/mac/Documents/dev/scrapy projects/linkedin/linkedin/spiders/data/combinaisons_keys_companies.csv',sep=',' )
		keywords = df['keywords'].tolist()
		companies = df['Companies'].tolist()

		for index in range(0, len(keywords)):
			yield scrapy.Request(
				url=f"https://google-search3.p.rapidapi.com/api/v1/search/q={keywords[index]}+{companies[index]}+united+kingdom+site%3Alinkedin.com%2Fin&num=100",
				headers=self.headers,
				callback=self.parse)

	def parse(self, response):
		resp = json.loads(response.body)
		results = resp.get('results')
		for result in results:
			yield {
				'Title': result.get('title'),
				'Link': result.get('link'),
				'Description': result.get('description')
			}
