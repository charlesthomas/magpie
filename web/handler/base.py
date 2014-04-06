from os import listdir
from os.path import join

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        path = join(self.settings.repo_root, kwargs['notebook'])
        kwargs['notes'] = listdir(path)
        kwargs['notebooks'] = listdir(self.settings.repo_root)
        super(BaseHandler, self).render(template, **kwargs)
