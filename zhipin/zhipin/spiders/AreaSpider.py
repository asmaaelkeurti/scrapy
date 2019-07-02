import scrapy


class AreaSpider(scrapy.Spider):
    name = "area_url"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@class="condition-box"]/dl[2]/dd/a/@href').getall():
            if len(link) > 20:
                yield {
                    'district_link': response.urljoin(link)
                }
