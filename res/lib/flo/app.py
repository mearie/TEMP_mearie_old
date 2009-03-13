"""WSGI application class.

One of most important piece of entire mearieflo code. It resolves given URL
and HTTP parameters via flo.resolve module, processes corresponding source file
via flo.process module(s), and finally returns final data.
"""

from __future__ import absolute_import, division, with_statement

from beaker.cache import CacheManager

from .context import Context, HttpError
from .resolve import Resolver
from .process import Processor

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
        self.processor = Processor(self)

        self.init_processor()
        self.cachemgr = CacheManager(type='memory')
        self.cache = self.cachemgr.get_cache('woah')

    def init_processor(self):
        from .process.mako import MakoProcessor
        self.processor.add(0, MakoProcessor(self.base))

        from .process.html_sanitize import HTMLSanitizer
        self.processor.add(10, HTMLSanitizer())

        # XML tree operations
        from .process.xmltree import XMLTreeReader, XMLTreeWriter
        from .process.references import ReferenceProcessor
        from .process.html_postproc import ImageFramer, MathReplacer, \
                AbbreviationFiller
        self.processor.add(100, XMLTreeReader(self.base))
        self.processor.add(110, ReferenceProcessor())
        self.processor.add(120, ImageFramer())
        self.processor.add(120, MathReplacer())
        self.processor.add(120, AbbreviationFiller())
        self.processor.add(199, XMLTreeWriter())

    def get_cache(self, name, **kwargs):
        return self.caches.get_cache(name, **kwargs)

    def __call__(self, environ, start_response):
        context = Context(self, environ)

        try:
            try:
                self.resolver.resolve(context)
                processed = self.cache.get_value(context.path,
                        createfunc=lambda: self.processor.process(context), expiretime=60)
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
                    processed = self.processor.process(context, open(path, 'rb').read())
                    break
                except: pass
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

