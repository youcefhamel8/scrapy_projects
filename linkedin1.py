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
from scrapy_splash import SplashRequest

from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import timeit

from multiprocessing import Pool
import csv
import json

#scrapy shell 'http://localhost:8050/render.html?url=https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin/page-with-javascript.html&timeout=10&wait=0.5'
#regions > div > div > ul > li > a

class linkedin(Spider):
	name = 'linkedin1'
	login_url = 'https://www.linkedin.com/login'
	#allowed_domains = ['ouedkniss.com']
	start_urls = ['https://www.linkedin.com/login']
	driver = webdriver.Chrome('./chromedriver')
	data = []
	def login(self):
		email = "youcef.hamel8@gmail.com"
		password = "ikram1994"
		actions.login(self.driver, email, password) # if email and password isnt given, it'll prompt in terminal
		#print(self.driver.page_source)
		self.driver.current_window_handle
	    
		"""
	    person2 = Person(   linkedin_url="https://www.linkedin.com/in/zahia-meraihi-8a3091193", 
	                        driver=driver, 
	                        name=None, 
	                        about=[], 
	                        experiences=[], 
	                        educations=[], 
	                        interests=[], 
	                        accomplishments=[], 
	                        company=None, 
	                        job_title=None,  
	                        scrape=True,
	                        close_on_complete=False )
	    """

	def parse(self, response):
		self.login()
		self.search()
		
	def search(self):
		init_url = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22101165590%22%5D&industry=%5B%2296%22%2C%224%22%2C%225%22%5D&keywords=information%20technology&origin=FACETED_SEARCH"
		url = init_url
		nbr_page = 5
		for i in range(2,nbr_page):
			self.driver.get(url)
			sleep(10)
			#profiles = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.artdeco-pagination.ember-view.pv5.ph2')))
			self.driver.implicitly_wait(10)
			profiles = self.driver.find_elements_by_css_selector('.entity-result__title-text.t-16 > a')
			#profiles = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-entity-action-source='actor'] [href]")))
			#print("profiles: ",profiles)
			links = [profile.get_attribute('href') for profile in profiles]
			for link in links:
				print(link)
				self.data.append([link])
			url = init_url+str("&page=")+str(i)
			print("\n\npage ",url)
			
		self.append_csv_file(self.data)
		return links

	def append_csv_file(self, row):
		f = open('profiles.csv', 'a') #w
		with f:
			for r in row:
				writer = csv.writer(f)
				writer.writerow(str(r))

	#title_is
	#title_contains
	#presence_of_element_located
	#visibility_of_element_located
	#visibility_of
	#presence_of_all_elements_located
	#text_to_be_present_in_element
	#text_to_be_present_in_element_value
	#frame_to_be_available_and_switch_to_it
	#invisibility_of_element_located
	#element_to_be_clickable
	#staleness_of
	#element_to_be_selected
	#element_located_to_be_selected
	#element_selection_state_to_be
	#element_located_selection_state_to_be
	#alert_is_present












