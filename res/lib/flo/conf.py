"""Configuration class.

All configurations, datas such as SQLite database, caches etc. is saved in
.flo directory, which can contain the following things:

- root: Empty, present only if this directory is site root.
- local.conf: Configures basic things like default language.
- local.py: Extended configuration with Python script.
- base.html: Base template inherited by other pages.
- http###.html: HTTP error/redirection templates.
- rewrite.conf: Configures URL-to-path mapping.
- types.conf: Additional media type definition.
- models/*.py: Database schema definition.
- db/*.db: SQLite database, created according the schema.
- cache/#/##/*: Temporary caches, organized with SHA-1 hash.
"""

from __future__ import absolute_import, division, with_statement

from .util import nenumerate

import os, os.path
import re
import copy
import httplib
import mimetypes
import ConfigParser as configparser

class Config(object):
    def __init__(self, parent, dir):
        self.parent = parent
        self.dir = os.path.normpath(dir).rstrip(os.sep) + os.sep
        assert self.parent is None or self.dir.startswith(self.parent.dir)

        self.conf = None
        self.types = None
        self.rules = None

    def paths(self, *trail):
        conf = self
        while conf is not None:
            yield os.path.join(conf.dir, *trail)
            conf = conf.parent

    def flo_paths(self):
        return self.paths('.flo')

    def error_paths(self, status):
        return self.paths('.flo', 'http%03d.html' % status)

    def read_conf(self):
        if self.parent is None:
            self.conf = configparser.SafeConfigParser()
        else:
            if self.parent.conf is None:
                self.parent.read_conf()
            self.conf = copy.deepcopy(self.parent.conf)

        path = os.path.join(self.dir, '.flo', 'local.conf')
        self.conf.read(path)

        try:
            self.internal_encoding = self.conf.get('global', 'encoding')
        except:
            self.internal_encoding = 'utf-8'

    def read_types(self):
        if self.parent is None:
            self.types = mimetypes.MimeTypes()
        else:
            if self.parent.types is None:
                self.parent.read_types()
            self.types = copy.deepcopy(self.parent.types)

        path = os.path.join(self.dir, '.flo', 'types.conf')
        if os.path.exists(path):
            self.types.read(path)

    def read_rules(self):
        self.rules = []

        path = os.path.join(self.dir, '.flo', 'rewrite.conf')
        if os.path.exists(path):
            curpass = []
            for lineno, line in nenumerate(open(path, 'rtU'), start=1):
                line = line.strip()
                if not line or line[0] == '#' or line[0] == ';': continue

                line = line.split()
                if line[0] == '-':
                    if curpass: self.rules.append(curpass)
                    curpass = []
                    continue

                if len(line) == 2:
                    pattern, repl = line
                    code = 0
                elif len(line) == 3:
                    pattern, repl, code = line
                    try:
                        code = int(code)
                        if code not in httplib.responses: raise ValueError
                    except:
                        raise ValueError('Invalid HTTP code at line %d' % lineno)
                else:
                    raise ValueError('Invalid rule at line %d' % lineno)

                if pattern == '-':
                    raise ValueError('Empty pattern at line %d' % lineno)
                pattern = re.compile(pattern)
                if repl == '-':
                    repl = ''

                curpass.append((pattern, repl, code))

            if curpass: self.rules.append(curpass)

    def __getitem__(self, key):
        if self.conf is None:
            self.read_conf()

        try:
            sect, opt = key
            opttype = unicode
            optdefault = None
        except ValueError:
            sect, opt, opttype = key
            if type(opttype) is not type:
                optdefault = opttype
                opttype = type(opttype)

        try:
            if issubclass(opttype, str):
                return self.conf.get(sect, opt)
            elif issubclass(opttype, unicode):
                return self.conf.get(sect, opt).decode(self.internal_encoding)
            elif issubclass(opttype, (int, long)):
                return self.conf.getint(sect, opt)
            elif issubclass(opttype, float):
                return self.conf.getfloat(sect, opt)
            elif issubclass(opttype, bool):
                return self.conf.getboolean(sect, opt)
            else:
                assert False
        except configparser.NoOptionError:
            if optdefault is None: raise
            return optdefault

    def guess_type(self, filename):
        if self.types is None:
            self.read_types()
        return self.types.guess_type(filename)

    def rewrite_url(self, url):
        """rewrite_url(url) -> (HTTP code, rewritten URL)

        Rewrites given URL relative to current directory. Rewritten URL is
        assumed to be relative to current directory but also can be absolute
        URL -- its interpretation is up to caller."""

        if self.rules is None:
            self.read_rules()

        for curpass in self.rules:
            for pattern, repl, code in curpass:
                result = pattern.match(url)
                if result is not None:
                    url = result.expand(repl)
                    if code: # terminates all rewriting
                        if not 200 <= code < 600:
                            raise ValueError('invalid HTTP status code %d' % code)
                        return code, url
                    else: # terminates current pass only
                        break
        return httplib.OK, url

class ConfigCache(object):
    def __init__(self, app):
        self.app = app
        self.cache = app.get_cache('flodirconf', type='memory', expiretime=30)

    def load(self, path):
        if path == self.app.base:
            parentconf = None
        else:
            parentconf = self.get(os.path.split(path)[0])
        return Config(parentconf, path)

    def get(self, path):
        return self.cache.get(path, createfunc=lambda: self.load(path))

    def forget(self, path):
        raise NotImplemented() # how to?

