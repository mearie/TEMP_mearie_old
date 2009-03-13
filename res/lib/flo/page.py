"""Page abstraction.
"""

from __future__ import absolute_import, division, with_statement

from .db import *

class Page(ModelBase):
    __tablename__ = 'flopages'

    # the directory path containing the page, like "/projects/flo/" in the page
    # "/projects/flo/index.ko.html".
    parent = Column(String, primary_key=True)
    # the actual (non-processed) file name, like "index.ko.html" in the page
    # "/projects/flo/index.ko.html".
    basename = Column(String, primary_key=True)
    # resolved URI name, like "index" from "index.ko.html".
    name = Column(String)
    # content language, like "ko" from "index.ko.html". it can be NULL.
    lang = Column(String)
    # content type, like "text/html" from "index.ko.html".
    type = Column(String)

    #def __init__(self, parent=None, basename=None, 

