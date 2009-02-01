"""Mako-based template preprocessor.
"""

from __future__ import absolute_import, division, with_statement

from mako.template import Template
from mako.lookup import TemplateLookup

class FloLookup(TemplateLookup):
    pass # TODO?

class MakoProcessor(object):
    input_type = ['text/html', 'application/xhtml+xml']
    output_type = 'text/html'

    def __init__(self, base, inencoding='utf-8', outencoding='utf-8'):
        self.base = base
        self.inencoding = inencoding
        self.outencoding = outencoding
        self.lookup = FloLookup(directories=['/', base], input_encoding=self.inencoding,
                output_encoding=self.outencoding, encoding_errors='replace')

    def __call__(self, context, data):
        if data is None:
            template = self.lookup.get_template(context.path)
        else:
            template = Template(uri=context.path, text=data, lookup=self.lookup,
                    module_filename=None, **self.lookup.template_args)
        data = template.render(flo=context)
        return data

