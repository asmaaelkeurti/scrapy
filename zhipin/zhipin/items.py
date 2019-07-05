# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DistrictItem(scrapy.Item):
    district_link = scrapy.Field()
    district_name = scrapy.Field()
