"""Generic file processor.
"""

from __future__ import absolute_import, division, with_statement

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import html_error_template

class Preprocessor(object):
    def __init__(self, base):
        self.base = base
        self.inencoding = self.outencoding = 'utf-8'
        self.lookup = TemplateLookup(directories=['/', base], input_encoding=self.inencoding,
                output_encoding=self.outencoding, encoding_errors='replace')

    def process(self, context):
        template = self.lookup.get_template(context.path)
        data = template.render(flo=context)
        return data

    def process_error(self):
        template = html_error_template()
        data = template.render()
        return data

