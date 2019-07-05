import scrapy
from ..items import AreaItem
import pymongo


class AreaSpider(scrapy.Spider):
    name = "area_url"
    custom_settings = {'ITEM_PIPELINES': {'zhipin.pipelines.AreaPipeline': 400}}

    def start_requests(self):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['zhipin']

        for d in db['district_items'].find():
            yield scrapy.Request(url=d['district_link'], callback=self.parse)

    def parse(self, response):
        area_result = list(zip(response.xpath('//div[@class="condition-box"]/dl[3]/dd/a/@href').getall()[1:],
                               response.xpath('//div[@class="condition-box"]/dl[3]/dd/a/text()').getall()[1:]))

        for link in area_result:
            if len(link[0]) > 20:
                yield AreaItem(
                    district_link=response.request.url,
                    area_link=response.urljoin(link[0]),
                    area_name=link[1])

