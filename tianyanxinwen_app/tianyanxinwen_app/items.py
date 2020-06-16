# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanxinwenAppItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    time = scrapy.Field()
    img_list = scrapy.Field()
    content = scrapy.Field()
