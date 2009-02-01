"""WSGI application class.

One of most important piece of entire mearieflo code. It resolves given URL
and HTTP parameters via flo.resolve module, processes corresponding source file
via flo.process module(s), and finally returns final data.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context, HttpError
from .resolve import Resolver
from .process import Processor, mako as proc_mako, html_postproc as proc_htmlpost

import sys
import os, os.path
import mimetypes
import traceback

class Application(object):
    def __init__(self, base):
        self.base = base
        self.resolver = Resolver(base)
        self.processor = Processor()
        self.init_processor()

    def init_processor(self):
        self.processor.add(0, proc_mako.MakoProcessor(self.base))

        self.processor.add(100, proc_htmlpost.HTMLTreeReader())
        self.processor.add(101, proc_htmlpost.ReferencesInserter())
        self.processor.add(199, proc_htmlpost.HTMLTreeWriter())

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            self.resolver.resolve(context)

            processed = self.processor.process(context)
            if processed is None: # not preprocessed, verbatim
                if 'wsgi.file_wrapper' in environ:
                    data = environ['wsgi.file_wrapper'](open(context.path, 'rb'))
                else:
                    data = [open(context.path, 'rb').read()]
                size = os.stat(context.path).st_size
            else:
                data = [processed]
                size = len(processed)

            context.headers['Content-Type'] = context.content_type
            context.headers['Content-Length'] = str(size)
            if context.content_enc is not None:
                context.headers['Content-Encoding'] = context.content_enc
        except HttpError, e:
            context.status = e.status
            context.headers['Content-Type'] = 'text/plain'
            data = [e.header_line]
        except:
            data = traceback.format_exc()
            start_response('500 Internal Server Error',
                    [('Content-Type', 'text/plain'), ('Content-Length', str(len(data)))],
                    sys.exc_info())
            return [data]

        start_response(context.header_line, context.headers.items())
        return data

