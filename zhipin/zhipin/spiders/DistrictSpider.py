import scrapy
from ..items import DistrictItem


class DistrictSpider(scrapy.Spider):
    name = "district_url"
    custom_settings = {'ITEM_PIPELINES': {'zhipin.pipelines.DistrictPipeline': 400}}

    start_urls = ['https://www.zhipin.com/job_detail/?query=&city=101020100&industry=&position=%3E']

    def parse(self, response):
        parse_result = list(zip(response.xpath('//div[@class="condition-box"]/dl[2]/dd/a/@href').getall(),
                                response.xpath('//div[@class="condition-box"]/dl[2]/dd/a/text()').getall()))
        for link in parse_result:
            if len(link[0]) > 20:
                district_item = DistrictItem(district_link=response.urljoin(link[0]), district_name=link[1])

                yield dict(district_item)
