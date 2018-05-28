
import time

from Crawler.Getter import Getter
from Dbs.redis_client import OrderSetClient
from Server.core import app
from Tester.Tester import Tester
from log.logs import Logger
from configs import GETTER_CYCLE,TESTER_CYCLE,TESTER_ENABLED, API_ENABLED, GETTER_ENABLED
from multiprocessing import Process


class Scheduler(object):
    logger = Logger()

    def scheduler_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            self.logger.info('Tester is running...')
            tester.run()
            time.sleep(TESTER_CYCLE)

    def scheduler_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            self.logger.info('Getter is running...')
            getter.run()
            time.sleep(GETTER_CYCLE)

    def schedule_api(self):
        '''
        开启api
        '''
        app()

    def run(self):
        self.logger.info('代理池开始运行')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
