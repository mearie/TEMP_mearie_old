"""Resolver class, providing generic resolution process for mearieflo.
"""

from __future__ import absolute_import, division, with_statement

from .conf import ConfigCache
from .context import Context
from .http import HttpError, is_langtag

import os, os.path
import posixpath
import urlparse

class Resolver(object):
    def __init__(self, app):
        self.app = app
        self.base = os.path.normpath(app.base)
        self.configcache = ConfigCache(app)

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
            typeq, typei = accepts.match_with_index(type)
            langq, langi = acceptlangs.match_with_index(lang)
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

        if os.sep != '/' and os.sep in path:
            # simple sanity check for windows (or VMS?) systems.
            context.forbidden()
        if '/.flo/' in path:
            # internal directory should not be visible, unless rewriting rule
            # explicitly maps other URL to it.
            context.not_found()

        # discard /./s and /../s. it also hopefully eliminates possible local
        # filesystem exploit using excessive /../s.
        assert posixpath.normpath('/foo/../../bar/') == '/bar'
        if path.endswith('/'):
            path = posixpath.normpath(path) + '/'
        else:
            path = posixpath.normpath(path)

        pos = 0
        while pos < len(path):
            conf = self.configcache.get(scriptbase)
            httpcode, newpath = conf.rewrite_url(path[pos+1:])
            newpath = urlparse.urljoin(path[:pos+1], newpath)

            if not 200 <= httpcode < 300:
                context.status = httpcode
                if 300 <= httpcode < 400:
                    context.headers['Location'] = newpath
                raise HttpError(httpcode)

            if not newpath.startswith('/'):
                raise ValueError('External URL is not allowed for internal redirection')

            if path != newpath:
                # minimizes total number of URL rewriting by using common prefix;
                # for example, if in the directory "/foo/bar", URL "/foo/bar/quux/blah"
                # is rewritten to "/foo/quux/blah", we can immediately check rewriting
                # rules for "/foo/quux" because "/", "/foo" is already checked.
                pos = posixpath.commonprefix([path, newpath]).rfind('/')
                path = newpath
                scriptbase = os.path.join(self.base, *path[1:pos].split('/'))

            npos = path.find('/', pos+1)
            if npos < 0: npos = len(path)
            component = path[pos+1:npos]
            pos = npos

            if not component: continue

            assert component != '.' and component != '..'
            newbase = os.path.join(scriptbase, component)
            context.path = newbase

            if not os.path.isdir(newbase): break
            scriptbase = newbase
        else:
            component = 'index' # default filename
            if not path.endswith('/'):
                context.perm_redirect(path + '/')

        assert os.path.isdir(scriptbase)
        context.conf = self.configcache.get(scriptbase)

        reqname, reqtype, reqenc, reqlang = self.parse_filename(context, component)
        trail = path[pos:]

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

        selected = self.select_candidate(candidates, context.accepts,
                context.acceptlangs)
        if selected is not None:
            context.path = os.path.join(scriptbase, selected)
            _, context.content_type, context.content_enc, context.lang = \
                    self.parse_filename(context, selected)
            context.trail = trail
            return context
        elif candidates:
            context.not_acceptable() # client explicitly rejects all candidates

        context.not_found()

