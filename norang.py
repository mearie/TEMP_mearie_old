#!/usr/bin/env python
# norang preprocessor
# Copyright (c) 2009, Kang Seonghoon.

from __future__ import absolute_import, division, with_statement

__version__ = '0.0.20090703'

import sys
import os
import os.path
import shutil
import ConfigParser as configparser

import markdown
import mako.lookup

class Settings(object):
    def __init__(self, filenames):
        self.read_conf(filenames)

    def read_conf(self, filenames):
        self.conf = configparser.SafeConfigParser()
        self.conf.read(filenames)

        try:
            self.internal_encoding = self.conf.get('global', 'encoding')
        except:
            self.internal_encoding = 'utf-8'

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

class Processor(object):
    def __init__(self, source, destination, settings):
        self.source = source
        self.destination = destination
        self.settings = settings

        self.working = set()
        self.working_data = {} 
        self.requires = {}
        self.finished = set()
        self.created = set() # in the destination directory

        self.markdownctx = markdown.Markdown(
                extensions=['meta'], extension_configs={},
                safe_mode=False, output_format='xhtml1')
        self.makoctx = mako.lookup.TemplateLookup(directories=[source],
                input_encoding='utf-8', output_encoding='utf-8',
                format_exceptions=True)

    def as_source(self, path):
        return os.path.join(self.source, os.path.normpath(path.lstrip('/')))

    def as_destination(self, path):
        return os.path.join(self.destination, os.path.normpath(path.lstrip('/')))

    def add(self, spec, data=None):
        if spec not in self.finished:
            print >>sys.stderr, 'adding spec %r' % (spec,)
            self.working.add(spec)
            self.working_data[spec] = data

    def handle_directory(self, path, data):
        realpath = self.as_source(path)
        for f in os.listdir(realpath):
            if f.startswith('.'): continue
            realf = os.path.join(realpath, f)
            if os.path.isdir(realf):
                self.add(('directory', path + '/' + f))
            elif f.endswith('.md'):
                self.add(('markdown', path + '/' + f))
            else:
                self.add(('copy', path + '/' + f))

    def handle_markdown(self, path, data):
        tmpl = self.makoctx.get_template(path)
        text = tmpl.render_unicode()
        html = self.markdownctx.convert(text)
        result = dict((str(k), '\n'.join(v)) for k, v in self.markdownctx.Meta.items())
        result['contents'] = html
        self.markdownctx.reset()

        targetpath = os.path.splitext(path)[0] + '.html'
        self.add(('templated_html', targetpath), result)

    def handle_templated_html(self, path, data):
        try:
            template = data['template']
        except KeyError:
            template = self.settings['processor.templated_html', 'default_template']
        tmpl = self.makoctx.get_template(template)
        html = tmpl.render(**data)

        target = self.as_destination(path)
        targetdir = os.path.dirname(target)
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)
        open(target, 'w').write(html)

    def handle_copy(self, path, data):
        target = self.as_destination(path)
        targetdir = os.path.dirname(target)
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)
        shutil.copyfile(self.as_source(path), target)

    def handle(self, spec, data):
        return getattr(self, 'handle_' + spec[0])(*spec[1:], data=data)

    def process(self):
        self.add(('directory', ''))
        while self.working:
            spec = self.working.pop()
            data = self.working_data.pop(spec, None)
            print >>sys.stderr, 'processing spec %r' % (spec,)
            self.handle(spec, data)
            self.finished.add(spec)

def main(argv):
    if len(argv) < 3:
        print >>sys.stderr, 'norang %s' % __version__
        print >>sys.stderr, 'Type "%s --help" for usage.' % argv[0]
        return 1

    source = argv[1]
    destination = argv[2]
    settings = Settings([os.path.join(source, 'norang.ini')])
    Processor(source, destination, settings).process()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

