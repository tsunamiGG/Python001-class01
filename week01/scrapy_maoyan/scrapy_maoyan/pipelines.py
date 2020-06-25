# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyMaoyanPipeline:
    def process_item(self, item, spider):
        name= item['name']
        tag = item['tag']
        time = item['time']
        output = f'|{name}|\t|{tag}|\t|{time}|\n\n'
        # print(output)
        with open('maoyantop10.text','a+',encoding='utf-8') as article:
            article.write(output)
            return item