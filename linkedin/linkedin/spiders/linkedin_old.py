# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector

#import dask.dataframe as dd
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.http import Request
from scrapy_selenium import SeleniumRequest

import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import timeit

from multiprocessing import Pool
import csv


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

    # ID = "id"
    # XPATH = "xpath"
    # LINK_TEXT = "link text"
    # PARTIAL_LINK_TEXT = "partial link text"
    # NAME = "name"
    # TAG_NAME = "tag name"
    # CLASS_NAME = "class name"
    # CSS_SELECTOR = "css selector"

class linkedin1(Spider):
    
    name = 'linkedin1'
    def start_requests(self):
        
        username_path = '#o1-input'

        yield SeleniumRequest(
            url = 'https://app.apollo.io/?#/login',
            wait_time=30,
            wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, username_path )),
            callback = self.login)

    def login(self, response):
        driver = response.meta['driver']
        print('\n\nConnexion etablie ...\n\n')
        # Path
        username_path = '#o1-input'
        password_path = '#o2-input'
        btn_path = '#provider-mounter > div > div:nth-child(2) > div > div.zp_3bCpW > div.zp_2I7me > div.zp_oUhHR > form > div.zp_18q8k > div.zp-button.zp_1X3NK.zp_2z1mP'

        # Login session
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, username_path ))).send_keys("youcef.hamel8@gmail.com")
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_path ))).send_keys("youcef1994")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn_path ))).click()
        sleep(5)
        card_path = '.zp_ggEA-.zp_3Yrzy.zp_1OBhZ.zp_36VLh.zp_2VU0v.zp_1Afi-.zp_2UWj3'
        #for page in range (1,100): 
        yield SeleniumRequest(
            url = 'https://app.apollo.io/#/people?finderViewId=5a205be19a57e40c095e1d5f&page=1&viewMode=explorer&personLocations[]=United%20Kingdom&personTitles[]=software%20engineer&personTitles[]=software%20developer&personTitles[]=data%20analyst&personTitles[]=it%20specialist&personTitles[]=database%20administrator&personTitles[]=data%20scientist&personTitles[]=network%20administrator',
            wait_time=30,
            callback=self.after_login)
    
    def after_login(self, response):
        sleep(5)
        driver = response.meta['driver']
        print("TEST DE CONNECTIVITE", response.css("#apollo-drift-chat-container > button ::text").extract())
        card_path = '.zp_ggEA-.zp_3Yrzy.zp_1OBhZ.zp_36VLh.zp_2VU0v.zp_1Afi-.zp_2UWj3'
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, card_path )))
        #profiles_sel = driver.find_element_by_css_selector(card_path)
        #profiles = response.css(card_path).extract()
        name_path = card_path + ' > div > div > div > span'
        profiles_sel = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, name_path ))).text
        for profile in profiles_sel:
            #print(profile)
            print('\n\n                     •••••• Res ••••••\n\n')
        yield {
                'test' : profiles_sel,
        }
        """
        for profile in profiles:
            yield{
                'Profile_url':profile.xpath(".//div/div[2]/a/@href").get(),
                'Name':profile.xpath(".//div/div[2]/a/h3/span/span/span[@class='name actor-name']/text()").get(),
                'Title':profile.xpath(".//div/div[2]/p[1]/text()").get(),
                'Area':profile.xpath(".//div/div[2]/p[2]/text()").get(),
                }
        """
        