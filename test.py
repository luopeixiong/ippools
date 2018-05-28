# -*- coding:utf-8 -*-

from Crawler import Spider,Getter
import flask
from multiprocessing import Process
from Dbs import redis_client
from Server import core
from Tester import Tester
from log import logs
from scheduler import Scheduler

if __name__ == '__main__':
    # _cls = Spider.Spider()
    # for func in _cls.CrawlerFunList:
        # func(_cls)
    # Spider.Spider().crawler_89ip()
    Scheduler().run()