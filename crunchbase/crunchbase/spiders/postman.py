#! /usr/bin/env python3
# coding: utf-8

import requests
from scrapy.selector import Selector

def get_response_text(url):

    payload = {'cid': 'CiinPl%2FTh3VUTgAoBm9NAg%3D%3D',
               '__cflb': '0H28vxzrpPtLNGTtMKpMQFkN8w7hro2Eycfyv1Ud7Rn',
               '__cfduid': 'd1dcb4b1466fb29bc8f6a8b3d56ce6aac1607698411',
               '_pxhd': 'a1f861484a811306580081a432d3462d1e8ec8dee5806ad3b8cde2e3c9ef6d1b%3Ac1a2cb41-3bd0-11eb-9846-7962d424d873'}
    files = [

    ]

    path = url.split('.com')[-1]
    headers = {
        'authority': 'www.crunchbase.com',
        'method': 'GET',
        'path': path,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr-FR,fr;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '__cfduid=daec7ceedc59f667844b11e1b62050e2c1607705334; _pxhd=a1f861484a811306580081a432d3462d1e8ec8dee5806ad3b8cde2e3c9ef6d1b:c1a2cb41-3bd0-11eb-9846-7962d424d873; cid=CiinPl/TovdSvgAnBNb1Ag==; __cflb=0H28vxzrpPtLNGTtMKpMQFkN8w7hro2FsdmBF492Dde; _pxvid=c1a2cb41-3bd0-11eb-9846-7962d424d873; _hp2_props.973801186=%7B%22Logged%20In%22%3Afalse%2C%22Pro%22%3Afalse%2C%22cbPro%22%3Afalse%7D; _ga=GA1.2.1331415483.1607705338; _gid=GA1.2.686451175.1607705338; _hp2_ses_props.973801186=%7B%22r%22%3A%22https%3A%2F%2Fwww.crunchbase.com%2Fperson%2Fjohnny-dolvik-2%22%2C%22ts%22%3A1607705337538%2C%22d%22%3A%22www.crunchbase.com%22%2C%22h%22%3A%22%2Fperson%2Fjohnny-dolvik-2%22%7D; _hp2_id.973801186=%7B%22userId%22%3A%226681439531306223%22%2C%22pageviewId%22%3A%227252824014594962%22%2C%22sessionId%22%3A%225722731265674908%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _px3=e8b7c399bddb0ce7096dfef831237701e786359aa302cd6cfb067459eb89231f:aetK2dFZP1mDRZ/ssh4TeNNZD7OG6lZAEg15kQpXRjN59N4RXIqtPf7zbLheCvZe17NAwoeEFYxW1re4Fn/YiQ==:1000:GjIdnyOXWWRlZ+vtvtN47AZfHwjy1yi6cgM/dzc0T0E5jhMqeC01AejmUOD94o0UpfDImYRbskeYYNeWvBOX+n0CCXnOESsIlHxIkDhi6DbTFKACgr67RTlmEfPfRFAYsjR9x4ConAzg3PCWSPF/L792GU0zI+NN7bRv1cYsXJw=; cid=CiinPl/Th3VUTgAoBm9NAg==; __cflb=0H28vxzrpPtLNGTtMKpMQFkN8w7hro2Eycfyv1Ud7Rn; __cfduid=d1dcb4b1466fb29bc8f6a8b3d56ce6aac1607698411; _pxhd=a1f861484a811306580081a432d3462d1e8ec8dee5806ad3b8cde2e3c9ef6d1b:c1a2cb41-3bd0-11eb-9846-7962d424d873',
        'referer': url,
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    
    html = response.text
    resp = Selector(text = html)
    
    return {
        'title': resp.css('title ::text'),
    }

