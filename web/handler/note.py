from os.path import join

from markdown2 import markdown
from sh import ErrorReturnCode_1

from base import BaseHandler

class NoteHandler(BaseHandler):
    def get(self, notebook_name, note_name):
        # TODO this should do some sort of file type checking so that it only tries to manipulate plain text files
        # TODO figure out how to handle other file types (specifically PDF, WORD, and common image types)
        notebook_name = notebook_name.replace('+', ' ')
        note_name = note_name.replace('+', ' ')
        delete = self.get_argument('delete', False)
        if delete:
            self.render('delete.html', notebook_name=notebook_name,
                        note_name=note_name)
        else:
            edit = self.get_argument('edit', False)
            path = join(self.settings.repo, notebook_name, note_name)
            note_contents = open(path).read()
            if not edit:
                note_contents = markdown(note_contents)
                highlight = self.get_argument('hl', None)
                if highlight is not None:
                    note_contents = self._highlight(note_contents, highlight)
                # TODO checking / unchecking a checkbox should save the note
                note_contents = note_contents.replace('[ ]', '<input type=checkbox>')
                note_contents = note_contents.replace('[x]', '<input type=checkbox checked=true>')
            self.render('note.html', notebook_name=notebook_name,
                        note_name=note_name, note_contents=note_contents,
                        edit=edit)

    def post(self, notebook_name, note_name):
        notebook_name = notebook_name.replace('+', ' ')
        note_name = note_name.replace('+', ' ')
        if bool(self.get_argument('save', False)):
            path = join(self.settings.repo, notebook_name, note_name)
            note = self.get_argument('note')
            f = open(path, 'w')
            f.write(note)
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
            path = join(self.settings.repo, notebook_name, note_name)
            self.application.git.rm(path)
            self.application.git.commit('-m', 'removing %s' % path)
            self.redirect('/' + notebook_name)
        else:
            self.redirect(note_name)
