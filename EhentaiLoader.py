import os

import tornado.ioloop
import tornado.web


class APIHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('Hello world')


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
handlers = [
    (r'/', tornado.web.RedirectHandler, {'url': '/index.html'}),
    (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(settings['static_path'], 'favicon.ico')}),
    (r'/api', APIHandler),
    (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path']))
]

if __name__ == '__main__':
    application = tornado.web.Application(handlers, **settings)
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
