# -*- coding: utf-8 -*-
import scrapy
import json
from proxyspider.items import ProxyspiderItem


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        item = ProxyspiderItem()
        print('response:' + response.text)
        item['ip'] = json.loads(response.text)['origin']
        yield item
