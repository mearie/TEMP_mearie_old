"""WSGI application class.

One of most important piece of entire mearieflo code. It resolves given URL
and HTTP parameters via flo.resolve module, processes corresponding source file
via flo.process module(s), and finally returns final data.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context, HttpError
from .resolve import Resolver
from .process import Preprocessor

import sys
import os, os.path
import mimetypes

class Application(object):
    def __init__(self, base):
        self.resolver = Resolver(base)
        self.preproc = Preprocessor(base)

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            self.resolver.resolve(context)

            if context.content_type == 'text/html': # preprocessed
                data = [self.preproc.process(context).strip()]
                size = len(data[0])
            else:
                if 'wsgi.file_wrapper' in environ:
                    data = environ['wsgi.file_wrapper'](open(context.path, 'rb'))
                else:
                    data = [open(context.path, 'rb').read()]
                size = os.stat(context.path).st_size

            context.headers['Content-Type'] = context.content_type
            context.headers['Content-Length'] = str(size)
            if context.content_enc is not None:
                context.headers['Content-Encoding'] = context.content_enc
        except HttpError, e:
            context.status = e.status
            context.headers['Content-Type'] = 'text/plain'
            data = [e.header_line]
        except:
            data = self.preproc.process_error()
            start_response('500 Internal Server Error',
                    [('Content-Type', 'text/html'), ('Content-Length', str(len(data)))],
                    sys.exc_info())
            return [data]

        start_response(context.header_line, context.headers.items())
        return data

