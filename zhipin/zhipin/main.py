import sys
import json
import requests
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from twisted.internet import reactor
from spiders.JobDetailSpider import JobDetailSpider
from spiders.JobSpider import JobSpider
from zhipin.IpPoolRefresh import Ip_Refresh
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


def check_ip_balance():
    response = requests.get(
        'http://wapi.http.cnapi.cc/package_balance?neek=74684&appkey=4052ee99c728fc96a399d0dccf2f92e5&ac=57299')
    response_data = json.loads(response.content)
    return response_data['data']['package_balance']


if __name__ == '__main__':
    while check_ip_balance() > 5:
        for x in range(4):
            p = Process(target=f_detail, args=(x,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
        for y in range(8):
            p = Process(target=f_url, args=(y,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
        Ip_Refresh().refresh()
