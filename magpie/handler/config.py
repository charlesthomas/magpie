from os.path import join

import bcrypt
from tornado.web import authenticated
from sh import git
from os.path import exists

from base import BaseHandler

class ConfigHandler(BaseHandler):
    ALLOWED = {'testing': bool, 'port': int, 'pwdhash': str, 'repo': str, 'repo_user': str, 'repo_email': str,
               'username': str, 'autosave': bool, 'listen_localhost_only': bool}
    @authenticated
    def get(self):
        self.render('config.html', config=self._fetch_existing_config())

    @authenticated
    def post(self):
        old = self._fetch_existing_config()
        new = dict()
        try:
                un=git('config','--get','user.name')
                ue=git('config','--get','user.email')
        except Exception, e:
                un=''
                ue=''
        for key in self.ALLOWED.keys():
            if self.ALLOWED[key] == bool:
                val = self.get_argument(key, False)
            else:
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
            if key == 'repo_user' and un != val:
                git.config('--global', 'user.name',  val)
            elif key == 'repo_email' and ue != val:
                git.config('--global', 'user.email', val)
            elif key == 'repo' and not exists(val):
                git.init(val)
            else:
                continue
        config_file.close()
        self.redirect('/')

    def _fetch_existing_config(self):
        existing = dict()
        for config in open(self.settings.config_path.web).readlines():
            key, val = config.strip().replace(' = ', '=').split('=')
            existing[key] = val.replace("'", "")
        return existing
