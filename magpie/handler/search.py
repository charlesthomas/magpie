import logging
from os import path
from re import sub
from sh import grep, ErrorReturnCode_1
from urllib2 import unquote

from base import BaseHandler

class SearchHandler(BaseHandler):
    def get(self):
        query = unquote(self.get_argument('q'))
        try:
            # TODO this doesn't search the names of notes/notebooks
            results = str(grep('-R', '--exclude-dir', '.git', query,
                               self.settings.repo))
        except ErrorReturnCode_1 as e:
            results = ''
        results = results.replace(self.settings.repo, '').split('\n')[:-1]
        formatted_results = []
        for result in results:
            if 'Binary file' in result:
                continue

            stuff = result.split(':')
            filename = stuff[0]
            if path.basename(filename).startswith('.'):
                filename = path.join(path.dirname(filename),
                                     path.basename(filename)[1:])
            string = ''.join(stuff[1:])
            string = self._highlight(string, query)
            formatted_results.append({'filename': filename, 'string': string})
        self.render('search.html', query=query, results=formatted_results)
