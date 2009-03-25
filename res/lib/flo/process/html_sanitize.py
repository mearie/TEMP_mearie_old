"""(X)HTML sanitizer, converts CDATA section and non-XML-compatible entities.
"""

from __future__ import absolute_import, division, with_statement

from .common import BaseHTMLProcessor

import re
import os
import htmlentitydefs

_ENTITY_LIST = dict((name, unichr(code).encode('utf-8'))
                    for name, code in htmlentitydefs.name2codepoint.items()
                    if code >= 128)
_CDATA_RE = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.S)
_ENTITY_RE = re.compile(r'&(%s);' % '|'.join(_ENTITY_LIST.keys()))

class HTMLSanitizer(BaseHTMLProcessor):
    def __call__(self, context, data):
        if data is None:
            data = context.as_file().read()

        data = _CDATA_RE.sub(
                lambda m: m.group(1).replace('&','&amp;').replace('<','&lt;') \
                        .replace('>','&gt;'),
                data)
        data = _ENTITY_RE.sub( lambda m: _ENTITY_LIST[m.group(1)], data)

        return data

