# coding=UTF-8

from os import makedirs, path
from shutil import rmtree
from urllib import quote

from base import BaseTest

class Test(BaseTest):
    def setUp(self):
        super(Test, self).setUp()
        self.notebook_slug = 'test_notebook'
        self.notebook_path = path.join(self.get_app().settings.repo,
                                       self.notebook_slug)
        self.notebook_url = '/%s/' % self.notebook_slug
        makedirs(self.notebook_path)

    def tearDown(self):
        rmtree(path.join(self.notebook_path))
        super(Test, self).tearDown()

    def touch(self, note, notebook=None):
        if notebook is None:
            notebook = self.notebook_slug
        open(path.join(self.get_app().settings.repo,
                       notebook,
                       note), 'a').close()

    def test_spaces_in_note_names(self):
        note_name_spaces = 'note name with spaces'
        note_name_pluses = note_name_spaces.replace(' ', '+')
        
        # touch file
        self.touch(note_name_spaces)

        # magpie 500s on bad notes
        self.get(self.notebook_url + note_name_pluses)

    def test_unicode_note_names(self):
        note_name = u'übernöte'
        self.touch(note_name)
        self.get(self.notebook_url + quote(note_name.encode('utf8')))

    def test_create_note(self):
        note_name = 'test_note'
        res = self.post(self.notebook_url + note_name,
                        allow_errors=True,
                        save=True,
                        note='this is a test note')
        test_path = path.join(self.notebook_path, note_name)
        self.assertTrue(path.exists(test_path))
