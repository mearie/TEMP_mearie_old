"""WSGI application class.

One of most important piece of entire mearieflo code.
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

    def resolve_type(self, path):
        mimetype = mimetypes.guess_type(os.path.basename(path))
        if mimetype is None:
            if path.endswith('.py'):
                return ('text/plain', None)
            return ('application/octet-stream', None)
        return mimetype

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            self.resolver.resolve(context)

            mimetype, encoding = self.resolve_type(context.path)
            if mimetype == 'text/html': # preprocessed
                data = [self.preproc.process(context)]
                size = len(data[0])
            else:
                if 'wsgi.file_wrapper' in environ:
                    data = environ['wsgi.file_wrapper'](open(context.path, 'rb'))
                else:
                    data = [open(context.path, 'rb').read()]
                size = os.stat(context.path).st_size

            context.headers['Content-Type'] = mimetype
            context.headers['Content-Length'] = str(size)
            if encoding is not None:
                context.headers['Content-Encoding'] = encoding
            start_response(context.header_line, context.headers.items())
            return data
        except HttpError, e:
            message = context.header_line
            context.headers['Content-Type'] = 'text/plain'
            start_response(message, context.headers.items())
            return [message]
        except:
            data = self.preproc.process_error()
            start_response('500 Internal Server Error',
                    [('Content-Type', 'text/html'), ('Content-Length', str(len(data)))],
                    sys.exc_info())
            return [data]

