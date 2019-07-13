import scrapy
import pymongo
from ..items import JobDetailItem


class JobDetailSpider(scrapy.Spider):
    name = "job_detail"

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'ITEM_PIPELINES': {'zhipin.pipelines.JobDetailPipeline': 400}
    }

    def start_requests(self):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['zhipin']

        for d in [doc for doc in db['job_items'].find({"$and": [{"job_description": {"$exists": False}},
                                                      {"request_times": {"$lt": 5}}]}).limit(5000)]:
            db['job_items'].update_one({'_id': d['_id']},
                                       {"$set": {'request_times': d['request_times']+1}},
                                       upsert=False
                                       )
            yield scrapy.Request(url=d['job_link'], callback=self.parse)

    def parse(self, response):
        yield JobDetailItem(
            job_link=response.request.url,
            job_description='\n'.join(response.xpath('//div[@class="detail-content"]/div[1]/div[1]/text()').getall()),
            industry=response.xpath('//div[@class="sider-company"]/p[4]/a/text()').get(),
            human_count=response.xpath('//div[@class="sider-company"]/p[3]/text()').get(),
            company_fullname=response.xpath('//div[@class="detail-content"]//div[@class="name"]/text()').get()
        )
