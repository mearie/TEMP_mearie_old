"""WSGI application class.

One of most important piece of entire mearieflo code.
"""

from __future__ import absolute_import, division, with_statement

#from . import resolve
from . import preprocess

import os, os.path
import mimetypes

class Application(object):
    def __init__(self, base):
        self.base = base
        self.preproc = preprocess.Preprocessor(base)

    def resolve_url(self, path):
        path = os.path.normpath(path.lstrip('/'))
        if path.startswith('..'): path = ''
        return os.path.join(self.base, path)

    def resolve_type(self, path):
        mimetype = mimetypes.guess_type(os.path.basename(path))
        if mimetype is None:
            if path.endswith('.py'):
                return ('text/plain', None)
            return ('application/octet-stream', None)
        return mimetype

    def __call__(self, environ, start_response):
        try:
            path = self.resolve_url(environ['PATH_INFO'])
            if os.path.isdir(path):
                path = os.path.join(path, 'index')
            if os.path.splitext(path)[1] == '':
                path += '.html'

            if not os.path.exists(path):
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return ['cannot resolve path: ' + environ['PATH_INFO']]

            mimetype, encoding = self.resolve_type(path)
            if mimetype == 'text/html': # preprocessed
                relpath = path[len(self.base):]
                data = [self.preproc.process(relpath)]
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
                    [('Content-Type', 'text/html'), ('Content-Length', str(len(data)))])
            return [data]

