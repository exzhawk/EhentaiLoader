import cPickle
import json
import os

import requests
import tornado.ioloop
import tornado.web

base_urls = {
    'test_login': 'http://exhentai.org/',
    'login': 'http://forums.e-hentai.org/index.php?act=Login&CODE=01',
    'login2': 'http://forums.e-hentai.org/index.php',
}
ua = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
cookies = {}
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8088',
}


class SearchHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        keyword = json.loads(self.request.body).get('q')


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        is_login = False
        try:
            saved_cookies = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'cookies.pkl'), 'rb'))
            r = requests.get(base_urls['test_login'], cookies=saved_cookies, proxies=proxies)
            if r.headers.get('content-type') is not 'image/gif':
                is_login = True
                global cookies
                cookies = dict(saved_cookies)
        except IOError:
            pass
        self.write({'isLogin': is_login})

    def post(self, *args, **kwargs):
        is_login = False
        user = json.loads(self.request.body)
        username = user.get('username')
        password = user.get('password')
        s = requests.Session()
        s.post(base_urls['login'], headers={'user-agent': ua, 'Content-Type': 'application/x-www-form-urlencoded'},
               data={'UserName': username, 'PassWord': password, 'submit': 'Log me in', 'CookieDate': 1,
                     'temporary_https': 'on'}, proxies=proxies)
        s.get(base_urls['login2'], headers={'user-agent': ua}, proxies=proxies)
        s.get(base_urls['test_login'], headers={'user-agent': ua}, proxies=proxies)
        global cookies
        cookies = dict(s.cookies.get_dict())
        cPickle.dump(cookies, open(os.path.join(os.path.dirname(__file__), 'cookies.pkl'), 'wb'))
        r = requests.get(base_urls['test_login'], cookies=cookies, proxies=proxies)
        if r.headers.get('content-type') is not 'image/gif':
            is_login = True
        self.write({'isLogin': is_login})


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
handlers = [
    (r'/', tornado.web.RedirectHandler, {'url': '/index.html'}),
    (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(settings['static_path'], 'favicon.ico')}),
    (r'/search', SearchHandler),
    (r'/login', LoginHandler),
    (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']))
]

if __name__ == '__main__':
    application = tornado.web.Application(handlers, **settings)
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
