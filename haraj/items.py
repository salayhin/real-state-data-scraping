# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentVilla(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    pictures = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    created_at = scrapy.Field()
    id = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()


