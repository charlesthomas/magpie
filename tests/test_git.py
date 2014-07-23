from os import path

from sh import git

from base import BaseTest

class Test(BaseTest):
    def setUp(self):
        super(Test, self).setUp()

        self.git = git.bake(_cwd=self.path)
        self.notebook_name = 'git_tests'
        self.note_name = 'test_note'

        # make notebook
        res = self.post('/' + self.notebook_name)

    def test_new_note_commits_to_git(self):
        note_text = 'this should be added to git'
        res = self.post('/%s/%s' % (self.notebook_name, self.note_name),
                        save=True,
                        note=note_text)
        log = self.git.log('-p', '-n', '1', '--no-color').split('\r\n')
        full_path = path.join(self.path, self.notebook_name, self.note_name)
        self.assertTrue('updating %s' % full_path in log[4])
        self.assertTrue(log[12].startswith('+%s' % note_text),
                        msg=log[12])
