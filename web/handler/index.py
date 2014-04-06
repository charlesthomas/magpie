from tornado.web import RequestHandler
# from base import BaseHandler

# class IndexHandler(BaseHandler):
class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')
