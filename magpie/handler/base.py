from os import listdir
from os.path import isdir, join

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        if kwargs.get('notebook_name', None) is not None:
            path = join(self.settings.repo, kwargs['notebook_name'])
            kwargs['notes'] = sorted([n for n in listdir(path) if not \
                                      n.startswith('.')])
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []
        if self.settings.repo is not None and isdir(self.settings.repo) and \
        not kwargs.get('hide_notebooks', False):
            kwargs['notebooks'] = sorted(listdir(self.settings.repo))
        else:
            kwargs['notebooks'] = []
        super(BaseHandler, self).render(template, **kwargs)

    def _highlight(self, text, highlight):
        return text.replace(highlight,
                            "<font style=background-color:yellow>%s</font>" % \
                            highlight)
    def get_current_user(self):
        if self.settings.username is None and self.settings.pwdhash is None \
        or self.settings.username == '' and self.settings.pwdhash == '':
            return True

        return self.get_cookie('session', '') == self.settings.session
