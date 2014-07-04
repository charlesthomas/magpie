from os import listdir
from os.path import isdir, join

import git

from tornado.web import RequestHandler
from urllib import quote_plus, unquote_plus

class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        #if self.application.repo is None:
        #    self._setup()


    #@classmethod
    #def _setup(self):
    def initialize(self):
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
        kwargs.update(starred_notes=self.get_starred())
        notebook_name = kwargs.get('notebook_name', None)
        if notebook_name is not None:
            kwargs['notes'] = self._notes_list(notebook_name)
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []
        #if self.settings.repo is not None and isdir(self.settings.repo) and \
        if self.application.repo is not None and \
        not kwargs.get('hide_notebooks', False):
            kwargs['notebooks'] = sorted(listdir(self.settings.repo))
        else:
            kwargs['notebooks'] = []
        notebookclean = []
        for n in kwargs['notebooks']:
            notebookclean.append(self._decode_notename(n))
        kwargs['notebooks'] = notebookclean
        noteclean = []
        for n in kwargs['notes']:
            noteclean.append(self._decode_notename(n))
        kwargs['notes'] = noteclean
        super(BaseHandler, self).render(template, **kwargs)

    def _notes_list(self, notebook_name):
        path = join(self.settings.repo, notebook_name)
        notes = sorted([n.split('/')[1] for n in self.get_starred() if
                        n.startswith(notebook_name)])
        notes += sorted([n for n in listdir(path) if not n.startswith('.') and \
                         n not in notes])
        return notes

    def _highlight(self, text, highlight):
        return text.replace(highlight,
                            "<font style=background-color:yellow>%s</font>" % \
                            highlight)

    def get_current_user(self):
        if self.settings.username is None and self.settings.pwdhash is None \
        or self.settings.username == '' and self.settings.pwdhash == '':
            return True

        return self.get_cookie('session', '') == self.settings.session

    def _encode_notename(self, name):
        name = name.replace(' ', '+')
        return quote_plus(name.encode('utf8'), '+')

    def _decode_notename(self, name):
        return unquote_plus(name.encode('utf8'))

    def get_starred(self):
        starred_list = self.get_cookie('starred_notes')
        if starred_list is None:
            return []
        return starred_list.split(',')
