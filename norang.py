#!/usr/bin/env python
# norang preprocessor
# Copyright (c) 2009, Kang Seonghoon.

from __future__ import absolute_import, division, with_statement

__version__ = '0.0.20090703'

import sys
import os
import os.path
import shutil

import markdown
import mako.lookup

class Processor(object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

        self.working = set([('directory', '/')])
        self.working_data = {} 
        self.finished = set()
        self.created = set() # in the destination directory

        self.markdownctx = markdown.Markdown(
                extensions=['meta'], extension_configs={},
                safe_mode=False, output_format='xhtml1')
        self.makoctx = mako.lookup.TemplateLookup(directories=[source],
                input_encoding='utf-8', output_encoding='utf-8',
                format_exceptions=True)

    def as_source(self, path):
        return os.path.join(self.source, path.lstrip('/'))

    def as_destination(self, path):
        return os.path.join(self.destination, path.lstrip('/'))

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
                self.add(('directory', os.path.join(path, f)))
            elif f.endswith('.md'):
                self.add(('markdown', os.path.join(path, f)))
            else:
                self.add(('copy', os.path.join(path, f)))

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
        tmpl = self.makoctx.get_template(data['template'])
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
        while self.working:
            spec = self.working.pop()
            data = self.working_data.pop(spec, None)
            print >>sys.stderr, 'processing spec %r' % (spec,)
            self.handle(spec, data)
            self.finished.add(spec)


def process_markdown(input, output, encoding='utf-8'):
    text = open(input, 'r').read().decode(encoding)
    html = md.convert(text)
    #print md.Meta
    open(output, 'w').write(html.encode(encoding))
    md.reset()

def process(source, destination):
    for base, dirs, files in os.walk(root):
        for name in files:
            if not name.endswith('.txt'): continue
            input = os.path.join(base, name)
            output = os.path.join(base, name[:-4])
            print >>sys.stderr, 'processing', input
            process_markdown(input, output)

def main(argv):
    if len(argv) < 3:
        print >>sys.stderr, 'norang %s' % __version__
        print >>sys.stderr, 'Type "%s --help" for usage.' % argv[0]
        return 1

    #process(argv[1], argv[2])
    Processor(argv[1], argv[2]).process()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

