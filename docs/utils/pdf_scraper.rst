=============
Scraping PDFs
=============
A nice feature of Evernote is that it scrapes PDFs you upload in order to make
them searchable. Magpie has that ability as well, if you use the magpie util
``pdf_scraper.py``.

Configuration
=============
``pdf_scraper.py`` has a config file, like magpie and ``email_notes.py``, and it
lives in the same place as the other config files. It only has two options to
configure:

* repo: This is (presumably) the same value you specified in the magpie config.
* default_notebook: If you run ``pdf_scraper.py`` on a PDF outside of your
  magpie repo, the plaintext output will be written to this notebook inside the
  magpie repo, rather than wherever the PDF lives

Scraping
========
Using ``pdf_scraper.py`` should be fairly straightforward. After configuration,
simply run ``pdf_scraper.py /path/to/pdf1.pdf /another/path/pdf2.pdf etc.pdf``.
The scraper will run against each of the files passed as command line arguments.
If the PDFs were inside the configured magpie repo, then the output files will
be stored in the same location as the original PDF, and then name will be
identical, except the filename will have a leading period. For example, if the
PDF was ``/path/to/file.pdf`` then the plaintext output from the scraper would
be stored in ``/path/to/.file.pdf``. If the PDF is not already in the configured
repo, then the file will still start with ".", and will be saved to the
default_notebook from the config file.

Ugly Output
===========
The odds are pretty good that the output of ``pdf_scraper.py`` will be ugly.
That's the best I could do for now. The purpose of this functionality is
primarily to allow for searching the PDFs, not necessarily to read their
contents in the web application. However, once the plaintext version exists in
magpie, you can edit it in the web application just like any other note, and it
will not impact the PDF. This means if you want to make the note readable and
clean it up, you can.
