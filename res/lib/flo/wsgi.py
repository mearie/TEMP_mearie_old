"""mearieflo WSGI wrapper."""

import sys, os.path
flopath = os.path.join(os.path.dirname(__file__), '..')
if flopath not in sys.path: sys.path.insert(0, flopath)

import flo.app
basepath = os.path.join(os.path.dirname(__file__), '..', '..', '..')
application = flo.app.Application(basepath)

