from urllib2 import quote, unquote

import bcrypt

from base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        error = self.get_argument('error', None)
        self.render('login.html', error=error, hide_notebooks=True)

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username is None or password is None:
            self.redirect('/login?error=' + quote(("Username and password are "
                                                   "required!")))
        elif username != self.settings.username or \
        bcrypt.hashpw(password, self.settings.pwdhash) != self.settings.pwdhash:
            self.redirect('/login?error=' + quote("Username/password "
                                                  "incorrect!"))
        else:
            self.make_cookie('session', self.settings.session)
            self.redirect(self.get_argument('next', '/'))
