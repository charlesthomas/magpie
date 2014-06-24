from os import listdir
from os.path import isdir, join

import git

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        #if self.application.repo is None:
        #    self._setup()


    #@classmethod
    #def _setup(self):
    def initialize(self):
        print "self.application.repo %s" % self.application.repo
        if self.application.repo is None:
            if self.settings.repo is None:
                self.application.config_problems.append({'type': 'danger',
                    'message': ('You have not configured the "repo" '
                        'setting in magpie\'s config.')})

            else:
                try:
                    self.application.repo = git.Repo(self.settings.repo)
                except git.exc.InvalidGitRepositoryError as e:
                    self.application.config_problems.append({'type': 'danger',
                        'message': ('Your "repo" (%s) is not a '
                            'valid git repository' % \
                                    self.settings.repo)})
                except git.exc.NoSuchPathError as e:
                    self.application.config_problems.append({'type': 'danger',
                        'message': ('Your "repo" setting (%s) is not a '
                            'valid directory' % \
                                    self.settings.repo)})


    def render(self, template, **kwargs):
        if kwargs.get('notebook_name', None) is not None:
            path = join(self.settings.repo, kwargs['notebook_name'])
            kwargs['notes'] = sorted([n for n in listdir(path) if not \
                                      n.startswith('.')])
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []
        #if self.settings.repo is not None and isdir(self.settings.repo) and \
        if self.application.repo is not None and \
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
