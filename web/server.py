#!/usr/bin/env python
import logging
from os import path
from random import choice
from string import letters, digits

from sh import git
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file
from tornado.web import Application

from handler import urls

class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, val):
        self[key] = val

def _rand_str(length=64):
    return ''.join([choice(letters + digits) for i in range(0, length)])

root = path.dirname(__file__)
static_path = path.join(root, 'static')
template_path = path.join(root, 'template')
config_path = path.join(root, '..', 'config', 'magpie.cfg')

app_config = dict(static_path=static_path,
                  template_path=template_path,
                  login_url='/login')

define('port', default='8080', type=int)
define('testing', default=False, type=bool)
define('repo', default=None, type=str)
define('username', default=None, type=str)
define('pwdhash', default=None, type=str)
try:
    parse_config_file(config_path)
except IOError:
    raise Exception('magpie.cfg file is REQUIRED\nTry renaming '
                    'magpie_example.cfg to magpie.cfg and editing it '
                    'as appropriate')

if options.testing:
    app_config.update(debug=True)
else:
    app_config.update(xsrf_cookies=True, cookie_secret=_rand_str())

server = Application(urls, **app_config)
server.settings = AttrDict(server.settings)
server.settings.repo = options.repo
server.settings.username = options.username
server.settings.pwdhash = options.pwdhash
server.settings.session = _rand_str()
server.settings.config_path = config_path
server.git = git.bake(_cwd=server.settings.repo)
server.listen(options.port)
autoreload.start()
autoreload.watch(config_path)
IOLoop.instance().start()
