import sys
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from twisted.internet import reactor
from spiders.JobDetailSpider import JobDetailSpider
from scrapy.utils.project import get_project_settings
sys.path.append('..')


def f(iteration):
    print(iteration)
    process = CrawlerProcess(get_project_settings())
    process.crawl(JobDetailSpider)
    process.start()


if __name__ == '__main__':
    for i in range(10):
        p = Process(target=f, args=(i,))
        p.start()
        p.join()
        print('-----------------------done---------------------')
