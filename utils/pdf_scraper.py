#!/usr/bin/env python
from os import path
from sys import argv

from pyPdf import PdfFileReader
from tornado.options import define, options, parse_config_file

from magpie.config import config_path

define('repo', default=None, type=str)
define('default_notebook', default='', type=str)
parse_config_file(config_path.pdf_scraper)

def scrape(file_path):
    pdf = PdfFileReader(file(file_path, 'rb'))
    content = ''
    for i in range(0, pdf.numPages):
        # TODO figure out why line breaks don't seem to be rendering
        content += pdf.getPage(i).extractText() + '\n'
    out_file = '.%s' % path.basename(file_path)
    out_path = path.join(path.dirname(file_path), out_file)
    if options.repo not in path.commonprefix([out_path, options.repo]):
        out_path = path.join(options.repo, options.default_notebook, out_file)
    content = content.encode('ascii', 'ignore')
    f = open(out_path, 'w')
    f.write(content)
    f.close()

if __name__ == '__main__':
    for file_name in argv[1:]:
        scrape(file_name)
