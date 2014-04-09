#!/usr/bin/env python
import logging
from os import path

from sh import git
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file
from tornado.web import Application

from handler import urls

class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, val):
        self[key] = val

root = path.dirname(__file__)
static_path = path.join(root, 'static')
template_path = path.join(root, 'template')

app_config = dict(static_path=static_path,
                  template_path=template_path)

# TODO add username/password
# TODO have default username/password in config file, create reset-password functionality
define('port', default='8080', type=int)
define('testing', default=False, type=bool)
define('repo', default=None, type=str)
try:
    parse_config_file(path.join(root, 'magpie.cfg'))
except IOError:
    raise Exception('magpie.cfg file is REQUIRED\nTry renaming '
                    'magpie_example.cfg to magpie.cfg and editing it '
                    'as appropriate')

assert options.repo is not None, "--repo is required!"

if options.testing:
    app_config.update(debug=True)

server = Application(urls, **app_config)
server.settings = AttrDict(server.settings)
server.settings.repo_root = options.repo
server.git = git.bake(_cwd=server.settings.repo_root)
server.listen(options.port)
IOLoop.instance().start()
