from os import listdir, makedirs
from os.path import isdir, join

from tornado.web import authenticated


from base import BaseHandler

class NotebookHandler(BaseHandler):
    @authenticated
    def get(self, notebook_name):
        notebook_enc = self.encode_name(notebook_name)

        print '%s :: %s' % (join(self.settings.repo, notebook_enc), notebook_name)
        if not isdir(join(self.settings.repo, notebook_enc)):
            self.redirect('/')
        else:
            if notebook_enc.endswith('/'):
                notebook_enc = notebook_enc[:-1]
            path = join(self.settings.repo, notebook_enc)
            notebook_contents = listdir(path)
            if '.git' in notebook_contents:
                notebook_contents.remove('.git')
            self.render('notebook.html', notebook_name=notebook_name,
                        note_name=None, notebook_contents=notebook_contents)

    @authenticated
    def post(self, notebook_name):
        path = join(self.settings.repo, self.encode_name(notebook_name))
        makedirs(path)
        self.finish()
