#!/usr/bin/env python
"""Command line interface to mearieflo."""

from __future__ import absolute_import, division, with_statement

if __name__ == '__main__':
    # we are not yet in the package!
    import sys, flo.main
    sys.exit(flo.main.main(sys.argv))

from . import __version__
from .app import Application

import sys
import getopt
from wsgiref.simple_server import make_server


def cmd_serve(args):
    port = 8080

    opts, args = getopt.getopt(args, 'p:', ['port='])
    for o, a in opts:
        if o in ('-p', '--port'):
            port = int(a)
        else:
            assert False

    if len(args) == 0:
        args = ['.'] # implicit path

    app = Application(args[0])
    server = make_server('', port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass # don't cause traceback


def main(args):
    if len(args) < 2:
        print >>sys.stderr, 'mearieflo %s' % __version__
        print >>sys.stderr, 'Type \'%s help\' for usage.' % args[0]
        return 0

    cmd = args[1]
    try:
        if cmd == 'serve':
            return cmd_serve(args[2:])
        else: #if cmd == 'help':
            return cmd_help(args[2:])
    except getopt.GetoptError, err:
        print >>sys.stderr, 'Error:', str(err)
        return 1

