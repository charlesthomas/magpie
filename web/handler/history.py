import logging
from os.path import join
from pprint import pformat

from base import BaseHandler

class HistoryHandler(BaseHandler):
    # TODO This is SUPER broken - it just hangs
    # TODO paginate by using -n y / --skip=x*y
    # where x is the page number and y is the number to show at once
    # TODO get rid of control chars
    def get(self, notebook, note_name):
        path = join(self.settings.repo_root, notebook, note_name)
        history = self.application.git.log('--no-color', '--pretty=fuller', path)
        history = history.replace('\n', '<br>')
        self.render('history.html', note_name=note_name, history=history)
