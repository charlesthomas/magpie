# coding=UTF-8
from os import makedirs, path, rmdir
from shutil import rmtree
from urllib import quote

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
            if e.strerror != 'File exists':
                raise

        home = self.fetch('/')
        notebook = self.fetch('/notebook+name')
        try:
            self.assertNotEqual(home.body, notebook.body,
                                msg=("It looks like notebook w/space in name "
                                     "can't be opened"))
        finally:
            rmdir(path.join(app.settings.repo, 'notebook name'))

    def test_unicode_notebooks(self):
        app = self.get_app()
        dirname = u'übernöteböök'.encode('ascii', errors='xmlcharrefreplace')
        try:
            makedirs(path.join(app.settings.repo, dirname))
        except OSError as e:
            if e.strerror != 'File exists':
                raise

        try:
            home = self.fetch('/')
            notebook = self.fetch('/' + quote(dirname))
            self.assertNotEqual(home.body, notebook.body)
        finally:
            rmtree(path.join(app.settings.repo, dirname))
