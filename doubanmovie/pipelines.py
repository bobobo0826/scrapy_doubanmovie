# -*- coding: utf-8 -*-
import pymongo
from doubanmovie.items import DoubanmovieItem
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

class MongoDBPipeline(object):
    #Connect to the MongoDB database
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["doubanmovie"]
        self.Movie = db["Movie"]

    def process_item(self, item, spider):
        if isinstance(item, DoubanmovieItem):
            try:
                self.Movie.insert(dict(item))
            except Exception:
                pass
        return item