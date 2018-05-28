# coding:utf-8

from flask import Flask,g,request, url_for, render_template
from Dbs import redis_client


def get_connect():
    _r = getattr(g, '_r', None)
    if _r is None:
        _r = redis_client.OrderSetClient()
        g._r = _r
    return _r

def create_app():
    app = Flask(__name__)

    @app.route('/get')
    def get_proxy():
        r = get_connect()
        return r.random()

    @app.route('/decrease')
    def decrease():
        ip = request.args.get('ip')
        r = get_connect()
        r.decrease(ip)
        return 'ok'

    @app.route('/count')
    def count():
        r = get_connect()
        return str(r.count())

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

def app():
    app = create_app()
    app.run(host='0.0.0.0', port=5555,debug=False)

if __name__ == '__main__':
    app()