import os
import pymongo
import requests
from utils.data_transfer import trans_mongodb_data_to_json

mongo_uri = os.environ.get("mongo_uri") or "mongodb://127.0.0.1:27017/"
base_es_uri = os.environ.get("base_es_uri") or "http://127.0.0.1:9200"
num_list = [1]


def insert_es(data):
    es_url = base_es_uri + "/resume/_doc/%s" % num_list[0]
    trans_mongodb_data_to_json(data)
    res = requests.post(es_url, json=data)
    num_list[0] += 1
    print(res)


def get_mongo_data():
    myclient = pymongo.MongoClient(mongo_uri)
    btp_staging = myclient["btp_staging"]
    resume_table = btp_staging["resume"]
    res = resume_table.find().limit(100)
    for x in res:
        insert_es(x)


get_mongo_data()
