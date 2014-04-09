import logging
from os.path import join
from re import sub
from sh import grep, ErrorReturnCode_1
from urllib2 import unquote

from base import BaseHandler

class SearchHandler(BaseHandler):
    def get(self):
        query = unquote(self.get_argument('q'))
        try:
            results = str(grep('-R', '--exclude-dir', '.git', query,
                               self.settings.repo_root))
        except ErrorReturnCode_1 as e:
            results = ''
        results = results.replace(self.settings.repo_root, '').split('\n')[:-1]
        formatted_results = []
        for result in results:
            stuff = result.split(':')
            filename = stuff[0]
            string = ''.join(stuff[1:])
            string = self._highlight(string, query)
            formatted_results.append({'filename': filename, 'string': string})
        self.render('search.html', query=query, results=formatted_results)
