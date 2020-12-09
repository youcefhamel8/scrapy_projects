# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy

from PIL import Image                                                           
import pytesseract                                                              
from scrapy.http import Request

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from time import sleep


class ExtractiondataSpiderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		# Called for each response that goes through the spider
		# middleware and into the spider.

		# Should return None or raise an exception.
		return None

	def process_spider_output(self, response, result, spider):
		# Called with the results returned from the Spider, after
		# it has processed the response.

		# Must return an iterable of Request, dict or Item objects.
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Response, dict
		# or Item objects.
		pass

	def process_start_requests(self, start_requests, spider):
		# Called with the start requests of the spider, and works
		# similarly to the process_spider_output() method, except
		# that it doesn’t have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)


class ExtractiondataDownloaderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.

		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		return None

	def process_response(self, request, response, spider):
		# Called with the response returned from the downloader.

		# Must either;
		# - return a Response object
		# - return a Request object
		# - or raise IgnoreRequest
		return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)

"""from w3lib.http import basic_auth_header

class CustomProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta['proxy'] = "https://103.248.41.13:59285"
		request.headers['Proxy-Authorization'] = basic_auth_header(
			'<PROXY_USERNAME>', '<PROXY_PASSWORD>')"""


class CaptchaMiddleware(object):

	max_retries = 5
	
	def process_response(request, response, spider):
		if not request.meta.get('solve_captcha', False):
			return response  # only solve requests that are marked with meta key
		catpcha = find_captcha(response)
		if not captcha:  # it might not have captcha at all!
			return response
		solved = solve_captcha(captcha)
		if solved:
			response.meta['captcha'] = captcha
			response.meta['solved_captcha'] = solved
			return response
		else:
			# retry page for new captcha
			# prevent endless loop
			if request.meta.get('catpcha_retries', 0) == 5:
				logging.warning('max retries for captcha reached for {}'.format(request.url))
				raise IgnoreRequest 
			request.meta['dont_filter'] = True
			request.meta['captcha_retries'] = request.meta.get('captcha_retries', 0) + 1
			return request

	def find_captcha(response):
		 img_url = response.urljoin(response.css('#captcha_img ::attr(src)').extract_first())
		 return img_url

	def solve_captcha(img_url):
		print('URL IMAGE :   '+img_url)
		#url_opener = urllib2.build_opener()                                     
		#url_opener.addheaders.append(('Cookie', 'PHPSESSID=xyz'))               
		img_bytes = urlopen(img_url).read()                             
		img = Image.open(io.BytesIO(img_bytes))                                 

		captcha = pytesseract.image_to_string(img)                              
		print ('Captcha solved:', captcha)                                        

		return scrapy.FormRequest.from_response(                                
			response, formdata={'captcha': captcha},                            
			callback=self.after_captcha)

