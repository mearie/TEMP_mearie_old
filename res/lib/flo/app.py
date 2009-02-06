"""WSGI application class.

One of most important piece of entire mearieflo code. It resolves given URL
and HTTP parameters via flo.resolve module, processes corresponding source file
via flo.process module(s), and finally returns final data.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context, HttpError
from .resolve import Resolver
from .process import Processor, \
        mako as proc_mako, html_postproc as proc_htmlpost, \
        html_sanitize as proc_htmlsanitize

import sys
import os, os.path
import mimetypes
import traceback

class Application(object):
    def __init__(self, base):
        self.base = os.path.abspath(base)
        self.resolver = Resolver(self.base)
        self.processor = Processor()
        self.init_processor()

    def init_processor(self):
        self.processor.add(0, proc_mako.MakoProcessor(self.base))
        self.processor.add(10, proc_htmlsanitize.HTMLSanitizer())

        self.processor.add(100, proc_htmlpost.HTMLTreeReader(self.base))
        self.processor.add(110, proc_htmlpost.ReferencesInserter())
        self.processor.add(120, proc_htmlpost.ImageFramer())
        self.processor.add(199, proc_htmlpost.HTMLTreeWriter())

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            try:
                self.resolver.resolve(context)
                processed = self.processor.process(context)
            except HttpError:
                raise # no need to set exception information.
            except:
                context.exc_info = sys.exc_info()
                context.internal_error()
        except HttpError, e:
            context.status = e.status

            # default error page.
            context.content_type = 'text/plain'
            context.content_enc = None
            data = 'HTTP ' + context.header_line + '\n(No custom error page is supplied.)\n\n'
            if context.exc_info is not None:
                data += ''.join(traceback.format_exception(*context.error_excinfo))

            if context.conf is not None:
                for path in context.conf.error_paths(e.status):
                    try:
                        data = open(path, 'rb').read()
                        context.content_type = 'text/html'
                        context.content_enc = None
                        break
                    except: pass

            processed = self.processor.process(context, data)

        if processed is None: # not preprocessed, verbatim
            if 'wsgi.file_wrapper' in environ:
                data = environ['wsgi.file_wrapper'](open(context.path, 'rb'))
            else:
                data = [open(context.path, 'rb').read()]
            size = os.stat(context.path).st_size
        else:
            data = [processed]
            size = len(processed)

        context.headers['Content-Type'] = context.content_type or 'application/octet-stream'
        context.headers['Content-Length'] = str(size)
        if context.content_enc is not None:
            context.headers['Content-Encoding'] = context.content_enc

        start_response(context.header_line, context.headers.items())
        return data

