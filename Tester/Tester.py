# coding:utf-8

from Dbs import redis_client
import aiohttp
import configs
import asyncio
import time
from log import logs
import random
from configs import Random_Test_ENABLE,RandomTestUrl,TEST_URL

logger = logs.Logger()

class Tester(object):
    def __init__(self):
        self.redis = redis_client.OrderSetClient()

    def test_url(self):
        if Random_Test_ENABLE:
            return random.choice(RandomTestUrl)
        return TEST_URL

    async def test_one(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get(self.test_url(), proxy=real_proxy, timeout=configs.TEST_TIME_OUT, headers=configs.HEADERS) as response:
                    if response.status in configs.VALID_STATUS:
                        self.redis.logger.debug('<proxy %s is useable>' % proxy)
                        self.redis.max(proxy)
                    else:
                        self.redis.logger.debug('<proxy %s is unuseable>' % proxy)
                        self.redis.decrease(proxy)
            except BaseException as e:
                self.redis.logger.debug('<proxy %s is unuseable and fail connect>' % proxy)
                self.redis.decrease_dobule(proxy)

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            proxies = self.redis.all()
            for i in range(0, len(proxies), configs.BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+configs.BATCH_TEST_SIZE]
                tasks = [asyncio.ensure_future(self.test_one(proxy)) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(configs.TEST_TIME_OUT)
        except Exception as e:
            print('Test error -->', e.args)
