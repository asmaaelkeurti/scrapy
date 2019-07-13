import scrapy
import datetime
from ..items import JobItem
import pymongo


class JobSpider(scrapy.Spider):
    name = "job_url"
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'ITEM_PIPELINES': {'zhipin.pipelines.JobPipeline': 400}
    }

    def start_requests(self):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['zhipin']

        for d in db['area_items'].find().sort('last_updated_time', pymongo.ASCENDING).limit(1):
            db['area_items'].update_one({'_id': d['_id']},
                                        {"$set": {'last_updated_time': datetime.datetime.now()}},
                                        upsert=False)
            yield scrapy.Request(url=d['area_link'], callback=self.parse)

    def parse(self, response):
        job_result = list(zip(response.xpath('//div[@class="job-title"]/text()').getall(),          # title
                              response.xpath('//span[@class="red"]/text()').getall(),               # salary
                              response.xpath('//div[@class="info-primary"]/p/text()[2]').getall(),  # exp_year
                              response.xpath('//div[@class="info-primary"]/h3/a/@href').getall(),    # job_link
                              response.xpath('//div[@class="company-text"]/h3/a/text()').getall()
                              ))
        district_name = response.xpath('//dd[@class="city-wrapper"]/a[2]/text()').get()
        area_name = response.xpath('//dd[@class="city-wrapper"]/a[3]/text()').get()

        for link in job_result:
            if len(link[3]) > 20:
                yield dict(JobItem(
                    district_name=district_name,
                    area_name=area_name,
                    job_title=link[0],
                    area_link=response.request.url,
                    salary=link[1],
                    exp_year=link[2],
                    job_link=response.urljoin(link[3]),
                    company_name=link[4],
                    request_times=0
                ))

        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').get()
        if (next_page is not None) and (len(next_page) > 20):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
