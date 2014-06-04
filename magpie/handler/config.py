from os.path import join

import bcrypt
from tornado.web import authenticated

from base import BaseHandler

class ConfigHandler(BaseHandler):
    ALLOWED = {'testing': bool, 'port': int, 'pwdhash': str, 'repo': str,
               'username': str}
    @authenticated
    def get(self):
        self.render('config.html', config=self._fetch_existing_config())

    @authenticated
    def post(self):
        # TODO need confirm password field?
        old = self._fetch_existing_config()
        new = dict()
        for key in self.ALLOWED.keys():
            val = self.get_argument(key, None)
            if val is None or val == '':
                new[key] = old[key]
            elif key == 'pwdhash':
                new[key] = bcrypt.hashpw(val, bcrypt.gensalt())
            elif self.ALLOWED[key] == str:
                new[key] = str(val)
            elif self.ALLOWED[key] == int:
                new[key] = int(val)
            elif self.ALLOWED[key] == bool:
                new[key] = bool(val)
        config_file = open(self.settings.config_path.web, 'w')
        for key, val in new.items():
            if self.ALLOWED[key] == str:
                config_file.write("%s='%s'\n" % (key, val))
            else:
                config_file.write("%s=%s\n" % (key, val))
        config_file.close()
        self.redirect('/')

    def _fetch_existing_config(self):
        existing = dict()
        for config in open(self.settings.config_path.web).readlines():
            key, val = config.strip().replace(' = ', '=').split('=')
            existing[key] = val.replace("'", "")
        return existing
