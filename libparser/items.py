# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LibparserItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    price_dc = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
