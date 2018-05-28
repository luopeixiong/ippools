

from tornado.httpclient import AsyncHTTPClient,HTTPClient
from tornado import ioloop
from tornado.concurrent import Future
from tornado.ioloop import IOLoop
from tornado import gen

def synchrnonous_fetch(url):
    '''
    同步
    '''
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

def parse_body(body):
    print('函数callback')
    print(body)

def asynchrnonous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)
    # 注意此处，需要启动IOLoop实例才能触发回调
    IOLoop.instance().start()

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future

def futrue_callback(res_future):
    print("调用回调函数 Futrue")
    parse_body(res_future._result.body)

def futrues_callback(res_future):
    for response in res_future._result:
        parse_body(response.body)

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield [http_client.fetch(url),http_client.fetch(url)]
    return response

async def fetch_async(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body

if __name__ == '__main__':
    url = 'http://www.baidu.com'
    # res = synchrnonous_fetch(url)
    # parse_body(res)
    # 异步请求，带回调函数
    # res = asynchrnonous_fetch(url, parse_body)

    # # 异步请求，返回Futrue类
    # future = async_fetch_future(url)
    # io_loop = IOLoop.current()
    # io_loop.add_future(future, callback=futrue_callback)
    # io_loop.start()
    # # # 使用协程调用
    # gen_future = fetch_coroutine(url)
    # io_loop = IOLoop.current()
    # io_loop.add_future(gen_future, callback=futrues_callback)
    # io_loop.start()

    # 使用async await关键字
    gen_future = fetch_async(url)
    io_loop = IOLoop.current()
    io_loop.add_future(gen_future, callback=futrue_callback)
    io_loop.start()
