# coding:utf-8

import configs
from configs import TIMEOUT,HEADERS
import asyncio
import aiohttp



async def async_get(url,timeout):
    '''
    异步抓取
    '''
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url,timeout=timeout,headers=HEADERS) as response:
                content = await response.read()
                return content.decode(configs.APPARENT_ENCODING,'ignore')
        except BaseException as e:
            pass

async def async_post(url,data=bytes(''.encode(configs.APPARENT_ENCODING))):
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data) as response:
            content = await response.read()

# async def aysnc_request(url,params)


def download_many(urls,timeout=configs.TIMEOUT):
    '''
    处理多url下载
    @return: response
    '''
    loop = asyncio.get_event_loop()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(async_get(url, timeout=timeout))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.wait(tasks))
    # 过滤调不正常的response
    return list(filter(lambda x:x,(i.result() for i in result[0])))

def download_many_post(urls):
    loop = asyncio.get_event_loop()
    tasks = []
    for req in urls:
        task = asyncio.ensure_future(async_post(req[0], req[1]))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.wait(tasks))
    return [i.result() for i in result[0]]




