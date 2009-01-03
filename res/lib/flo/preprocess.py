"""Text preprocessor.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import html_error_template
from mako.util import FastEncodingBuffer
import os, os.path

class Preprocessor(object):
    def __init__(self, base):
        self.base = base
        self.inencoding = self.outencoding = 'utf-8'
        self.lookup = TemplateLookup(directories=['/', base], input_encoding=self.inencoding,
                output_encoding=self.outencoding, encoding_errors='replace')

    def process(self, path, **kwargs):
        template = self.lookup.get_template(path)
        buf = FastEncodingBuffer(unicode=False, encoding=self.outencoding,
                errors='replace')
        context = Context(buf, **kwargs)
        template.render_context(context)
        data = context._pop_buffer().getvalue()
        return data

    def process_error(self):
        template = html_error_template()
        data = template.render()
        return data

