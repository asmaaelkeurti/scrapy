# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DistrictItem(scrapy.Item):
    district_link = scrapy.Field()
    district_name = scrapy.Field()


class AreaItem(scrapy.Item):
    district_link = scrapy.Field()
    area_link = scrapy.Field()
    area_name = scrapy.Field()
    district_name = scrapy.Field()

    first_updated_time = scrapy.Field()
    last_updated_time = scrapy.Field()


class JobItem(scrapy.Item):
    district_name = scrapy.Field()
    area_name = scrapy.Field()

    company_name = scrapy.Field()
    job_title = scrapy.Field()
    area_link = scrapy.Field()
    salary = scrapy.Field()
    exp_year = scrapy.Field()
    job_link = scrapy.Field()
    first_updated_time = scrapy.Field()
    last_updated_time = scrapy.Field()
    request_times = scrapy.Field()


class JobDetailItem(scrapy.Item):
    job_link = scrapy.Field()
    job_description = scrapy.Field()
    industry = scrapy.Field()
    human_count = scrapy.Field()
    company_fullname = scrapy.Field()
