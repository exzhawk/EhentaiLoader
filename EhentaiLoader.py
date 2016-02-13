import cPickle
import json
import os

import requests
import tornado.ioloop
import tornado.web
from lxml import etree

base_urls = {
    'test_login': 'http://exhentai.org/',
    'login': 'http://forums.e-hentai.org/index.php?act=Login&CODE=01',
    'login2': 'http://forums.e-hentai.org/index.php',
    'search': 'http://exhentai.org/',
    'thumb_mode': 'http://exhentai.org/?inline_set=dm_t',
}
ua = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
accept = '*/*'
accept_encoding = 'gzip, deflate, sdch'
default_headers = {'user-agent': ua, 'accept': accept, 'accept_encoding': accept_encoding}
cookies = {}
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888',
}


def get_page(url, headers=None, data=None):
    if headers is None:
        headers = default_headers
    else:
        headers.update(default_headers)
    r = requests.get(url=url,
                     cookies=cookies,
                     proxies=proxies,
                     headers=headers,
                     data=data
                     )
    return r


class SearchHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        keyword = self.get_argument('q')
        r = get_page(base_urls['search'],
                     data={"f_artistcg": "1", "f_non-h": "1", "f_gamecg": "1", "f_imageset": "1", "f_cosplay": "1",
                           "f_asianporn": "1", "f_manga": "1", "f_doujinshi": "1", "f_western": "1", "f_misc": "1",
                           "f_apply": "Apply Filter", "f_search": keyword})
        result_posts = []
        tree = etree.HTML(r.text)
        posts = tree.xpath('//div[@class="itg"]/div[@class="id1"]')
        for post in posts:
            thumb_src = post.xpath('./div[@class="id3"]/a/img/@src')[0]
            title = post.xpath('./div[@class="id2"]/a/text()')[0]
            url = post.xpath('./div[@class="id2"]/a/@href')[0]
            pic_count = post.xpath('./div[@class="id4"]/div[@class="id42"]/text()')[0]
            result_posts.append({'thumb_src': thumb_src, 'title': title, 'url': url, 'pic_count': pic_count})
        filtered_result = filter_result(result_posts)
        self.write(json.dumps({'posts': filtered_result}))


def filter_result(posts):
    return posts


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        is_login = False
        try:
            saved_cookies = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'cookies.pkl'), 'rb'))
            r = requests.get(base_urls['test_login'], cookies=saved_cookies, proxies=proxies,
                             headers={'user-agent': ua})
            if r.headers.get('content-type') is not 'image/gif':
                is_login = True
                global cookies
                cookies = dict(saved_cookies)
        except IOError:
            pass
        self.write({'isLogin': is_login})

    def post(self, *args, **kwargs):
        is_login = False
        username = self.get_argument('username')
        password = self.get_argument('password')
        s = requests.Session()
        s.post(base_urls['login'], headers={'user-agent': ua, 'Content-Type': 'application/x-www-form-urlencoded'},
               data={'UserName': username, 'PassWord': password, 'submit': 'Log me in', 'CookieDate': 1,
                     'temporary_https': 'on'}, proxies=proxies)
        s.get(base_urls['login2'], headers={'user-agent': ua}, proxies=proxies)
        s.get(base_urls['test_login'], headers={'user-agent': ua}, proxies=proxies)
        s.get(base_urls['thumb_mode'], headers={'user-agent': ua}, proxies=proxies)
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
