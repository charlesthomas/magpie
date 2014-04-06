import logging
from os.path import join
from pprint import pformat

from markdown2 import markdown

from base import BaseHandler

class NoteHandler(BaseHandler):
    def get(self, dirname, filename):
        logging.info('dirname: %s' % dirname)
        logging.info('filename: %s' % filename)
        edit = self.get_argument('edit', False)
        path = join(self.settings.repo_root, dirname, filename)
        note = open(path).read()
        if not edit:
            note = note.replace('[ ]', '<input type=checkbox>')
            note = note.replace('[x]', '<input type=checkbox checked=true>')
            note = markdown(note)
        self.render('note.html', title=filename, note=note, edit=edit)

    def post(self, dirname, filename):
        if bool(self.get_argument('save', False)):
            path = join(self.settings.repo_root, dirname, filename)
            f = open(path, 'w')
            f.write(self.get_argument('note'))
            f.close()

            self.application.git.add(path)
            # TODO this freaks out if there weren't any changes (add a try/except)
            self.application.git.commit('-m', 'updating %s' % path)
        self.redirect(filename)
