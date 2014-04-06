from os import listdir
from os.path import join

from tornado.web import RequestHandler
# from base import BaseHandler

# class NotebookHandler(BaseHandler):
class NotebookHandler(RequestHandler):
    def get(self, notebook=None):
        if notebook is None:
            path = self.settings.repo_root
        else:
            if notebook.endswith('/'):
                notebook = notebook[:-1]
            path = join(self.settings.repo_root, notebook)
        notebook_contents = listdir(path)
        if '.git' in notebook_contents:
            notebook_contents.remove('.git')
        self.render('notebook.html', notebook_name=notebook,
                    notebook_contents=notebook_contents)
