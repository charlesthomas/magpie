======
magpie
======
magpie: [ma]rkdown, [g]it, [pie]thon

Git-backed Evernote replacement

Useful Links
------------

`magpie on Github`_
`magpie in PyPI`_
`Contributing`_
`To Do`_

Quickstart
----------

What is magpie?
---------------
I *love* `Evernote`_, but I no longer trust my data to cloud providers. Magpie
is an attempt to make a reasonably sufficient Evernote replacement where the
user controls their data.

Basically, magpie is just a web tool for managing text files in a git repo. In
it, you can create notebooks (which are just folders); create, edit, and delete
notes (which are just files). That's pretty much it. However, when you make any
of these changes, they are automatically committed to git.

What isn't magpie?
------------------

* Complete (see `contributing`_)

* Secure (magpie is only as safe as you make it. If your git repo is hosted on
  a public server, people will be able to read your notes. If you run it on an
  open network, people may be able to access your notes. Etc.)

* Shiny (This is a side project written and maintained - so far - by a single
  person. It's never going to be as good or as useable as Evernote.)

Features
--------

* Markdown notes are rendered on the page

* Uses git as a backend

    * Easy backups (if you know git): clone once, then pull to backup notes

    * track history, etc, just like with git (using git, not via magpie's web
      interface ... yet?)

* Render "[ ]" and "[x]" as check boxes. Clicking them changes and saves the
  note.

* Email yourself notes (see `emailing notes`_)

.. _magpie on Github: https://github.com/charlesthomas/magpie/
.. _magpie on PyPI: https://pypi.python.org/pypi/magpie/
.. _Contributing: https://github.com/charlesthomas/magpie/blob/master/contributing.rst
.. _To Do: https://github.com/charlesthomas/magpie/blob/master/todo.md
.. _Evernote: https://evernote.com
.. _emailing notes: emailing_notes.rst
