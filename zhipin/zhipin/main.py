from scrapy.crawler import CrawlerProcess
from zhipin.zhipin.spiders.JobDetailSpider import JobDetailSpider


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(JobDetailSpider)
    process.start() # the script will block here until the crawling is finished

