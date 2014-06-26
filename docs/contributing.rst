============
Contributing
============

Thanks!
-------
Thanks to:
* [Erwyn](https://github.com/Erwyn) for fixing [the write/reload race
  condition](https://github.com/charlesthomas/magpie/pull/15)
* [tomleo](https://github.com/tomleo) for fixing the [home dir config
bug](https://github.com/charlesthomas/magpie/pull/10)
* [looper](https://github.com/looperhacks) for adding the [home directory config
functionality](https://github.com/charlesthomas/magpie/pull/5).

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

Web Scraper
===========
Evernote has a Javascript bookmarklet that will scrape a webpage and add it as a
note. If I was better with Javascript, I'd try to implement this myself.

OCR
===
Evernote's `OCR`_ is *really* good. I looked into Python projects that would
allow me to do OCR in magpie, and I didn't find anything that seemed both
feature complete and easy to use.

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
No tests exist for magpie yet, but some probably should. I've used `Travis-CI`_
for other projects and would recommend starting by setting up a `.travis.yaml`_
file.

Documentation
-------------
Hopefully this documentation is good enough to get people using magpie, but
documentation can always be more thorough.

.. _todo.md: https://github.com/charlesthomas/todo.md
.. _magpie's todo.md: https://github.com/charlesthomas/magpie/blob/master/todo.md
.. _OCR: https://en.wikipedia.org/wiki/Optical_character_recognition
.. _Travis-CI: https://travis-ci.org/
.. _.travis.yaml: http://docs.travis-ci.com/user/languages/python/
