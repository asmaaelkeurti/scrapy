import pymongo
import jieba

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['zhipin']

    def how_many_left_to_separate_word(self):
        return self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                   {"unique_words": {"$exists": False}}]}).count()

    def separate_words_set(self):
        cursor = self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                     {"words_list": {"$exists": False}}]}).limit(1)
        doc = [d for d in cursor][0]
        # doc['_id']
        seg_list = jieba.cut_for_search(doc['job_description'])
        words_list = list(set([x for x in seg_list]))
        self.db['job_items'].update_one({'_id': doc['_id']},
                                        {'$set': {'words_list': words_list}}
                                        )


if __name__ == '__main__':
    m = Mongo()
    for i in range(1000):
        m.separate_words_set()
