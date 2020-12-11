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

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 500,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'BOT_NAME': 'Googlebot',
    }

    headers = {
        'authority': 'realtime.www.linkedin.com',
        'x-li-accept': 'application/vnd.linkedin.normalized+json+2.1',
        'x-li-track': '{"clientVersion":"1.7.6741","mpVersion":"1.7.6741","osName":"web","timezoneOffset":1,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1440,"displayHeight":900}',
        'x-li-lang': 'en_US',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'x-li-page-instance': 'urn:li:page:feed_index_index;1S6M9yD5RP+kJIAnauOD4A==',
        'accept': 'text/event-stream',
        'cache-control': 'no-cache',
        'x-restli-protocol-version': '2.0.0',
        'csrf-token': 'ajax:8962524689042221203',
        'origin': 'https://www.linkedin.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.linkedin.com/',
        'accept-language': 'fr-FR,fr;q=0.9',
        'cookie': 'bcookie="v=2&55cc7a8b-75fa-49f8-8298-ff81d68b1bf0"; bscookie="v=1&20201210204423d862c934-63b9-4594-84ea-9aad522b40a3AQH3ZC9uhFSxgB7hP5Sxqh6z058Ewe5Q"; lissc=1; G_ENABLED_IDPS=google; _ga=GA1.2.1705489116.1607633068; _gid=GA1.2.218022422.1607633068; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=21029690998702922590813418412973811659; liap=true; li_at=AQEDARDmnGgFwvyKAAABdk5qOt0AAAF2cna-3U4AWFgErYs6ZPpbr1kBGp10LrndsHa4LLCnMUrKvwknv0vBIjv8Izb0R9BpImUAYJqQn-rFQkF_tSvz5bN-6NWwqb4XQlSggiFM7FQZSNLBS80VUcOh; JSESSIONID="ajax:8962524689042221203"; lang=v=2&lang=en-us; spectroscopyId=476f06c0-7ccb-4582-a10c-cf52d09d05df; li_sugr=eec85169-07a8-4395-afef-bfd19f8593ef; UserMatchHistory=AQJW6rRyJtMN3AAAAXZOalxBXkRpVgtTWlTbM_pIMve7BMPAKxgbSmR15pRQQWEUUcFIjBz2yj0yY09JvJmqjp9DeRkEwmJ_G4ew-MmWWhYGTQQyDwSccYnwliwg3m6sdX_xP_nw0uSMTWCy2EeJznUaWexrKftdKTOlxcmAtlhNAS9MTF-Ss4DhVsVbY5gvDo_TCeQJDkh4a2wfV1fb0VC_WuWT6vWRKtBGJRNGz1wvjYR4cRHzNxShM0pw0h5tdbiyFXUyoR1uTEv8MOjWr5ySCKBfkw-qfuo8; li_oatml=AQH0L7f7p_hQswAAAXZOal1RxO-rOaC4D9_8Xw-a_xnQDKMrOfwwHvZvXvFTW2EOxtlRC_5tTReUBSN0FQHNYWE2fYUwOVIf; lidc="b=VB76:s=V:r=V:g=2643:u=25:i=1607633362:t=1607634657:v=1:sig=AQHYBA--LfD0_edR6FknGE7FJHDduhWK"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C18607%7CMCMID%7C21527387537517268240830624410403738624%7CMCAAMLH-1608238165%7C6%7CMCAAMB-1608238165%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1607640565s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1601449681',
    }
    

    def parse(self, response):
       
        # Authenticate using any Linkedin account credentials
        api = Linkedin('tanyabansal.ubs@gmail.com', 'nitish7ujm@', cookies={'li_at':'AQEDARDmnGgFwvyKAAABdk5qOt0AAAF2cna-3U4AWFgErYs6ZPpbr1kBGp10LrndsHa4LLCnMUrKvwknv0vBIjv8Izb0R9BpImUAYJqQn-rFQkF_tSvz5bN-6NWwqb4XQlSggiFM7FQZSNLBS80VUcOh'})
        df = pd.read_csv(
            '/Users/mac/Documents/dev/scrapy_projects/linkedin/linkedin/spiders/data/linkedin_tech.csv', sep=',')
        urls_profile = df['Link'].to_list()

        for link in urls_profile:
            try:
                profile_id = link.split('/in/')[-1]
                profile = api.get_profile(profile_id)
                # print(profile_id)
                yield {
                    'data': profile,
                }

            except Exception as e:
                print("Wrong ID ", e)
