from tornado.web import RequestHandler
from base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')
