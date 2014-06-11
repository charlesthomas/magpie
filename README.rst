======
magpie
======

.. image:: https://dl.dropboxusercontent.com/u/402325/dontdelete/magpie.jpg

magpie: [ma]rkdown, [g]it, [pie]thon

Git-backed Evernote replacement

Quickstart
==========
Pre-requisites
--------------

(outside of PyPI):

* libmagic
* Python
* Pip/Easy Install
* Git

Installing magpie
-----------------
::

    pip install magpie

Setup Git Repo
--------------

git init
~~~~~~~~
Locally::

    mkdir -p /path/to/notes/repo/
    cd /path/to/notes/repo/
    git init

On `Github`_

On `Bitbucket`_

git config
~~~~~~~~~~
Depending on what your environment is like, you may get a nasty error the first
time you try to do something useful. This happened to me when I setup magpie to
work with supervisor. In order to resolve this, I had to set the ``user.name``
and ``user.email`` fields in git config. The error message on the magpie page
will tell you the syntax.

Launch magpie
-------------
::

    magpie

Connect
-------
In browser, go to http://localhost:8080

Configure
---------
On the main page, there should be a link to configure magpie. (Alternatively,
http://localhost:8080/config)

Enter as much info here as you want. Username / Password are not required, but
recommended. The only required field is repo. The path from "Init Git Repo"
above should be entered here.

Useful Links
============

* `magpie documentation`_
* `magpie on Github`_
* `magpie in PyPI`_
* `Contributing`_
* `To Do`_

What is magpie?
===============
I *love* `Evernote`_, but I no longer trust my data to cloud providers. Magpie
is an attempt to make a reasonably sufficient Evernote replacement where the
users control their data.

Basically, magpie is just a web tool for managing text files in a git repo. In
it, you can create notebooks (which are just folders); create, edit, and delete
notes (which are just files). That's pretty much it. However, when you make any
of these changes, they are automatically committed to git.

Demo
----
`A demo of magpie is available here`_

What isn't magpie?
==================

* Complete (see `contributing`_)

* Secure (magpie is only as safe as you make it. If your git repo is hosted on
  a public server, people will be able to read your notes. If you run it on an
  open network, people may be able to access your notes. Etc.)

* Shiny (This is a side project written and maintained - so far - by a single
  person. It's never going to be as good or as useable as Evernote.)

Features
========

* Markdown & HTML notes are rendered on the page

* Uses git as a backend

    * Easy backups (if you know git): clone once, then push/pull to backup notes

    * track history, etc, just like with git (using git, not via magpie's web
      interface ... yet?)

* Render "[ ]" and "[x]" as check boxes. Clicking them changes and saves the
  note.

* Email yourself notes (see `emailing notes`_)

* Scrape PDFs to make them searchable in magpie (see `pdf_scraper`_)

Image Attribution
=================
Logo/favicon courtesy of `Kieran Palmer`_, as licensed under CC BY-SA 2.0 Generic.

.. _Github: https://help.github.com/articles/create-a-repo
.. _Bitbucket: https://confluence.atlassian.com/display/BITBUCKET/Create+an+Account+and+a+Git+Repo
.. _magpie documentation: https://magpie-notes.readthedocs.org/en/latest/
.. _magpie on Github: https://github.com/charlesthomas/magpie/
.. _magpie in PyPI: https://pypi.python.org/pypi/magpie/
.. _Contributing: https://github.com/charlesthomas/magpie/blob/master/docs/contributing.rst
.. _To Do: https://github.com/charlesthomas/magpie/blob/master/todo.md
.. _Evernote: https://evernote.com
.. _A demo of magpie is available here: http://magpie.sknkwrks.net/
.. _emailing notes: https://magpie-notes.readthedocs.org/en/latest/utils/emailing_notes.html
.. _pdf_scraper: https://magpie-notes.readthedocs.org/en/latest/utils/pdf_scraper.html
.. _Kieran Palmer: http://www.kpword.net
