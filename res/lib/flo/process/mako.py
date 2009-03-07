"""Mako-based template preprocessor.
"""

from __future__ import absolute_import, division, with_statement

import os.path, posixpath

from mako.template import Template
from mako.lookup import TemplateCollection

class FloLookup(TemplateCollection):
    """Custom lookup class for path-dependent template lookup.
    """

    def __init__(self, base, **template_args):
        TemplateCollection.__init__(self)
        self.base = base
        self.template_args = template_args

    def preprocess(self, data):
        if '<%inherit' not in data and 'FLO_NOBASE' not in data:
            data = '<%inherit file=".flo/base.html"/>' + data
        return data

    def get_template(self, uri):
        return Template(uri=uri, filename=uri, lookup=self, module_filename=None,
                preprocessor=self.preprocess, **self.template_args)

    def make_template(self, uri, data):
        return Template(uri=uri, filename=uri, text=data, lookup=self, module_filename=None,
                preprocessor=self.preprocess, **self.template_args)

    def filename_to_uri(self, uri, filename):
        raise NotImplemented()

    def adjust_uri(self, uri, relativeto):
        relativeto = os.path.normpath(posixpath.dirname(relativeto))
        if uri.startswith('.flo/'):
            while relativeto.startswith(self.base):
                filename = os.path.join(relativeto, uri)
                if os.path.exists(filename): return filename
                relativeto = os.path.split(relativeto)[0]
            assert False
        else:
            return os.path.join(os.path.normpath(relativeto), uri)

class MakoProcessor(object):
    input_type = ['text/html', 'application/xhtml+xml']
    output_type = 'text/html'

    def __init__(self, base, inencoding='utf-8', outencoding='utf-8'):
        self.base = base
        self.inencoding = inencoding
        self.outencoding = outencoding
        self.lookup = FloLookup(base, input_encoding=self.inencoding,
                output_encoding=self.outencoding, encoding_errors='replace')

    def __call__(self, context, data):
        if data is None:
            template = self.lookup.get_template(context.path)
        else:
            template = self.lookup.make_template(context.path, data)
        data = template.render(flo=context)
        return data

