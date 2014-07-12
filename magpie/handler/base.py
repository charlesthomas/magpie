from base64 import b64encode, b64decode
from os import listdir, path

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        self.starred_notes = self.get_starred()
        kwargs.update(starred_notes=self.starred_notes)

        notebook_name = kwargs.get('notebook_name', None)
        if notebook_name is not None:
            kwargs['notes'] = self._notes_list(notebook_name)
        else:
            kwargs['notebook_name'] = ''
            kwargs['notes'] = []

        kwargs['notebooks'] = self._notebooks_list(kwargs.get('hide_notebooks',
                                                              False))
        super(BaseHandler, self).render(template, **kwargs)

    def _notebooks_list(self, hide_notebooks=False):
        if self.settings.repo is None or not path.isdir(self.settings.repo) or \
        hide_notebooks:
            return []

        return sorted([self.decode_name(nb) for nb in \
                       listdir(self.settings.repo) if nb != ''])

    def _notes_list(self, notebook_name):
        notes_path = path.join(self.settings.repo,
                               self.encode_name(notebook_name))

        all_notes = [self.decode_name(n) for n in listdir(notes_path) if not \
                     n.startswith('.')]
        starred = []
        unstarred = []

        while all_notes:
            note = all_notes.pop()
            if u'%s/%s' % (notebook_name, note) in self.starred_notes:
                starred.append(note)
            else:
                unstarred.append(note)

        return sorted(starred) + sorted(unstarred)

    def highlight(self, text, highlight):
        return text.replace(highlight,
                            "<font style=background-color:yellow>%s</font>" % \
                            highlight)

    def get_current_user(self):
        if self.settings.username is None and self.settings.pwdhash is None \
        or self.settings.username == '' and self.settings.pwdhash == '':
            return True

        return self.get_cookie('session', '') == self.settings.session

    def encode_name(self, name):
        return name.replace('+', ' ').encode('utf8')

    def decode_name(self, name):
        return name.encode('utf8').replace('+', ' ')

    def get_starred(self):
        starred_list = self.get_cookie('starred_notes')
        if starred_list is None:
            return []
        return b64decode(starred_list).decode('utf8').replace('+', ' ').split(',')
