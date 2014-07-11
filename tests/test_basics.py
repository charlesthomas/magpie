from os import makedirs, path, rmdir

from base import BaseTest

class Test(BaseTest):
    def test_proof_of_concept(self):
        res = self.fetch('/')

    def test_bad_notebook_redirects_home(self):
        home = self.fetch('/')
        dne = self.fetch('/this+notebook+doesnt+exist')
        self.assertEqual(home.body, dne.body)

    def test_spaces_ok_in_notebook_name(self):
        app = self.get_app()
        try:
            makedirs(path.join(app.settings.repo, 'notebook name'))
        except OSError as e:
            if e.strerror == 'File exists':
                pass
            else:
                raise

        home = self.fetch('/')
        notebook = self.fetch('/notebook+name')
        self.assertNotEqual(home.body, notebook.body)
        rmdir(path.join(app.settings.repo, 'notebook name'))
