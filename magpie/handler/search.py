from os import path
from re import sub
from sh import find, grep, ErrorReturnCode_1
from urllib2 import unquote

from tornado.web import authenticated

from base import BaseHandler

class SearchHandler(BaseHandler):
    @authenticated
    def get(self):
        query = unquote(self.get_argument('q', ''))
        if query == '':
            self.redirect('/')
        try:
            results = str(grep('-Rli', '--exclude-dir', '.git', query,
                               self.settings.repo))
        except ErrorReturnCode_1 as e:
            results = ''

        try:
            results += str(find(self.settings.repo, '-type', 'f', '-iname',
                                '*' + query + '*', '-not', '(', '-path',
                                '%s/%s/*' % (self.settings.repo, '.git'), ')'))
        except ErrorReturnCode_1 as e:
            pass

        results = results.replace(self.settings.repo, '').split('\n')[:-1]
        formatted_results = []
        for filename in results:
            if 'Binary file' in filename or filename == '':
                continue

            if path.basename(filename).startswith('.'):
                filename = path.join(path.dirname(filename),
                                     path.basename(filename)[1:])

            resultpath = path.join(self.settings.repo, filename[1:])
            if path.exists(resultpath):
                try:
                    string = str(grep('-i', query, resultpath ))
                except ErrorReturnCode_1 as e:
                    string = ''

                string = self.highlight(string, query)
                formatted_results.append({'filename': filename, 'string': string})
        self.render('search.html', query=query, results=formatted_results)
