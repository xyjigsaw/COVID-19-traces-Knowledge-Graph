# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RouteTrackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    location = scrapy.Field()
    pubtime = scrapy.Field()
    info = scrapy.Field()
    description = scrapy.Field()
    traces = scrapy.Field()
    source = scrapy.Field()

