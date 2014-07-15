============
Contributing
============

Thanks!
-------
Thanks to:

* tony-o for beginning the auto-save feature (`#20`_), fixing the .git search
  problem (`#21`_), cleaning up the base template (`#22`_), and adding ünicode 
  support.

* Erwyn for fixing the write/reload race condition (`#15`_)

* tomleo for fixing the home dir config bug (`#10`_)

* looper for adding the home directory config functionality (`#5`_)

Bug Fixes / Minor Changes
-------------------------
magpie uses `todo.md`_ to track TODO items in its code. If you're looking to fix
bugs, `magpie's todo.md`_ is a good place to start.

New Features
------------
There are a few features that magpie could use to make it really great, and even
better competition for Evernote.

Git Setup
=========
In order to use magpie right now, you have to know enough about git to init the
repo, and set the user name and email. It would be nice if magpie was smart
enough to do this through the web application.

Note history
=========
It should be possible to show the history of a note, and diff the changes between
notes versions, something like how redmine handles it on file versions:
http://www.redmine.org/projects/redmine/repository

Web Scraper
===========
Evernote has a Javascript bookmarklet that will scrape a webpage and add it as a
note. If I was better with Javascript, I'd try to implement this myself.

OCR
===
Evernote's `OCR`_ is *really* good. I looked into Python projects that would
allow me to do OCR in magpie, and I didn't find anything that seemed both
feature complete and easy to use.

A good option would be to use tessaract, https://code.google.com/p/tesseract-ocr/ 
but that will require that as an external dependency, rather than some
pure python-implementation.

Other document scrapers
=======================
It would be great if a user could upload docs of various types to magpie and
have them scraped into plaintext. I've already added a rudimentary PDF scraper,
and I started building functionality into magpie already that will handle
viewing the plaintext version of a non-plaintext document, by looking at files
with identical names, only the plaintext filename starts with a dot. For
example::

    file.pdf  <-- PDF
    .file.pdf <-- scraped plaintext

In the above example, magpie will render the .file.pdf plaintext file when you
click on file.pdf in the left-hand side notes menu.

OCR should be done on parts of the PDF which does not have text in it, such as 
image parts or scanned PDFs.

Utils Config Tool
=================
The pdf scraper and the script for turning emails into notes are called magpie
utils (and exist in the utils dir of the code base). Like the web application,
the utils each have their own config file, all located in ``magpie/config``.
There is functionality in the application to edit its own config file, but not
to edit the config files for any of the utils. It would be nice if that was
added by someone.

Testing
-------
There are some tests available for magpie, and tests are run by Travis on
each commit to master. See the current state here:
https://travis-ci.org/charlesthomas/magpie

Documentation
-------------
Hopefully this documentation is good enough to get people using magpie, but
documentation can always be more thorough.

.. _#20: https://github.com/charlesthomas/magpie/pull/20
.. _#21: https://github.com/charlesthomas/magpie/pull/21
.. _#22: https://github.com/charlesthomas/magpie/pull/22
.. _#15: https://github.com/charlesthomas/magpie/pull/15
.. _#10: https://github.com/charlesthomas/magpie/pull/10
.. _#5: https://github.com/charlesthomas/magpie/pull/5
.. _todo.md: https://github.com/charlesthomas/todo.md
.. _magpie's todo.md: https://github.com/charlesthomas/magpie/blob/master/todo.md
.. _OCR: https://en.wikipedia.org/wiki/Optical_character_recognition
.. _Travis-CI: https://travis-ci.org/
.. _.travis.yaml: http://docs.travis-ci.com/user/languages/python/
