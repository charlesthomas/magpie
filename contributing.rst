============
Contributing
============

Bug Fixes / Minor Changes
-------------------------
magpie uses `todo.md`_ to track TODO items in its code. If you're looking to fix
bugs, `magpie's todo.md`_ is a good place to start.

New Features
------------
There are a few features that magpie could use to make it really great, and even
better competition for Evernote.

Web Scraper
===========
Evernote has a Javascript bookmarklet that will scrape a webpage and add it as a
note. If I was better with Javascript, I'd try to implement this myself.

OCR
===
Evernote's `OCR`_ is *really* good. I looked into Python projects that would
allow me to do OCR in magpie, and I didn't find anything that seemed both
feature complete and easy to use.

Word / PDF / Etc Scraper
========================
It would be great if a user could upload docs of various types to magpie and
have them scraped into plaintext. I started building functionality into magpie
already that will handle viewing the plaintext version of a non-plaintext
document, by looking at files with identical names, only the plaintext filename
starts with a dot. For example::

    file.doc  <-- Word
    .file.doc <-- plaintext

In the above example, magpie will render the .file.doc plaintext file when you
click on file.doc in the left-hand side notes menu.

Testing
-------
No tests exist for magpie yet, but some probably should. I've used `Travis-CI`_
for other projects and would recommend starting by setting up a `.travis.yaml`_
file.

.. _todo.md: https://github.com/charlesthomas/todo.md
.. _magpie's todo.md: https://github.com/charlesthomas/magpie/blob/master/todo.md
.. _OCR: https://en.wikipedia.org/wiki/Optical_character_recognition
.. _Travis-CI: https://travis-ci.org/
.. _.travis.yaml: http://docs.travis-ci.com/user/languages/python/
