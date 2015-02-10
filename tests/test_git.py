from os import path, linesep

from sh import git

from base import BaseTest

class Test(BaseTest):
    def setUp(self):
        super(Test, self).setUp()

        self.git = git.bake(_cwd=self.path)
        self.notebook_name = 'git_tests'

        # make notebook
        if not path.exists(path.join(self.path, self.notebook_name)):
            res = self.post('/' + self.notebook_name)

    def fetch_log(self):
        return self.git.log('-p', '-n', '1', '--no-color').split(linesep)

    def test_creating_note_commits_to_git(self):
        note_name = 'new_note'
        res = self.post('/%s/%s' % (self.notebook_name, note_name),
                        save=True,
                        note='')
        log = self.fetch_log()
        full_path = path.join(self.path, self.notebook_name, note_name)
        self.assertFalse('updating %s' % full_path in log[4])
        self.assertTrue('creating %s' % full_path in log[4])

    def test_saving_note_commits_to_git(self):
        note_name = 'test_note'
        note_text = 'this should be added to git'
        res = self.post('/%s/%s' % (self.notebook_name, note_name),
                        save=True,
                        note=note_text)
        log = self.fetch_log()
        full_path = path.join(self.path, self.notebook_name, note_name)
        self.assertTrue('updating %s' % full_path in log[4])
        self.assertTrue(log[12].startswith('+%s' % note_text),
                        msg=log[12])

    def test_deleting_note_removes_from_git(self):
        note_name = 'del_note'
        note_text = 'this should be removed from git'

        # make note
        res = self.post('/%s/%s' % (self.notebook_name, note_name),
                        save=True,
                        note=note_text)

        # delete note
        res = self.post('/%s/%s' % (self.notebook_name, note_name),
                        delete=True,
                        confirmed=True)

        log = self.fetch_log()
        full_path = path.join(self.path, self.notebook_name, note_name)
        self.assertTrue('removing %s' % full_path in log[4])
        self.assertTrue(log[12].startswith('-%s' % note_text),
                        msg=log[12])
