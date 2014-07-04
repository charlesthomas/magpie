from os import listdir, makedirs
from os.path import isdir, join

from tornado.web import authenticated


from base import BaseHandler

class NotebookHandler(BaseHandler):
    @authenticated
    def get(self, notebook_name):
        notebook_name = self._encode_notename(notebook_name)
        if self.application.repo is None:
            self.redirect('/')
        elif not isdir(join(self.application.repo.working_dir, notebook_name)):
            self.redirect('/')
        else:
            if notebook_name.endswith('/'):
                notebook_name = notebook_name[:-1]
            path = join(self.application.repo.working_dir, notebook_name)
            notebook_contents = listdir(path)
            if '.git' in notebook_contents:
                notebook_contents.remove('.git')
            self.render('notebook.html', notebook_name=notebook_name,
                        note_name=None, notebook_contents=notebook_contents)

    @authenticated
    def post(self, notebook_name):
        path = join(self.application.repo.working_dir, self._encode_notename(notebook_name))
        makedirs(path)
        self.finish()
