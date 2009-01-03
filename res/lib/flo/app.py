"""WSGI application class.

One of most important piece of entire mearieflo code.
"""

from __future__ import absolute_import, division, with_statement

from .resolve import Resolver
from .preprocess import Preprocessor

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
        try:
            path, trail = self.resolver.resolve(environ['PATH_INFO'])
            if path is None:
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return ['cannot resolve path: ' + environ['PATH_INFO']]

            mimetype, encoding = self.resolve_type(path)
            if mimetype == 'text/html': # preprocessed
                data = [self.preproc.process(path, trail=trail)]
                size = len(data[0])
            else:
                if 'wsgi.file_wrapper' in environ:
                    data = environ['wsgi.file_wrapper'](open(path, 'rb'))
                else:
                    data = [open(path, 'rb').read()]
                size = os.stat(path).st_size

            headers = [('Content-Type', mimetype), ('Content-Length', str(size))]
            if encoding is not None:
                headers.append(('Content-Encoding', encoding))
            start_response('200 OK', headers)
            return data
        except:
            data = self.preproc.process_error()
            start_response('500 Internal Server Error',
                    [('Content-Type', 'text/html'), ('Content-Length', str(len(data)))],
                    sys.exc_info())
            return [data]

