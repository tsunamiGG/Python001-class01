# -*- coding: utf-8 -*-
import scrapy
from scrapy_maoyan.items import ScrapyMaoyanItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&offset=0']

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}
        cookies = {
            'uuid': '66a0f5e7546b4e068497.1542881406.1.0.0',
            '_lxsdk_cuid': '1673ae5bfd3c8-0ab24c91d32ccc8-143d7240-144000-1673ae5bfd4c8',
            '__mta': '222746148.1542881402495.1542881402495.1542881402495.1',
            'ci': '20',
            'rvct': '20%2C92%2C282%2C281%2C1',
            '_lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorganic',
            '_lxsdk_s': '1674f401e2a-d02-c7d-438%7C%7C35'
        }
        url = 'https://maoyan.com/films?showType=3&offset=0'
        yield scrapy.Request(url, headers=headers, cookies=cookies, callback=self.parse, dont_filter=True)

    def parse(self, response):
        movies = Selector(response=response).xpath("//div[@class='movie-hover-info']")
        for movie in movies[0:10]:
            item = ScrapyMaoyanItem()
            name = movie.xpath('./div[1]/span/text()').extract()
            tag = movie.xpath('./div[2]/text()').extract()[1].strip('\n').strip()
            time = movie.xpath('./div[last()]/text()').extract()[1].strip('\n').strip()
            item.update({'name': name, 'tag': tag, 'time': time})
            yield item
