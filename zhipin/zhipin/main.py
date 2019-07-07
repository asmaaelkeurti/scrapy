from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pymongo


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl('job_detail')
    process.start()
