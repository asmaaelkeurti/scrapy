import scrapy


class DistrictSpider(scrapy.Spider):
    name = "district_url"
    start_urls = ['https://www.zhipin.com/job_detail/?query=&city=101020100&industry=&position=%3E']

    def parse(self, response):
        for link in response.xpath('//div[@class="condition-box"]/dl[2]/dd/a/@href').getall():
            if len(link) > 20:
                yield {
                    'district_link': response.urljoin(link)
                }
