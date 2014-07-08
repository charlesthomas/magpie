from os import listdir, makedirs, path

from tornado.web import authenticated

from base import BaseHandler

class NotebookHandler(BaseHandler):
    @authenticated
    def get(self, notebook_name):
        notebook_enc = self.encode_name(notebook_name)

        if not path.isdir(path.join(self.settings.repo, notebook_enc)):
            self.redirect('/')
        else:
            if notebook_enc.endswith('/'):
                notebook_enc = notebook_enc[:-1]
            notebook_path = path.join(self.settings.repo, notebook_enc)
            notebook_contents = listdir(notebook_path)
            if '.git' in notebook_contents:
                notebook_contents.remove('.git')
            self.render('notebook.html', notebook_name=notebook_name,
                        note_name=None, notebook_contents=notebook_contents)

    @authenticated
    def post(self, notebook_name):
        notebook_path = path.join(self.settings.repo,
                                  self.encode_name(notebook_name))
        makedirs(notebook_path)
        self.finish()
