# coding:utf-8

import sys
import redis
import configs
import random
from .error import PoolEmptyError
from log.logs import Logger


SCORE_DECREASE = abs(configs.SCORE_DECREASE)


class BaseClient(object):
    def __init__(self,*args,**kwargs):
        '''
        初始化redis.Rdis对象
        '''
        self.r = redis.StrictRedis.from_url(configs.REDIS_CONFIG)
        self.key = configs.REDIS_KEY
        self.logger = Logger()


class  OrderSetClient(BaseClient):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def add(self, value):
        '''
        向有序集合 添加代理
        '''
        self.logger.info('添加 代理成功 %s' % value) 
        sys.stdout.flush()
        self.r.zadd(self.key, configs.INIT_SCORE, value)

    def exits(self, value):
        '''
        判断代理是否存在,返回bool值 存在==>True
        '''
        return self.r.zscore(self.key, value) != None

    def random(self):
        '''
        若有分值为100的代理 ,则随机从中取一个,若无则随机生成,若代理池为空raise error
        '''
        result = self.r.zrangebyscore(self.key, configs.MAX_SCORE, configs.MAX_SCORE)
        if result:
            return random.choice(result)
        else:
            result = self.r.zrevrange(self.key, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError('proxies pool is empty!')

    def delete(self, value):
        '''
        删除代理
        '''
        self.logger.info('代理失效--->,已经删除 %s' % value)
        sys.stdout.flush()
        self.r.zrem(self.key, value)

    def max(self, value):
        '''
        代理设置问MAX_SCORE
        '''
        self.r.zadd(self.key, configs.MAX_SCORE, value)

    def count(self):
        return self.r.zcard(self.key)

    def decrease(self, value, sep=SCORE_DECREASE):
        score = self.r.zscore(self.key, value)
        if score and score-SCORE_DECREASE>=configs.MIN_SCORE:
            self.r.zincrby(self.key, value, -sep)
        else:
            self.r.zrem(self.key, value)

    def decrease_dobule(self, value, sep=SCORE_DECREASE * 2):
        self.decrease(value, sep)

    def all(self):
        '''
        按分值排序输出所有代理
        '''
        return self.r.zrangebyscore(self.key, configs.MIN_SCORE, configs.MAX_SCORE)


class  UnOrderSetClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, value):
        pass


