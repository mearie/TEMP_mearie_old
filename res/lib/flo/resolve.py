"""Resolver class, providing generic resolution process for mearieflo.
"""

from __future__ import absolute_import, division, with_statement

from .conf import Config
from .context import Context
from .http import is_langtag, parse_accept, parse_acceptlang, \
        match_accept, match_acceptlang

import os, os.path

class Resolver(object):
    def __init__(self, app):
        self.app = app
        self.base = os.path.normpath(app.base)

    def guess_type(self, context, name):
        """guess_type(self, context, name) -> (Content-Type, Content-Encoding)"""
        type, enc = context.conf.guess_type(name)
        langdep = False
        if type == 'text/html' or type == 'application/xhtml+xml':
            langdep = True
        return type, enc, langdep

    def parse_filename(self, context, filename):
        parts = filename.split('.')

        type = 'application/octet-stream'
        enc = None
        lang = None
        if len(parts) < 2:
            name = filename
        else:
            guessedtype, guessedenc, langdep = self.guess_type(context, filename)
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

    def select_candidate(self, candidates, accepts, acceptlangs):
        maxfname = None
        maxq = 0
        mini = 9999
        for fname, name, type, enc, lang in candidates:
            typeq, typei = match_accept(accepts, type)
            langq, langi = match_acceptlang(acceptlangs, lang)
            q = typeq * langq
            i = typei + langi
            if (maxq, -mini) < (q, -i):
                maxq = q
                mini = i
                maxfname = fname

        if maxq > 0: return maxfname
        return None

    def resolve(self, context):
        context.url = path = context.environ['PATH_INFO']
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
                context.path = newbase

                # prohibits the access to parents of document root.
                if not newbase.startswith(self.base):
                    context.not_found()

                if not os.path.isdir(newbase): break
                scriptbase = newbase
        else:
            component = 'index' # default filename
            if not path.endswith('/'):
                context.perm_redirect(path + '/')

        assert os.path.isdir(scriptbase)
        context.conf = Config(self.base, scriptbase)

        reqname, reqtype, reqenc, reqlang = self.parse_filename(context, component)
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

        # search for candidates.
        candidates = []
        for fname in os.listdir(scriptbase):
            fullname = os.path.join(scriptbase, fname)
            if not os.path.isfile(fullname): continue
            name, type, enc, lang = self.parse_filename(context, fname)
            if name == reqname:
                candidates.append((fname, name, type, enc, lang))

        varies = []
        if len(set((type, enc) for _, _, type, enc, _ in candidates)) > 1:
            varies.append('Accept')
        if len(set(lang for _, _, _, _, lang in candidates)) > 1:
            varies.append('Accept-Language')
        if varies:
            context.headers['Vary'] = ', '.join(varies)

        selected = self.select_candidate(candidates, accepts, acceptlangs)
        if selected is not None:
            context.path = os.path.join(scriptbase, selected)
            _, context.content_type, context.content_enc, context.lang = \
                    self.parse_filename(context, selected)
            context.trail = trail
            return context
        elif candidates:
            context.not_acceptable() # client explicitly rejects all candidates

        context.not_found()

