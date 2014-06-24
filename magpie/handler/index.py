from os.path import isdir

#from sh import ErrorReturnCode_128
import git

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
        else:
            try:
                self.application.repo = git.Repo(self.settings.repo)
            except git.exc.InvalidGitRepositoryError as e:
                config_problem = {'type': 'danger',
                                  'message': ('Your "repo" (%s) is not a '
                                              'valid git repository' % \
                                              self.settings.repo)}
            except git.exc.NoSuchPathError as e:
                config_problem = {'type': 'danger',
                                  'message': ('Your "repo" setting (%s) is not a '
                                              'valid directory' % \
                                              self.settings.repo)}


        if config_problem is None:
            if self.settings.username is None or self.settings.pwdhash is None \
            or self.settings.username == '' or self.settings.pwdhash == '':
                config_problem = {'type': 'warning',
                                  'message': ("It looks like you don't have a "
                                              "username and password set. It's "
                                              "not required, but it's "
                                              "recommended.")}
        self.render('index.html', config_problem=config_problem)
