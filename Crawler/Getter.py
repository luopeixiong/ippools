
# coding:utf-8


from .Spider import Spider
from Dbs import redis_client
from configs import IS_OVER_THRESHOLD

class Getter(object):

    def __init__(self):
        self.redis = redis_client.OrderSetClient()
        self.spider = Spider()

    def is_over_threshold(self):
        if self.redis.count() >= IS_OVER_THRESHOLD:
            return True
        return False

    def run(self):
        if not self.is_over_threshold():
            for callback in self.spider.CrawlerFunList:
                callback(self.spider)