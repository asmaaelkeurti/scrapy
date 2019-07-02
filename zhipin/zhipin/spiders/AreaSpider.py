import scrapy
import json


class AreaSpider(scrapy.Spider):
    name = "area_url"

    def start_requests(self):
        with open("district_link.json", 'r') as f:
            urls = [link['district_link'] for link in json.load(f)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        area_result = list(zip(response.xpath('//div[@class="condition-box"]/dl[3]/dd/a/@href').getall()[1:],
                               response.xpath('//div[@class="condition-box"]/dl[3]/dd/a/text()').getall()[1:]))

        for link in area_result:
            if len(link[0]) > 20:
                yield {
                    'district_link': response.request.url,
                    'area_link': response.urljoin(link[0]),
                    'area': link[1]
                }
