# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
import selenium
from time import sleep
from scrapy.selector import Selector

class LeadSpider(scrapy.Spider):
    name = 'apollo'
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://app.apollo.io/',
            wait_time=25,
            callback=self.login)

    def login(self, response):
        username_path = '#o1-input'
        password_path = '#o2-input'

        driver = response.meta['driver']
        login = driver.find_element_by_css_selector(username_path)
        login.send_keys('mlata.ibrahim@gmail.com')
        password = driver.find_element_by_css_selector(password_path)
        password.send_keys('Lead7707$')
        btn = driver.find_element_by_css_selector("#provider-mounter > div > div:nth-child(2) > div > div.zp_3bCpW > div.zp_2I7me > div.zp_oUhHR > form > div.zp_18q8k > div.zp-button.zp_1X3NK.zp_2z1mP")
        btn.click()
        sleep(10)
        # for page in range (1,100):
        yield SeleniumRequest(
            url = f'https://app.apollo.io/#/people?finderViewId=5a205be19a57e40c095e1d5f&page=1&viewMode=explorer&personLocations[]=United%20Kingdom&personTitles[]=software%20engineer&personTitles[]=software%20developer&personTitles[]=data%20analyst&personTitles[]=it%20specialist&personTitles[]=database%20administrator&personTitles[]=data%20scientist&personTitles[]=network%20administrator',
            wait_time=25,
            callback=self.after_login)

    def after_login(self, response):
        driver = response.meta['driver']
        sel = Selector(text=driver.page_source)
        for profile in sel.xpath("//*[contains(@href,'linkedin')]"):
            yield{
                'Linkedin':profile.get(),
                }
        