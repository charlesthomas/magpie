#!/usr/bin/env python
from email import message_from_string
from email.header import decode_header
from imaplib import IMAP4, IMAP4_SSL
from os.path import dirname, join
from sys import exit

from sh import git
from tornado.options import define, options, parse_config_file

class EmailNotesError(Exception):
    pass

config_path = join(dirname(__file__), 'email_notes.cfg')

define('imap_server', default=None, type=str)
define('username', default=None, type=str)
define('password', default=None, type=str)
define('folder', default=None, type=str)
define('repo', default=None, type=str)
define('use_ssl', default=True, type=bool)
try:
    parse_config_file(config_path)
except IOError:
    raise Exception('email_notes.cfg file is REQUIRED\nTry renaming '
                    'email_notes_example.cfg to email_notes.cfg and editing it '
                    'as appropriate')

if options.use_ssl:
    imap = IMAP4_SSL(options.imap_server)
else:
    imap = IMAP4(options.imap_server)
imap.login(options.username, options.password)

result, data = imap.select(options.folder)
if result != 'OK':
    raise EmailNotesError(result)
result, messages = imap.search(None, '(UNSEEN)')
if result != 'OK':
    raise EmailNotesError(result)

if messages[0] == '':
    exit()

for message_index in messages[0].split(' '):
    junk, data = imap.fetch(message_index, '(RFC822)')
    message = message_from_string(data[0][1])
    subject = decode_header(message.get('Subject'))[0]
    if subject[1] is None:
        subject = subject[0]
    else:
        subject = subject[0].decode(subject[1])

    subject = subject.replace('*Note*', '')
    # TODO make a regex for @notebook @.*$
    # TODO append if subject.endswith(' +')
    # TODO figure out tags
    # TODO actually write and `git add` the note
