from os.path import isdir

#from sh import ErrorReturnCode_128

from tornado.web import authenticated, RequestHandler

from base import BaseHandler

class IndexHandler(BaseHandler):
    @authenticated
    def get(self):

        if len(self.application.config_problems) == 0:
            if self.settings.username is None or self.settings.pwdhash is None \
            or self.settings.username == '' or self.settings.pwdhash == '':
                self.application.config_problems.append({'type': 'warning',
                                  'message': ("It looks like you don't have a "
                                              "username and password set. It's "
                                              "not required, but it's "
                                              "recommended.")})
        self.render('index.html', config_problems=self.application.config_problems)
