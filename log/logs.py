# coding:utf-8

__all__ = ('logger',)


import logging
import sys
from configs import LOG_LEVEL
__intance__ = {}


def Logger():
    if not __intance__.get('logger'):
        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger(__name__)
        filter = logging.Filter(__name__)
        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
         

        file_handler = logging.FileHandler("test.log")
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式


        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)  

        # 指定日志的最低输出级别，调用配置文件log 级别
        logger.setLevel(logging.getLevelName(LOG_LEVEL))
        logger.addFilter(filter)
        __intance__['logger'] = logger
    return __intance__['logger']



if __name__ == '__main__':
    # 输出不同级别的log
    logger.debug('this is debug info')
    logger.info('this is information')
    logger.warn('this is warning message')
    logger.error('this is error message')
    logger.fatal('this is fatal message, it is same as logger.critical')
    logger.critical('this is critical message')
    # 移除一些日志处理器
    logger.removeHandler(file_handler)