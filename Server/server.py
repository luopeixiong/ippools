from tornado import web,ioloop
from tornado.httpclient import AsyncHTTPClient,HTTPClient
from tornado.concurrent import futures

SESSION_ID = 1


class MainHandler(web.RequestHandler):
    '''
    根页面
    '''
    def prepare(self):
        '''
        用于调用get post等方法前的初始化处理
        '''

    def get(self):
        self.write("Hello World")

    def on_finish(self):
        '''
        用于请求处理结束后的一些清理工作   
        主要用于 清理对象占用 或者关闭数据库连接等工作
        '''


class SearchHandle(web.RequestHandler):
    '''
    Search请求  获取用户信息
    '''
    def get(self, keywords):
        ip = self.request.remote_ip # 获取用户ip
        host = self.request.host # 获取请求的主机地址
        method = self.request.method # 获取Http请求方法
        uri = self.request.uri # 获取客户端请求的uri完整内容
        path = self.request.path # uri的路径名，不包含查询字符串
        query = self.request.query # uri中的查询字符串
        version = self.request.version # http协议版本
        headers = self.request.headers # 请求头
        body = self.request.body # 请求体
        protocol = self.request.protocol # 请求协议名
        arguments = self.request.arguments # 客户端提交的所有参数 键对应的值为bytes类型  注意转换
        files = self.request.files # 以字典方式表达的客户端上传的文件  每个文件名对应一个HTTPFile
        cookies = self.request.cookies # 客户端提交的Cookie字典
        self.write('ip:{},</br>host:{},</br>method:{},</br>uri:{},</br>path:{},</br>query:{},</br>version:{},</br>\
            headers:{},</br>body:{},</br>protocol:{},</br>arguments:{},</br>files:{},</br>cookies:{}'.format(
            ip, host, method ,uri, path, query,version,headers,body, protocol,arguments, files, cookies))

class SetHeader(web.RequestHandler):
    '''
    设置请求头
    '''
    def get(self):
        self.set_header('NUMBER', 9)
        self.set_header('LANGUAGE', 'France')
        self.set_header('LANGUAGE', 'Chinese')

class SetStatus404(web.RequestHandler):
    '''
    状态码设置
    '''
    def get(self):
        self.set_status(400,'never')

class SetCookie(web.RequestHandler):
    '''
    Cookie设置
    '''
    def get(self):
        self.set_cookie('session', 'session')

class GetSession(web.RequestHandler):
    def get(self):
        global SESSION_ID
        if not self.get_secure_cookie("session"):
            self.set_secure_cookie("session", str(SESSION_ID))
            SESSION_ID = SESSION_ID + 1
            self.write('your session got a new one')
        else:
            self.write('your session was set')

settings = {'cookie_secret':"Artio", # session 加盐
        'xsrf_cookies':True, # 防范跨站共计   并在template模板内加入 {% module xsrf_form_html() %}  
        'debug':True, # 调试模式
        'static_path': os.path.join(os.path.dirname(__file__), 'static'), # 配置静态文件
        
            }
def make_app():
    return web.Application(
        [(r'/',MainHandler),
        (r'/search/([^\/]+)',SearchHandle),
        (r'/404',SetStatus404),
        (r'/setheader',SetHeader),
        (r'/setcookie', SetCookie),
        (r'/session',GetSession),
        ],
        **settings
        )



def main():
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()