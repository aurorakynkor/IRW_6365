# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobCountItem(scrapy.Item):
    # define the fields for your item here like:
    website = scrapy.Field()
    keyword = scrapy.Field()
    location = scrapy.Field()
    count = scrapy.Field()
