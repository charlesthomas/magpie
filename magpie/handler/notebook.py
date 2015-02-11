from os import listdir, makedirs, path

from tornado.web import authenticated

from base import BaseHandler
from pprint import pprint
class NotebookHandler(BaseHandler):
    @authenticated
    def get(self, notebook_name):
        if notebook_name.endswith('/'):
            notebook_name = notebook_name[:-1]
        notebook_name = self.encode_name(notebook_name)

        if not path.isdir(path.join(self.settings.repo, notebook_name)):
            self.redirect('/')
        else:
            notebook_path = path.join(self.settings.repo, notebook_name)
            #notebook_contents = []
            #for fil in listdir(notebook_path):
            #    if not fil.startswith('.'):
            #        notebook_contents.append(fil)
            notebook_contents = listdir(notebook_path)
            pprint(notebook_contents)
            if '.git' in notebook_contents:
                notebook_contents.remove('.git')
            self.render('notebook.html', notebook_name=notebook_name,
                        note_name=None, notebook_contents=notebook_contents)

    @authenticated
    def post(self, notebook_name):
        if notebook_name.endswith('/'):
            notebook_name = notebook_name[:-1]
        notebook_name = self.encode_name(notebook_name)

        notebook_path = path.join(self.settings.repo, notebook_name)
        if not path.exists(notebook_path):
            makedirs(notebook_path)
        self.finish()
