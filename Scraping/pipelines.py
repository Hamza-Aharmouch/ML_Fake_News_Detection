# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import random

class ScrapingProjectPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['News_DB']
        self.collection = db['api_fakenews']


    def process_item(self, item, spider):
        if item.get('details') is not None:
            self.collection.insert(item)
            # if item.get('id') is None:
            #     item['id'] = random.sample(range(500, 3510), 1)
            #     self.collection.insert(item)
        return item



# from scrapy.conf import settings

# class MongoDBPipeline(object):
#
#     def __init__(self):
#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DB']]
#         self.collection = db[settings['MONGODB_COLLECTION']]
