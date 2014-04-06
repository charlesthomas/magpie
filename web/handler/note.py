from os.path import join

from markdown2 import markdown
from sh import ErrorReturnCode_1

from tornado.web import RequestHandler
# from base import BaseHandler

# class NoteHandler(BaseHandler):
class NoteHandler(RequestHandler):
    def get(self, notebook, note_name):
        edit = self.get_argument('edit', False)
        path = join(self.settings.repo_root, notebook, note_name)
        note_contents = open(path).read()
        if not edit:
            note_contents = note_contents.replace('[ ]', '<input type=checkbox>')
            note_contents = note_contents.replace('[x]', '<input type=checkbox checked=true>')
            note_contents = markdown(note_contents)
        self.render('note.html', notebook=notebook, note_name=note_name,
                    note_contents=note_contents, edit=edit)

    def post(self, notebook, note_name):
        if bool(self.get_argument('save', False)):
            path = join(self.settings.repo_root, notebook, note_name)
            f = open(path, 'w')
            f.write(self.get_argument('note'))
            f.close()

            self.application.git.add(path)
            try:
                self.application.git.commit('-m', 'updating %s' % path)
            except ErrorReturnCode_1 as e:
                if 'nothing to commit' not in e.message:
                    raise
        self.redirect(note_name)
