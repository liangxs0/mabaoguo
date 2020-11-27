# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MabaoguoPipeline:

    def __init__(self, mongo_url, mongo_db, mongo_table):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_table = mongo_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_url=crawler.settings.get("MONGO_URI"),
                   mongo_db=crawler.settings.get("MONGO_DB"),
                   mongo_table=crawler.settings.get("MONGO_TABLE"))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]


    def process_item(self, item, spider):
        if item is None:
            return item
        self.db[self.mongo_table].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()