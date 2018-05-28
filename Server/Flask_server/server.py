
from flask import Flask # Application类
from flask import url_for # 路由地址反向生成
from flask import session # session类
from flask import redirect # 重定向
from flask import request
from datetime import datetime

from flask import g # 全局对象类  
from werkzeug.contrib.cache import SimpleCache


def create_app():
    app = Flask(__name__)

    CACHE_TIMEOUT = 300
    app.secret_key = 'Artio'

    cache = SimpleCache()
    cache.timeout = CACHE_TIMEOUT


    @app.before_request
    def return_cached():
        if not request.values:
            response = cache.get(request.path)
            if response:
                print('get page in cache')
                return response


    @app.after_request
    def cache_response(response):
        if not request.values:
            cache.set(request.path, response, CACHE_TIMEOUT)
        return response

    @app.route('/index')
    def _index():
        return 'index'

    def index():
        pass


    def f_book():
        pass

    @app.route('/write_session/')
    def writeSession():
        if session.get('key_time'):
            session['key_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # session.new 是否新建的
            # session.modified 是否被修改
        return session['key_time']

    @app.route('/read_session/')
    def readSession():
        if not session.get('key_time'):
            return redirect(url_for('writeSession'),code=302, Response=None)
        return session['key_time']

    class MyDB():
        def __init__(self):
            print('A db is created')

        def close(self):
            print('A db is closed')

    def get_db():
        db = getattr(g,'_database', None)
        if db is None:
            db = MyDB()
            g._database = db
        return db

    @app.teardown_request
    def teardown_db(response):
        db = getattr(g, '_database',None)
        if db is not None:
            db.close()

    # 路由注册  
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/book/','f_book', f_book)

    with app.test_request_context():
        print(url_for('f_book'), url_for('index'))
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8001,debug=True)