# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime


class DistrictPipeline(object):

    collection_name = 'district_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URi'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].remove({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class AreaPipeline(object):

    collection_name = 'area_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URi'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['last_updated_time'] = datetime.datetime.now()
        item['district_name'] = self.db['district_items'].find_one({"district_link": item['district_link']})['district_name']

        result = self.db[self.collection_name].find_one({'area_link': item['area_link']})
        if result is None:
            item['first_updated_time'] = datetime.datetime.now()
            self.db[self.collection_name].insert_one(dict(item))
        else:
            self.db[self.collection_name].update_one({'_id': result['_id']},
                                                     {"$set": {'last_updated_time': item['last_updated_time']}},
                                                     upsert=False)
        return item


class JobPipeline(object):

    collection_name = 'job_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URi'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['last_updated_time'] = datetime.datetime.now()
        result = self.db[self.collection_name].find_one({'job_link': item['job_link']})

        if result is None:
            item['first_updated_time'] = datetime.datetime.now()
            self.db[self.collection_name].insert_one(dict(item))
        else:
            self.db[self.collection_name].update_one({'_id': result['_id']},
                                                     {"$set": {'last_updated_time': item['last_updated_time']}},
                                                     upsert=False)
        return item
