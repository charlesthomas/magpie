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

from config import config_path
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

app_config = dict(static_path=static_path,
                  template_path=template_path,
                  login_url='/login')

define('port', default='8080', type=int)
define('testing', default=False, type=bool)
define('repo', default=None, type=str)
define('username', default=None, type=str)
define('pwdhash', default=None, type=str)
define('listen_localhost_only', default=True, type=bool)
parse_config_file(config_path.web)

if options.testing:
    app_config.update(debug=True)

server = Application(urls, **app_config)
server.settings = AttrDict(server.settings)
server.settings.repo = options.repo
server.settings.username = options.username
server.settings.pwdhash = options.pwdhash
server.settings.session = _rand_str()
server.settings.config_path = config_path

def main():
    server.git = git.bake(_cwd=server.settings.repo)
    if options.listen_localhost_only:
        server.listen(options.port, 'localhost')
    else:
        server.listen(options.port)
    autoreload.start()
    autoreload.watch(config_path.web)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
