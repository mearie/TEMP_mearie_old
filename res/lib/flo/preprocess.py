"""Text preprocessor.
"""

from __future__ import absolute_import, division, with_statement

#from . import resolve

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import html_error_template
import os, os.path

class Preprocessor(object):
    def __init__(self, base):
        self.base = base
        self.lookup = TemplateLookup(directories=['/',base],
                input_encoding='utf-8', output_encoding='utf-8',
                encoding_errors='replace')

    def process(self, path):
        template = self.lookup.get_template(path)
        data = template.render()
        return data

    def process_error(self):
        template = html_error_template()
        data = template.render()
        return data

