# -*- coding: utf-8 -*-

# Scrapy settings for extractionData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'extractionData'

SPIDER_MODULES = ['extractionData.spiders']
NEWSPIDER_MODULE = 'extractionData.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'extractionData (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 50

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'extractionData.middlewares.ExtractiondataSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'extractionData.middlewares.ExtractiondataDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'extractionData.pipelines.ExtractiondataPipeline': 300,
#}
ITEM_PIPELINES = {'extractionData.pipelines.ExtractiondataPipeline': 300,}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "findlaw"
MONGODB_COLLECTION = "arizona"

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 5
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 50
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOADER_MIDDLEWARES = {
    #'extractionData.middlewares.CustomProxyMiddleware': 350,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    #'scrapy_proxies.RandomProxy': 3000,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    #'extractionData.middlewares.ExtractiondataDownloaderMiddleware': 20000,
    #'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #'rotating_proxies.middlewares.BanDetectionMiddleware': 620,

    #'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    #'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    #'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    #'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    #'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    #'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    #'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    #'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 700,
    #'extractionData.middlewares.CaptchaMiddleware': 543,
    #'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
}

USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
]
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36

#PROXY_LIST = './list.txt'
#ROTATING_PROXY_LIST_PATH = './http-900ms-country_all-anonymity_all-ssl_all-.txt'
#PROXY_MODE = 0
MEMUSAGE_ENABLED = True
#MEMUSAGE_LIMIT_MB = 1000000
DUPEFILTER_DEBUG = False
DEPTH_LIMIT = 6
max_proc_per_cpu = 4
max_proc = 4
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
#REACTOR_THREADPOOL_MAXSIZE = 20





