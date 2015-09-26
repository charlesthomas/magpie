==============
Emailing Notes
==============
One of the most convenient features of Evernote is the ability to email notes to
yourself. I've attempted to duplicate this functionality for magpie. This is a
totally separate process from the magpie web server, but is also installed when
you ``pip install magpie``. In addition to magpie being installed as an
executable, you should also get an executable called ``email_notes.py``.

The ``email_notes.py`` script **does not** delete email, and it only operates on
**unread** emails.

Configuration
=============
``email_notes.py`` is configured via a config file in ``magpie/config``.
Assuming you're using virtualenv, and you've named the magpie virtualenv
"magpie", then the full path would be something like
``/home/you/.virtualenvs/magpie/lib/python-verison/site-packages/magpie/config/email_notes.cfg``.
In that file, you can set the following options:

* imap_server: This is the address of your IMAP server (non-IMAP email isn't
  currently supported)
* username: The username you use to authenticate to the server (likely, but not
  necessarily your email address)
* password: The password you use to authenticate to the server
* folder: You'll probably want to have notes filtered into a special folder
  (gmail calls these labels) so they don't clutter up your inbox. specify that
  here.
* repo: This is the git repo where your notes live (almost certainly should be
  the same path you specified when configuring the web application)
* use_ssl: Do you want to connect securely to your IMAP server (recommended)
* default_notebook: You can specify which notebook an email will be saved to in
  the subject line of the email (see "Subject Syntax" below). If you don't
  specify that in the subject, your notes will default to this notebook.

**With the exception of use_ssl, all fields should be wrapped in single or
double quotes. use_ssl should either be True (capital T) or False (capital F).**

Subject Syntax
==============
The body of the email you sent will be the contents of your note in magpie. The
title of your note, which notebook it should be stored in, and more will be
controlled via the subject line of the email. If you have not set the folder
field in the config file, or have set it to anything other than "inbox"
(case-**in**sensitive), then your notes ***MUST*** start with "\*Note\* ". If
you *have* specified a folder (other than "inbox", then do not include
"\*Note\*". If you want to specifiy a notebook other than the default from the
config file, use "@notebook name" towards the end of the subject line. If you
want an existing note to be appended to, rather than overwritten, add " +" as
the very last thing in the subject line. Everything from the beginning of the
subject line (excluding \*Note\* if it's required), and before either @ if
you've specified the notebook name or + if you haven't will be considered the
title of the note.

Examples
--------

    This is a plain note title

This note will be called "This is a plain note title" and will be stored in the
default_notebook specified in the config file. If a note with that name already
exists, **its contents will be overwritten** by the contents of the email.

    \*Note\* This is also plain

If you have not specified a folder in the config file, then "\*Note\* " is
required, and this note will be called "This is also plain" and stored in the
default notebook. **If you *have* specified a folder in the config file, this
note will be titled "\*Note\* This is also plain."**

    This is an appended note +

This note will be called "This is an appended note" It will be placed in the
default_notebook and if a note with that title exists, the contents of the email
will be appended to the end of the existing text.

    This will be stored in a different notebook @another notebook

This note will be stored in the notebook "another notebook"

    Appended note in @another notebook +

This note will be stored in "another notebook" it will be titled "Appended note
in" and will be appended to the end of the existing note, if one already exists
with that name.

Filtering
=========
You'll probably want to create an email filter for these notes so they don't
clog your inbox, and so you can specify that in the config file so you don't
have to add "\*Note\* " to the beginning of *every* note you send yourself. Many
email servers allow you to alter your email address in order to setup special
filters. For example, in gmail you can add "+anyTextYouWant" to the end of your
username *and* you can add or remove periods to your heart's content. So if your
email address was "magpie@gmail.com" you could set up a filter to send notes
sent from yourself to "m.agpie@gmail.com" or "magpie+note@gmail.com" to be moved
to your "notes" folder/label, and then configure "notes" as the "folder" value
in the config file.

Scheduling
==========
``email_notes.py`` runs once and then exits; it does not run as a daemon. You
probably want to configure cron or some other scheduler to run it at some
interval so you don't have to remember to run it manually.
