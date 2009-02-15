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
import ConfigParser as configparser

class Config(object):
    def __init__(self, base, dir):
        # append a slash if there is no trailing slash.
        self.base = os.path.normpath(base).rstrip(os.sep) + os.sep
        self.dir = os.path.normpath(dir).rstrip(os.sep) + os.sep
        assert self.dir[:len(self.base)] == self.base
        self.dirdepth = self.dir[len(self.base):].count(os.sep)

        self.localconf = None
        self.encoding = None

    def paths(self, *trail):
        dir = self.dir
        yield os.path.join(dir, *trail)
        for i in xrange(self.dirdepth):
            dir = os.path.join(dir, '..')
            yield os.path.join(dir, *trail)

    def flo_paths(self):
        return self.paths('.flo')

    def error_paths(self, status):
        return self.paths('.flo', 'http%03d.html' % status)

    def read_localconf(self):
        self.localconf = configparser.SafeConfigParser()
        self.localconf.read(os.path.join(self.dir, '.flo', 'local.conf'))

        try:
            self.encoding = self.localconf.get('global', 'encoding')
        except:
            self.encoding = 'utf-8'

    def __getitem__(self, key):
        if self.localconf is None: self.read_localconf()

        try:
            sect, opt = key
            type = unicode
        except ValueError:
            sect, opt, type = key

        if type is str:
            return self.localconf.get(sect, opt)
        elif type is unicode:
            return self.localconf.get(sect, opt).decode(self.encoding)
        elif type is int or type is long:
            return self.localconf.getint(sect, opt)
        elif type is float:
            return self.localconf.getfloat(sect, opt)
        elif type is bool:
            return self.localconf.getboolean(sect, opt)
        else:
            assert False
