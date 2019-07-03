import scrapy
import json


class JobSpider(scrapy.Spider):
    name = "job_url"

    start_urls = ['https://www.zhipin.com/c101020100/a_%E5%BC%A0%E6%B1%9F-b_%E6%B5%A6%E4%B8%9C%E6%96%B0%E5%8C%BA/']

    def parse(self, response):
        job_result = list(zip(response.xpath('//div[@class="job-title"]/text()').getall(),          # title
                              response.xpath('//span[@class="red"]/text()').getall(),               # salary
                              response.xpath('//div[@class="info-primary"]/p/text()[2]').getall(),  # exp_year
                              response.xpath('//div[@class="info-primary"]/h3/a/@href').getall()    # job_link
                              ))

        for link in job_result:
            if len(link[3]) > 20:
                yield {
                    'job_title': link[0],
                    'area_link': response.request.url,
                    'salary': link[1],
                    'exp_year': link[2],
                    'job_link': response.urljoin(link[3])
                }

        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').get()
        if len(next_page) > 20:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
