import sys
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from twisted.internet import reactor
from spiders.JobDetailSpider import JobDetailSpider
from spiders.JobSpider import JobSpider
from scrapy.utils.project import get_project_settings
sys.path.append('..')


def f_detail(iteration):
    process = CrawlerProcess(get_project_settings())
    process.crawl(JobDetailSpider)
    process.start()


def f_url(iteration):
    process = CrawlerProcess(get_project_settings())
    process.crawl(JobSpider)
    process.start()


if __name__ == '__main__':
    for i in range(100):
        for x in range(7):
            p = Process(target=f_detail, args=(i,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
        for y in range(2):
            p = Process(target=f_url, args=(i,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
