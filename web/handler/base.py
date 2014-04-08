from os import listdir
from os.path import join

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        if kwargs.get('notebook_name', None) is not None:
            path = join(self.settings.repo_root, kwargs['notebook_name'])
            kwargs['notes'] = sorted(listdir(path))
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []
        kwargs['notebooks'] = sorted(listdir(self.settings.repo_root))
        super(BaseHandler, self).render(template, **kwargs)

    def _highlight(self, text, highlight):
        return text.replace(highlight,
                            "<font style=background-color:yellow>%s</font>" % \
                            highlight)
