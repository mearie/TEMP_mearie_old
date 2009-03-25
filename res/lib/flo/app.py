"""WSGI application class.

One of most important piece of entire mearieflo code. It resolves given URL
and HTTP parameters via flo.resolve module, processes corresponding source file
via flo.process module(s), and finally returns final data.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context, HttpError
from .resolve import Resolver

import sys
import os, os.path
import mimetypes
import traceback

from beaker.cache import CacheManager

class Application(object):
    def __init__(self, base):
        self.base = os.path.abspath(base)
        self.caches = CacheManager()
        self.resolver = Resolver(self)
        self.processors = {}

    def processor_from_name(self, name): 
        if name not in self.processors:
            parts = name.split('.')
            obj = __import__('.'.join(parts[:-1]))
            for part in parts[1:]:
                obj = getattr(obj, part)
            self.processors[name] = obj(self)
        return self.processors[name]

    def get_cache(self, name, **kwargs):
        return self.caches.get_cache(name, **kwargs)

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            try:
                self.resolver.resolve(context)
                processor = context.conf.get_processor(self)
                processed = processor.process(context)
            except HttpError:
                raise # no need to set exception information.
            except:
                context.exc_info = sys.exc_info()
                context.internal_error()
        except HttpError, e:
            context.status = e.status

            if context.conf is None:
                errpaths = []
            else:
                errpaths = context.conf.error_paths(e.status)

            for path in errpaths:
                try:
                    context.content_type = 'text/html'
                    context.content_enc = None
                    processor = context.conf.get_processor(self)
                    processed = processor.process(context, open(path, 'rb').read())
                    break
                except:
                    context.exc_info = sys.exc_info()
            else:
                # default error page.
                context.content_type = 'text/plain'
                context.content_enc = None
                processed = 'HTTP ' + context.header_line + \
                        '\n(No custom error page is supplied, or all caused internal error.)\n\n'
                if context.exc_info is not None:
                    processed += ''.join(traceback.format_exception(*context.exc_info))

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

