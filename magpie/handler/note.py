from base64 import b64encode, b64decode
from os.path import exists, join
from re import search

from magic import Magic
from markdown2 import markdown
from sh import ErrorReturnCode_1
from tornado.web import authenticated
from tornado.escape import url_escape

from base import BaseHandler

class NoteHandler(BaseHandler):
    def _star(self, notebook_name, note_name, star, redir=True):
        starred = self.get_starred()
        full_name = u'%s/%s' % (notebook_name, note_name)
        if star == 'set' and full_name not in starred:
            starred.append(full_name)
        elif star == 'unset' and full_name in starred:
            starred.remove(full_name)
        self.set_cookie('starred_notes',
                        b64encode(','.join(starred).encode('utf8')),
                        expires=2667692112)
        if redir:
            self.redirect('/%s/%s' % (url_escape(notebook_name).replace('#', '%23'), url_escape(note_name).replace('#', '%23')))

    def _delete(self, notebook_name, note_name, confirmed=False):
        notebook_enc = self.encode_name(notebook_name)
        note_enc = self.encode_name(note_name)
        path = join(self.settings.repo, notebook_enc, note_enc)
        dot_path = join(self.settings.repo, notebook_name, '.' + note_name)
        if confirmed:
            self.application.git.rm(path)
            if exists(dot_path):
                self.application.git.rm(dot_path)
            self.application.git.commit('-m', 'removing %s' % path)

            self._star(notebook_name, note_name, 'unset', False)

            self.redirect('/' + notebook_enc.replace('#', '%23'))
        else:
            self.render('delete.html', notebook_name=notebook_name,
                        note_name=note_name)

    def _edit(self, notebook_name, note_name, note_contents=None,
              confirmed=False, toggle=-1):

        notebook_enc = self.encode_name(notebook_name)
        note_enc = self.encode_name(note_name)
        path = join(self.settings.repo, notebook_enc, note_enc)
        if not confirmed:
            note_contents = open(path).read()
            self.render('note.html', notebook_name=notebook_name,
                        note_name=note_name, note_contents=note_contents,
                        edit=True, autosave=self.settings['autosave'])
        else:
            if toggle > -1:
                f = open(path)
                tmp = []
                search_string = r'^(\s*?)(\[.\])\s(.*)$'
                index = 0
                for line in f.readlines():
                    regex = search(search_string, line)
                    if regex is not None:
                        if int(index) == int(toggle):
                            old = regex.group(2)
                            if old == '[x]':
                                new = '[ ]'
                            else:
                                new = '[x]'
                            line = "%s%s %s\n" % \
                            (regex.group(1), new, regex.group(3))
                        index = index + 1
                    tmp.append(line)
                f.close()
                note_contents = ''.join(tmp)

            f = open(path, 'w')
            f.write(note_contents.encode('utf8'))
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
            self.redirect(note_enc.replace('#', '%23'))

    def _view_plaintext(self, notebook_name, note_name, highlight=None,
                        dot=False):
        notebook_enc = self.encode_name(notebook_name)
        note_enc = self.encode_name(note_name)
        if dot:
            path = join(self.settings.repo, notebook_enc, '.' + note_enc)
        else:
            path = join(self.settings.repo, notebook_enc, note_enc)
        note_contents = open(path).read()
        note_contents = markdown(note_contents)
        if highlight is not None:
            note_contents = self.highlight(note_contents, highlight)
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
        notebook_name = self.encode_name(notebook_name)
        note_name = self.encode_name(note_name)

        action = self.get_argument('a', 'view')
        if action == 'delete':
            self._delete(notebook_name, note_name, confirmed=False)
        elif action == 'edit':
            self._edit(notebook_name, note_name, confirmed=False)
        elif action == 'star':
            self._star(notebook_name, note_name, star='set')
        elif action == 'unstar':
            self._star(notebook_name, note_name, star='unset')
        else:
            path = join(self.settings.repo, notebook_name, note_name)
            dot_path = join(self.settings.repo, notebook_name, '.' + note_name)
            highlight = self.get_argument('hl', None)
            with Magic() as m:

                # Open the file since m.id_filename() does not accept utf8
                # paths, not even when using path.decode('utf8')
                with open(path) as f:
                    mime = m.id_buffer(f.read())
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
        notebook_name = self.encode_name(notebook_name)
        note_name = self.encode_name(note_name)

        action = self.get_argument('a', 'view')
        if bool(self.get_argument('save', False)):
            note = self.get_argument('note')
            toggle = self.get_argument('toggle', -1)
            self._edit(notebook_name=notebook_name, note_name=note_name,
                       note_contents=note, confirmed=True, toggle=toggle)
        elif bool(self.get_argument('delete', False)):
            self._delete(notebook_name, note_name, confirmed=True)
        else:
            self.redirect(note_name.replace('#', '%23'))
