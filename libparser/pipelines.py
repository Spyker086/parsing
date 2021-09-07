# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class LibparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        if item['author'] != None:
            item['author'] = item['author'].replace('\n  ', '').replace('\n', '')
        item['name'] = item['name'].replace('\n          ','').replace('\n        ', '')
        if item['price'] != None:
            item['price'] = float(item['price'])
        if item['price_old'] != None:
            item['price_old'] = float(item['price_old'])
        if item['price_dc'] != None:
            item['price_dc'] = float(item['price_dc'])
        item['rating'] = float(item['rating'].replace(',','.'))
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item
