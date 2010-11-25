# webase -- too simple to be a Python web framework
# written by Kang Seonghoon; dedicated to public domain.

from __future__ import absolute_import, division, with_statement

import sys
import re
import httplib
import cgi
import traceback
from operator import attrgetter

from odict import odict

__all__ = ['Application']

# replacement of FieldStorage which __getitem__ returns string.
class FieldStorageEx(cgi.FieldStorage):
    getitem = cgi.FieldStorage.__getitem__

    def __getitem__(self, key):
        value = self.getitem(key)
        if isinstance(value, list): value = value[0]
        return value.value

    # get* functions references __getitem__ and needs adjustment.
    def getvalue(self, key, default=None):
        if key in self:
            value = self.getitem(key)
            if isinstance(value, list):
                return map(attrgetter('value'), value)
            else:
                return value.value
        else:
            return default

    def getfirst(self, key, default=None):
        if key in self:
            value = self.getitem(key)
            if isinstance(value, list): value = value[0]
            return value.value
        else:
            return default

    def getlist(self, key):
        if key in self:
            value = self.getitem(key)
            if isinstance(value, list):
                return map(attrgetter('value'), value)
            else:
                return [value.value]
        else:
            return []

class Environment(object):
    def __init__(self, app, environ, start_response, func, args=(), kwargs={}):
        self.app = app
        self.environ = environ
        self.start_response = start_response
        self.func = func
        self.func_args = args
        self.func_kwargs = kwargs

        self.header_sent = False
        self.code = None
        self.headers = odict([('Content-Type', 'text/html')])
        self.reason = None

        self.GET = FieldStorageEx(None,
                environ={'REQUEST_METHOD': 'GET', 'QUERY_STRING': self.environ['QUERY_STRING']})
        self.POST = None
        if self.environ['REQUEST_METHOD'].upper() not in ('GET', 'HEAD'):
            self.POST = FieldStorageEx(self.environ['wsgi.input'], environ=self.environ)

    def __iter__(self):
        try:
            self.header_sent = False
            iterable = self.func(self, *self.func_args, **self.func_kwargs)
            try:
                if hasattr(iterable, 'next'):
                    data = iterable.next()
                    nodata = last = False
                else:
                    data = iterable
                    nodata = (data is None)
                    last = True
            except StopIteration:
                nodata = last = True

            code = self.code or 200
            headerline = '%d %s' % (code, self.reason or httplib.responses[code])
            self.start_response(headerline, self.headers.items())
            self.header_sent = True
            if last:
                if not nodata: yield data
                return

            while True:
                yield data
                try:
                    data = iterable.next()
                except StopIteration:
                    break
        except:
            excinfo = sys.exc_info()
            traceback.print_exception(file=sys.stderr, *excinfo)

            if self.header_sent:
                handler = self.app.error_handler(self, excinfo)
            else:
                handler = Environment(self.app, self.environ, self.start_response,
                        self.app.error_handler, args=(excinfo,))
            for data in handler:
                yield data

    def __getitem__(self, key):
        return self.environ[key]

    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    def status(self, code, reason=None):
        if self.header_sent:
            raise RuntimeError('Cannot change response header as it is already sent.')
        if self.code is not None:
            raise RuntimeError('Environment.status cannot be called twice or more.')
        self.code = code
        self.reason = reason

    def header(self, key, value):
        if self.header_sent:
            raise RuntimeError('Cannot change response header as it is already sent.')
        self.headers[key] = str(value)

class Application(object):
    def __init__(self, show_traceback=True):
        self.handlers = []
        self.error_handler = self._default_error_handler
        self.missing_handler = self._default_missing_handler

        self.show_traceback = show_traceback

    def handle(self, pattern):
        def inner(func):
            self.handlers.append((re.compile(pattern), func))
            return func
        return inner

    def handle_error(self):
        def inner(func):
            self.error_handler = func
            return func
        return inner

    def handle_missing(self):
        def inner(func):
            self.missing_handler = func
            return func
        return inner

    def _default_error_handler(self, env, excinfo):
        yield ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n'
               '<html><head><title>500 Internal Server Error</title></head><body><h1>Internal Server Error</h1>'
                '<p>The server encountered an internal error and was unable to complete your request.</p>')
        if self.show_traceback:
            yield ('<p>Python traceback:</p><pre>%s</pre>' %
                   ''.join(traceback.format_exception(*excinfo)).replace('&', '&amp;')
                     .replace('<', '&lt;').replace('>', '&gt;'))
        else:
            yield '<p>More information about this error may be available in the server error log.</p>'
        yield '</body></html>'

    def _default_missing_handler(self, env):
        yield ('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n'
               '<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1>'
               '<p>The requested URL ' + env['PATH_INFO'] + ' was not found on this server.</p>'
               '</body></html>')

    def __call__(self, environ, start_response):
        result = None

        try:
            path = environ['PATH_INFO']
            for pattern, func in self.handlers:
                m = pattern.match(path)
                if m is not None:
                    return Environment(self, environ, start_response, func, kwargs=m.groupdict())
            return Environment(self, environ, start_response, self.missing_handler)
        except:
            # this only handles internal error. Environment.__iter__ should handle the remaining cases.
            excinfo = sys.exc_info()
            traceback.print_exception(file=sys.stderr, *excinfo)
            return Environment(self, environ, start_response, self.error_handler, args=(excinfo,))

