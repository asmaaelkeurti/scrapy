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
        'http://wapi.http.cnapi.cc/package_balance?neek=74684&appkey=ce326b3d702e6621faf369d061fc6e76&ac=58152')
    response_data = json.loads(response.content)
    return response_data['data']['package_balance']


if __name__ == '__main__':
    while check_ip_balance() > 10:
        for x in range(4):
            p = Process(target=f_detail, args=(x,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
        for y in range(1):
            p = Process(target=f_url, args=(y,))
            p.start()
            p.join()
            print('-------------------------------------------done----------------------------------------------------------------')
        # Ip_Refresh().refresh()
