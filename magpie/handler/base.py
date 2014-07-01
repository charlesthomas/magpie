from os import listdir
from os.path import isdir, join

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        kwargs.update(starred_notes=self.get_starred())
        notebook_name = kwargs.get('notebook_name', None)
        if notebook_name is not None:
            kwargs['notes'] = self._notes_list(notebook_name)
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []
        if self.settings.repo is not None and isdir(self.settings.repo) and \
        not kwargs.get('hide_notebooks', False):
            kwargs['notebooks'] = sorted(listdir(self.settings.repo))
        else:
            kwargs['notebooks'] = []
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

    def get_starred(self):
        starred_list = self.get_cookie('starred_notes')
        if starred_list is None:
            return []
        return starred_list.split(',')
