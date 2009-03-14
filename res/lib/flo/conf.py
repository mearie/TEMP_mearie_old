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

import os, os.path
import copy
import mimetypes
import ConfigParser as configparser

class Config(object):
    def __init__(self, parent, dir):
        self.parent = parent
        self.dir = os.path.normpath(dir).rstrip(os.sep) + os.sep
        assert self.parent is None or self.dir.startswith(self.parent.dir)

        self.localconf = None
        self.localtypes = None
        self.encoding = None

    def paths(self, *trail):
        conf = self
        while conf is not None:
            yield os.path.join(conf.dir, *trail)
            conf = conf.parent

    def flo_paths(self):
        return self.paths('.flo')

    def error_paths(self, status):
        return self.paths('.flo', 'http%03d.html' % status)

    def read_localconf(self):
        if self.parent is None:
            self.localconf = configparser.SafeConfigParser()
        else:
            if self.parent.localconf is None:
                self.parent.read_localconf()
            self.localconf = copy.deepcopy(self.parent.localconf)

        path = os.path.join(self.dir, '.flo', 'local.conf')
        self.localconf.read(path)

        try:
            self.encoding = self.localconf.get('global', 'encoding')
        except:
            self.encoding = 'utf-8'

    def read_localtypes(self):
        if self.parent is None:
            self.localtypes = mimetypes.MimeTypes()
        else:
            if self.parent.localtypes is None:
                self.parent.read_localtypes()
            self.localtypes = copy.deepcopy(self.parent.localtypes)

        path = os.path.join(self.dir, '.flo', 'types.conf')
        if os.path.exists(path):
            self.localtypes.read(path)

    def __getitem__(self, key):
        if self.localconf is None:
            self.read_localconf()

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
                return self.localconf.get(sect, opt)
            elif issubclass(opttype, unicode):
                return self.localconf.get(sect, opt).decode(self.encoding)
            elif issubclass(opttype, (int, long)):
                return self.localconf.getint(sect, opt)
            elif issubclass(opttype, float):
                return self.localconf.getfloat(sect, opt)
            elif issubclass(opttype, bool):
                return self.localconf.getboolean(sect, opt)
            else:
                assert False
        except configparser.NoOptionError:
            if optdefault is None: raise
            return optdefault

    def guess_type(self, filename):
        if self.localtypes is None:
            self.read_localtypes()
        return self.localtypes.guess_type(filename)

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
        raise NotImplemented # how to?

