import logging
from os import path

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from magpie.server import make_app

logging.getLogger('tornado').setLevel(logging.ERROR)

APP = None

class BaseTest(AsyncHTTPTestCase):
    def get_app(self):
        # This global nonsense is because I was getting a port in use error when
        # running more than one test. I suspect I am missing something / doing
        # something wrong in testing, but this works.
        # I have seen the port in use error pop up again but it was only when
        # there were errors in this method
        global APP
        if APP is None:
            APP = make_app(path.join(path.dirname(__file__),
                                     'configs',
                                     'default.cfg'))
        return APP

    def fetch(self, url, allow_errors=False):
        self.http_client.fetch(self.get_url(url), self.stop)
        return self.wait()
