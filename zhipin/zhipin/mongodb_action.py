import pymongo
import jieba
import psycopg2
import re


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['zhipin']
        self.pg_conn = psycopg2.connect(host="localhost", database="zhipin", user="postgres", password="lwj380279011")

    def how_many_left_to_separate_word(self):
        return self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                   {"words_list": {"$exists": False}}]}).count()

    def separate_words_set(self):
        cursor = self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                     {"words_list": {"$exists": False}}]})
        try:
            while True:
                doc = cursor.next()
                seg_list = jieba.cut_for_search(doc['job_description'])
                words_list = list(set([x for x in seg_list]))
                self.db['job_items'].update_one({'_id': doc['_id']},
                                                {'$set': {'words_list': words_list}}
                                                )
        except StopIteration:
            pass

    def separate_salary(self):
        cursor = self.db['job_items'].find({"$and": [
            {"salary": {"$exists": True}},
            {"salary_lower_bound": {"$exists": False}}
        ]})

        try:
            while True:
                doc = cursor.next()
                re_search = re.search(r'(.*)-(.*)k', doc['salary'], re.I)
                if re_search is None:
                    upper_bound = -1
                    lower_bound = -1
                else:
                    upper_bound = re_search.group(2)
                    lower_bound = re_search.group(1)
                self.db['job_items'].update_one({'_id': doc['_id']},
                                                {'$set': {'salary_lower_bound': lower_bound,
                                                          'salary_upper_bound': upper_bound}}
                                                )

        except StopIteration:
            pass

    def clean_district_name(self):
        # needs to recode
        cursor = self.db['job_items'].find({"district_name": {"$regex": ".* .*"}})

        try:
            while True:
                doc = cursor.next()
                self.db['job_items'].update_one({'_id': doc['_id']},
                                                {'$set': {'district_name': doc['district_name'].replace(" ", "").replace("\n", "")}}
                                                )
        except StopIteration:
            pass

    def create_table(self):
        commands = ["""DROP TABLE job_detail;""",
                   """DROP TABLE job_detail_words""",
            """
            CREATE TABLE job_detail(
	            id VARCHAR(30) PRIMARY KEY,
	            district_name VARCHAR (20),
	            area_name VARCHAR (20),
	            job_title VARCHAR (50),
	            last_updated_time DATE,
	            first_updated_time DATE,
	            company_name VARCHAR (50),
	            company_fullname VARCHAR(50),
	            human_count VARCHAR(50),
	            industry VARCHAR(50),
	            salary_lower_bound INTEGER,
	            salary_upper_bound INTEGER
                );
                    """,
                    """
                    CREATE TABLE job_detail_words(
                        id VARCHAR (30),
                        word VARCHAR (20)
                    );
                    """

                   ]
        cur = self.pg_conn.cursor()
        for c in commands:
            cur.execute(c)
        self.pg_conn.commit()

        cur.close()
        self.pg_conn.commit()

    def clean_job_detail_table(self):
        command = """DELETE FROM job_detail;"""
        cur = self.pg_conn.cursor()
        cur.execute(command)
        cur.close()
        self.pg_conn.commit()

    def insert_job_detail(self):
        mongo_cursor = self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                 {"words_list": {"$exists": True}}]})

        command = """
            INSERT INTO job_detail(id, district_name, area_name, job_title, 
                                  last_updated_time, first_updated_time, company_name, company_fullname, 
                                  human_count, industry, salary_lower_bound, salary_upper_bound)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        mongo_extract = [(str(d['_id']), d['district_name'], d['area_name'], d['job_title'],
                              d['last_updated_time'], d['first_updated_time'], d['company_name'], d['company_fullname'],
                              d['human_count'], d['industry'], d['salary_lower_bound'], d['salary_upper_bound']) for d in mongo_cursor]

        print(len(mongo_extract))
        cur = self.pg_conn.cursor()
        cur.executemany(command, mongo_extract)
        self.pg_conn.commit()
        cur.close()

    def insert_job_detail_words(self):
        mongo_cursor = self.db['job_items'].find({"$and": [{"job_description": {"$exists": True}},
                                                           {"words_list": {"$exists": True}}]})
        command = """
            INSERT INTO job_detail_words(id, word)
            VALUES (%s, %s)
        """
        cur = self.pg_conn.cursor()

        count = 0
        try:
            while True:
                count += 1
                doc = mongo_cursor.next()
                result = [(str(doc['_id']), w) for w in doc['words_list'] if len(w) > 1 and not w.isdigit() and len(w) < 20]
                cur.executemany(command, result)

                if count % 1000 == 0:
                    print(count)
                    self.pg_conn.commit()
        except StopIteration:
            pass

        self.pg_conn.commit()
        cur.close()


if __name__ == '__main__':
    m = Mongo()

    # m.create_table()
    # m.insert_job_detail_words()
    print('table created')
    m.separate_salary()
    print('calculate salary upper and lower bound')
    m.separate_words_set()
    print('separate words')
    m.clean_district_name()
    print('clean district name')

    m.clean_job_detail_table()
    m.insert_job_detail()

