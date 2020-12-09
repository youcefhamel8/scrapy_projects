# -*- coding: utf-8 -*-                                                         
import io                                                                       
#import urllib2  
from urllib.request import urlopen                                                                

from PIL import Image                                                           
import pytesseract                                                              
import scrapy                                                                   


class CaptchaSpider(scrapy.Spider):                                             
    name = 'captcha'                                                            

    def start_requests(self):                                                   
        yield scrapy.Request('https://www.ouedkniss.com/captcha/',                  
                             cookies={'PHPSESSID': 'xyz'}, callback= self.parsesss)                      

    def parse(self, response):

        img_url = response.urljoin(response.css('#captcha_img ::attr(src)').extract_first())
        print('URL IMAGE :   '+img_url)
        #url_opener = urllib2.build_opener()                                     
        #url_opener.addheaders.append(('Cookie', 'PHPSESSID=xyz'))               
        img_bytes = urlopen(img_url).read()                             
        img = Image.open(io.BytesIO(img_bytes))                                 

        captcha = pytesseract.image_to_string(img)                              
        print ('Captcha solved:', captcha)                                        

        req = scrapy.FormRequest.from_response(                                
            response, formdata={'captcha': captcha},                            
            callback=self.after_captcha)
        yield req
        print ()                                        

    def after_captcha(self, response):                                          
        #print ('Result:', response.body)
        yield url