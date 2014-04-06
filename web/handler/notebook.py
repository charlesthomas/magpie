from os import listdir
from os.path import join

from base import BaseHandler

class NotebookHandler(BaseHandler):
    def get(self, notebook_name=None):
        if notebook_name is None:
            path = self.settings.repo_root
        else:
            if notebook_name.endswith('/'):
                notebook_name = notebook_name[:-1]
            path = join(self.settings.repo_root, notebook_name)
        notebook_contents = listdir(path)
        if '.git' in notebook_contents:
            notebook_contents.remove('.git')
        self.render('notebook.html', notebook_name=notebook_name,
                    note_name=None, notebook_contents=notebook_contents)
