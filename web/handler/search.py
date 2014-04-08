import logging
from os.path import join
from re import sub
from sh import grep
from urllib2 import unquote

from base import BaseHandler

class SearchHandler(BaseHandler):
    def get(self):
        query = unquote(self.get_argument('q'))
        results = str(grep('-R', '--exclude-dir', '.git', query,
                           self.settings.repo_root))
        results = results.replace(self.settings.repo_root, '').split('\n')[:-1]
        formatted_results = []
        for result in results:
            filename, string = result.split(':')
            string = self._highlight(string, query)
            formatted_results.append({'filename': filename, 'string': string})
        self.render('search.html', query=query, results=formatted_results)
