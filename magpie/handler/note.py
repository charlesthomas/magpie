from os.path import exists, join
from re import search

from magic import Magic
from markdown2 import markdown
from sh import ErrorReturnCode_1
from tornado.web import authenticated

from base import BaseHandler

class NoteHandler(BaseHandler):
    def _delete(self, notebook_name, note_name, confirmed=False):
        path = join(self.settings.repo, notebook_name, note_name)
        dot_path = join(self.settings.repo, notebook_name, '.' + note_name)
        if confirmed:
            self.application.git.rm(path)
            if exists(dot_path):
                self.application.git.rm(dot_path)
            self.application.git.commit('-m', 'removing %s' % path)
            self.redirect('/' + notebook_name)
        else:
            self.render('delete.html', notebook_name=notebook_name,
                        note_name=note_name)

    def _edit(self, notebook_name, note_name, note_contents=None,
              confirmed=False, toggle=False):
        path = join(self.settings.repo, notebook_name, note_name)
        if not confirmed:
            note_contents = open(path).read()
            self.render('note.html', notebook_name=notebook_name,
                        note_name=note_name, note_contents=note_contents,
                        edit=True)
        else:
            if toggle:
                f = open(path)
                tmp = []
                # TODO () in the text seems to break this
                search_string = r'(\[.\])\s(%s)' % note_contents
                for line in f.readlines():
                    regex = search(search_string, line)
                    if regex is not None:
                        old = regex.group(1)
                        if old == '[x]':
                            new = '[ ]'
                        else:
                            new = '[x]'
                        line = "%s %s\n" % (new, regex.group(2))
                    tmp.append(line)
                f.close()
                note_contents = ''.join(tmp)

            f = open(path, 'w')
            f.write(note_contents)
            f.close()

            self.application.git.add(path)
            try:
                if note_contents == '':
                    message = 'creating %s' % path
                else:
                    message = 'updating %s' % path
                self.application.git.commit('-m', message)
            except ErrorReturnCode_1 as e:
                if 'nothing to commit' not in e.message:
                    raise
            self.redirect(note_name)

    def _view_plaintext(self, notebook_name, note_name, highlight=None,
                        dot=False):
        if dot:
            path = join(self.settings.repo, notebook_name, '.' + note_name)
        else:
            path = join(self.settings.repo, notebook_name, note_name)
        note_contents = open(path).read()
        note_contents = markdown(note_contents)
        if highlight is not None:
            note_contents = self._highlight(note_contents, highlight)
        self.render('note.html', notebook_name=notebook_name,
                    note_name=note_name, note_contents=note_contents,
                    edit=False, dot=dot)

    def _view_file(self, notebook_name, note_name):
        path = join(self.settings.repo, notebook_name, note_name)
        with open(path, 'rb') as f:
            self.set_header("Content-Disposition", "attachment; filename=%s" % \
                            note_name)
            self.write(f.read())

    @authenticated
    def get(self, notebook_name, note_name):
        notebook_name = notebook_name.replace('+', ' ')
        note_name = note_name.replace('+', ' ')
        action = self.get_argument('a', 'view')
        if action == 'delete':
            self._delete(notebook_name, note_name, confirmed=False)
        elif action == 'edit':
            self._edit(notebook_name, note_name, confirmed=False)
        else:
            path = join(self.settings.repo, notebook_name, note_name)
            dot_path = join(self.settings.repo, notebook_name, '.' + note_name)
            highlight = self.get_argument('hl', None)
            with Magic() as m:
                mime = m.id_filename(path)
                if 'text' in mime or 'empty' in mime:
                    self._view_plaintext(notebook_name=notebook_name,
                                         note_name=note_name,
                                         highlight=highlight)
                elif exists(dot_path):
                    download = self.get_argument('dl', False)
                    if download:
                        self._view_file(notebook_name=notebook_name,
                                        note_name=note_name)
                    else:
                        self._view_plaintext(notebook_name=notebook_name,
                                             note_name=note_name,
                                             highlight=highlight, dot=True)

                else:
                    self._view_file(notebook_name=notebook_name,
                                    note_name=note_name)

    @authenticated
    def post(self, notebook_name, note_name):
        notebook_name = notebook_name.replace('+', ' ')
        note_name = note_name.replace('+', ' ')
        action = self.get_argument('a', 'view')
        if bool(self.get_argument('save', False)):
            note = self.get_argument('note')
            toggle = self.get_argument('toggle', False)
            self._edit(notebook_name=notebook_name, note_name=note_name,
                       note_contents=note, confirmed=True, toggle=toggle)
        elif bool(self.get_argument('delete', False)):
            self._delete(notebook_name, note_name, confirmed=True)
        else:
            self.redirect(note_name)
