from os.path import isdir

from sh import ErrorReturnCode_128
from tornado.web import authenticated, RequestHandler

from base import BaseHandler

class IndexHandler(BaseHandler):
    @authenticated
    def get(self):
        config_problem = None
        if self.settings.repo is None:
            config_problem = {'type': 'danger',
                              'message': ('You have not configured the "repo" '
                                          'setting in magpie\'s config.')}
        elif not isdir(self.settings.repo):
            config_problem = {'type': 'danger',
                              'message': ('Your "repo" setting (%s) is not a '
                                          'valid directory' % \
                                          self.settings.repo)}
        else:
            try:
                self.application.git.status()
            except ErrorReturnCode_128 as e:
                if 'Not a git repository' in e.message:
                    config_problem = {'type': 'danger',
                                      'message': ('Your "repo" (%s) is not a '
                                                  'valid git repository' % \
                                                  self.settings.repo)}
                else:
                    raise

        if config_problem is None:
            if self.settings.username is None or self.settings.pwdhash is None \
            or self.settings.username == '' or self.settings.pwdhash == '':
                config_problem = {'type': 'warning',
                                  'message': ("It looks like you don't have a "
                                              "username and password set. It's "
                                              "not required, but it's "
                                              "recommended.")}
        self.render('index.html', config_problem=config_problem)
