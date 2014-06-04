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

    def make_cookie(self, name, value, domain=None, expires=None, path='/',
                   expires_days=None, **kwargs):
        '''
        Use make_cookie instead of set_cookie, so that it automatically sets
        regular cookies in debug mode and secure cookies in production mode
        '''
        import logging
        if self.settings.get('debug', False):
            logging.error('setting insecure cookie')
            self.set_cookie(name, value, domain, expires, path, expires_days,
                            **kwargs)
        else:
            logging.error('setting secure cookie')
            self.set_secure_cookie(name, value, **kwargs)

    def fetch_cookie(self, name, default=None):
        '''
        Use fetch_cookie instead of get cookie, so that it automatically gets
        regular cookies in debug mode and secure cookies in production mode
        '''
        if self.settings.get('debug', False):
            cookie = self.get_cookie(name, default)
        else:
            cookie = self.get_secure_cookie(name, default)

        return cookie

    def get_current_user(self):
        if self.settings.username is None and self.settings.pwdhash is None \
        or self.settings.username == '' and self.settings.pwdhash == '':
            return True

        # return self.fetch_cookie('session', '')['value'] == self.settings.session
        return self.fetch_cookie('session', '') == self.settings.session
