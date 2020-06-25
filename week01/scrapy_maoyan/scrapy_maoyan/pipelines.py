# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pandas

class ScrapyMaoyanPipeline:
    def process_item(self, item, spider):
        name= item['name']
        tag = item['tag']
        time = item['time']
        output = [f'|{name}|\t|{tag}|\t|{time}|\n\n']
        
        movie = pandas.DataFrame(data=output)
        movie.to_csv('./maoyantop10.csv', mode='a', encoding='utf8',index=False, header=False)