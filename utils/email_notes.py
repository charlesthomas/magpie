#!/usr/bin/env python
from email import message_from_string
from email.header import decode_header
from imaplib import IMAP4, IMAP4_SSL
from os import makedirs
from os.path import exists, join
import re
from sys import exit

import sh
from tornado.options import define, options, parse_config_file

from magpie.config import config_path

class EmailNotesError(Exception):
    pass

define('imap_server', default=None, type=str)
define('username', default=None, type=str)
define('password', default=None, type=str)
define('folder', default=None, type=str)
define('repo', default=None, type=str)
define('use_ssl', default=True, type=bool)
define('default_notebook', default='', type=str)
parse_config_file(config_path.email_notes)

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

# TODO there seems to be a bug where other notes in other notebooks can be deleted
# it might be when a folder is created?
git = sh.git.bake(_cwd=options.repo)
for message_index in messages[0].split(' '):
    junk, data = imap.fetch(message_index, '(RFC822)')
    message = message_from_string(data[0][1])
    subject = decode_header(message.get('Subject'))[0]
    if subject[1] is None:
        subject = subject[0]
    else:
        subject = subject[0].decode(subject[1])
    subject = subject.replace('\r\n','')

    append = False
    if options.folder is None or options.folder.lower() == 'inbox':
        with_notebook = r'^\*Note\*\s(.*)\s@(.*)$'
        without_notebook = r'^\*Note\*\s(.*)$'
    else:
        with_notebook = r'^(.*)\s@(.*)$'
        without_notebook = r'^(.*)$'
    regex = re.search(with_notebook, subject)
    if regex is None:
        regex = re.search(without_notebook, subject)
        notebook_name = options.default_notebook
    else:
        notebook_name = regex.group(2)
        if notebook_name.endswith(' +'):
            notebook_name = notebook_name[:-2]
            append = True
    if regex is None:
        continue

    note_name = regex.group(1)
    if note_name.endswith(' +'):
        note_name = note_name[:-2]
        append = True

    path = join(options.repo, notebook_name)
    if not exists(path):
        makedirs(path)
    path = join(path, note_name)
    if append:
        note_file = open(path, 'a')
    else:
        note_file = open(path, 'w')
    payload = message.get_payload()
    if type(payload) == list:
        text = ''
        for part in payload:
            text += part.get_payload()
    else:
        text = payload
    text = text.replace('\r\n', '\n')
    note_file.write(text)
    note_file.close()
    git.add(path)
    # TODO add try/except like web to prevent this from failing if there's no change
    git.commit('-m', 'adding %s from email_notes.py' % note_name)
