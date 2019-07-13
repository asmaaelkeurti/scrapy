import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from ..zhipin.spiders.JobSpider import JobSpider
from ..zhipin.spiders.JobDetailSpider import JobDetailSpider
import pymongo


def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['zhipin']

    while True:
        if db['job_items'].count_documents({"$and": [{"job_description": {"$exists": False}}, {"request_times": {"$lt": 5}}]}) > 500:
            run_spider(JobDetailSpider)
        else:
            run_spider(JobSpider)

