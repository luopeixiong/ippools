

import random


LOG_LEVEL = 'INFO'

# 下载延迟 
TIMEOUT = 3

# 默认Headers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            }
# 页面编码
APPARENT_ENCODING = 'UTF-8'

# redis 设置
REDIS_CONFIG = 'redis://luopx:Haifeng.123@10.1.12.80:6379'

# 存储的redis键
REDIS_KEY = 'proxiespool'

# 有序集合初始化值
INIT_SCORE = 10

# redis有序集合 对应最大分值
MAX_SCORE = 100

# 最小分值 超出则删除
MIN_SCORE = 0

# 每次代理失效, 分值减少
SCORE_DECREASE = 1

# 最大代理数 超过此代理数 crawler处于阻塞状态
MAX_NUMBERS = 5000



RandomTestUrl = ['http://httpbin.org/get']

Random_Test_ENABLE = True
# 测试url
TEST_URL = 'http://httpbin.org/get'

# 测试超时
TEST_TIME_OUT = 8

# 测试 正常状态码
VALID_STATUS = {200}

# 测试 线程
BATCH_TEST_SIZE = 64

# 代理池代理数量
IS_OVER_THRESHOLD = 2000

GETTER_CYCLE = 300

TESTER_CYCLE = 60

TESTER_ENABLED = True

GETTER_ENABLED = True

API_ENABLED = True