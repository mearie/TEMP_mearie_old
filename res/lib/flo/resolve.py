"""Resolver class, providing generic resolution process for mearieflo.
"""

from __future__ import absolute_import, division, with_statement

from .context import Context
from .http import is_langtag, parse_accept, parse_acceptlang, \
        match_accept, match_acceptlang

from mako.lookup import TemplateLookup

import os, os.path
import mimetypes

class Resolver(object):
    def __init__(self, base):
        self.base = os.path.normpath(base)
        self.typesdb = mimetypes.MimeTypes()

        # TODO move to separate file
        self.typesdb.add_type('text/plain', '.py')

    def guess_type(self, name):
        """guess_type(self, name) -> (Content-Type, Content-Encoding)"""
        type, enc = self.typesdb.guess_type(name)
        langdep = False
        if type == 'text/html' or type == 'application/xhtml+xml':
            langdep = True
        return type, enc, langdep

    def parse_filename(self, filename):
        parts = filename.split('.')

        type = 'application/octet-stream'
        enc = None
        lang = None
        if len(parts) < 2:
            name = filename
        else:
            guessedtype, guessedenc, langdep = self.guess_type(filename)
            if guessedtype is not None:
                # don't strip extension if guess is failed.
                type = guessedtype
                enc = guessedenc
                parts.pop()

            for i in xrange(len(parts)-1, 0, -1):
                if langdep and lang is None and is_langtag(parts[i]):
                    lang = parts[i]
                    parts.pop(i)
            name = '.'.join(parts)

        return name, type, enc, lang

    def resolve(self, context):
        context.path = path = context.environ['PATH_INFO']
        assert path.startswith('/')

        scriptbase = self.base
        if not os.path.isdir(scriptbase):
            context.not_found()

        pos = 0
        while pos < len(path):
            npos = path.find('/', pos+1)
            if npos < 0: npos = len(path)
            component = path[pos+1:npos]
            pos = npos
            if component:
                if component == '..':
                    newbase = os.path.split(scriptbase)[0]
                else:
                    newbase = os.path.join(scriptbase, component)
                if not newbase.startswith(self.base):
                    context.not_found()
                if not os.path.isdir(newbase): break
                scriptbase = newbase
        else:
            component = 'index' # default filename
            if not path.endswith('/'):
                context.perm_redirect(path + '/')

        assert os.path.isdir(scriptbase)
        reqname, reqtype, reqenc, reqlang = self.parse_filename(component)
        trail = path[pos:]

        try:
            accepts = [(1000, (None, None), [])]
            if 'HTTP_ACCEPT' in context.environ:
                accepts = parse_accept(context.environ['HTTP_ACCEPT'])
        except ValueError:
            pass
        try:
            acceptlangs = [(1000, ())]
            if 'HTTP_ACCEPT_LANGUAGE' in context.environ:
                acceptlangs = parse_acceptlang(context.environ['HTTP_ACCEPT_LANGUAGE'])
        except ValueError:
            pass

        maxfname = None
        maxq = 0
        mini = 9999
        found = False
        for fname in os.listdir(scriptbase):
            fullname = os.path.join(scriptbase, fname)
            if not os.path.isfile(fullname): continue
            name, type, enc, lang = self.parse_filename(fname)
            if name == reqname:
                found = True
                typeq, typei = match_accept(accepts, type)
                langq, langi = match_acceptlang(acceptlangs, lang)
                q = typeq * langq
                i = typei + langi
                if (maxq, -mini) < (q, -i):
                    maxq = q
                    mini = i
                    maxfname = fname

        # TODO: Vary header

        if maxq > 0:
            context.path = os.path.join(scriptbase, maxfname)
            _, context.content_type, context.content_enc, context.lang = \
                    self.parse_filename(maxfname)
            context.trail = trail
            return context
        elif found:
            context.not_acceptable() # client explicitly rejects all candidates

        context.not_found()

