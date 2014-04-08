from os.path import join

from markdown2 import markdown
from sh import ErrorReturnCode_1

from base import BaseHandler

class NoteHandler(BaseHandler):
    # TODO need to escape strings, b/c somewhere, spaces are breaking stuff
    def get(self, notebook_name, note_name):
        delete = self.get_argument('delete', False)
        if delete:
            self.render('delete.html', notebook_name=notebook_name,
                        note_name=note_name)
        else:
            edit = self.get_argument('edit', False)
            path = join(self.settings.repo_root, notebook_name, note_name)
            note_contents = open(path).read()
            if not edit:
                note_contents = markdown(note_contents)
                highlight = self.get_argument('hl', None)
                if highlight is not None:
                    note_contents = self._highlight(note_contents, highlight)
                note_contents = note_contents.replace('[ ]', '<input type=checkbox>')
                note_contents = note_contents.replace('[x]', '<input type=checkbox checked=true>')
            self.render('note.html', notebook_name=notebook_name,
                        note_name=note_name, note_contents=note_contents,
                        edit=edit)

    def post(self, notebook_name, note_name):
        if bool(self.get_argument('save', False)):
            path = join(self.settings.repo_root, notebook_name, note_name)
            f = open(path, 'w')
            f.write(self.get_argument('note'))
            f.close()

            self.application.git.add(path)
            try:
                if note == '':
                    message = 'creating %s' % path
                else:
                    message = 'updating %s' % path
                self.application.git.commit('-m', message)
            except ErrorReturnCode_1 as e:
                if 'nothing to commit' not in e.message:
                    raise
            self.redirect(note_name)

        elif bool(self.get_argument('delete', False)):
            path = join(self.settings.repo_root, notebook_name, note_name)
            self.application.git.rm(path)
            self.application.git.commit('-m', 'removing %s' % path)
            self.redirect('/' + notebook_name)
        else:
            self.redirect(note_name)
