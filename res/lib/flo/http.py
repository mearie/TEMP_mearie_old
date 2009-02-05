"""Partial implementation of HTTP/1.1.
"""

from __future__ import absolute_import, division, with_statement

import re
import httplib


class HttpError(Exception):
    def __init__(self, status, reason=None):
        if reason is None: reason = httplib.responses[status]
        Exception.__init__(self, status, reason)

    @property
    def status(self):
        return self.args[0]

    @property
    def reason(self):
        return self.args[1]

    @property
    def header_line(self):
        status, reason = self.args
        return '%d %s' % (status, reason)

    def __repr__(self):
        status, reason = self.args
        return '%s(httplib.%s, %r)' % (self.__class__.__name__,
                httplib.responses[status].upper().replace(' ','_').replace('-','_'),
                reason)


_TOKEN_RE = re.compile(r'''
        ["(),/:;<=>?@\[\\\]{}] | # separators
        [!#$%&'*+\-.0-9A-Z^_`a-z|~]+ | # token
        "(?:[^"]|\\.)+" # quoted-string
    ''', re.S | re.X)
_QUOTEDCHAR_RE = re.compile(r'\\(.)', re.S)

def tokenize(value):
    """Tokenize value to separators, tokens and quoted strings,
    as defined in RFC 2616 section 2.2."""
    return _TOKEN_RE.findall(value)


_LANGTAG_RE = re.compile(r'''
        ^(?:
            [a-z]{2,3}(?:-[a-z0-9]{2,8})* | # usual language tag
            [ix](?:-[a-z0-9]{1,8})+         # grandfathered(i-) or private use(x-)
        )$''', re.X | re.I)

def is_langtag(tag):
    """Returns true if given tag is likely an IETF language subtag."""
    return _LANGTAG_RE.search(tag) is not None

def parse_acceptlike(value, parsefunc, moreparams=False):
    """Parse Accept and Accept-* header ("Accept-like"). It handles most practical
    cases correctly, but doesn't fully conform as it can accept some wrong header."""
    tokens = tokenize(value)

    i = 0
    entries = []
    while i < len(tokens):
        entry, i = parsefunc(tokens, i)

        params = []
        q = 1000 # rescaled by 1000 (see section 3.9)
        while i < len(tokens) and tokens[i] == ';':
            if tokens[i+2] != '=': raise ValueError, 'expected "="'
            if tokens[i+1] == 'q':
                token = tokens[i+3]
                q = int(token[:1] + token[2:].ljust(3, '0'))
                if not 0 <= q <= 1000: raise ValueError, 'invalid q value'
            elif not moreparams:
                raise ValueError, 'too many parameters'
            else:
                name = tokens[i+1]
                token = tokens[i+3]
                if token.startswith('"'):
                    token = _QUOTEDCHAR_RE.sub(r'\1', token[1:-1])
                params.append((name, token))
            i += 4

        if i < len(tokens) and tokens[i] != ',': raise ValueError, 'expected ","'
        i += 1

        if moreparams:
            entries.append((q, entry, params))
        else:
            entries.append((q, entry))

    # XXX assumes list.sort is stable (which is true for CPython 2.3+, but that's
    # implementation detail)
    if moreparams:
        entries.sort(key=lambda (q,e,p): q, reverse=True)
    else:
        entries.sort(key=lambda (q,e): q, reverse=True)
    return entries

def _parsefunc_type(tokens, i):
    if tokens[i+1] != '/': raise ValueError, 'expected "/"'
    type = tokens[i]
    if type == '*': type = None
    subtype = tokens[i+2]
    if subtype == '*': subtype = None
    return (type, subtype), i+3

def _parsefunc_lang(tokens, i):
    token = tokens[i]
    if token == '*': token = ''
    return tuple(token.lower().split('-')), i+1

def parse_accept(value):
    """Parses Accept header. Returns a list of (q, (type, subtype), params)."""
    return parse_acceptlike(value, _parsefunc_type, moreparams=True)

def parse_acceptlang(value):
    """Parse Accept-Language header. Returns a list of (q, (lang, sublang, ...))."""
    return parse_acceptlike(value, _parsefunc_lang)

def match_accept(entries, type):
    if type is not None:
        type, subtype = type.split('/')
    else:
        type = subtype = None
    for i, (q, entry, params) in enumerate(entries):
        if entry[0] is not None and entry[0] != type: continue
        if entry[1] is not None and entry[1] != subtype: continue
        return q, i
    return 0, 0

def match_acceptlang(entries, lang):
    if lang is not None:
        lang = tuple(lang.lower().split('-'))
    else:
        lang = ()
    for i, (q, entry) in enumerate(entries):
        if lang[:len(entry)] == entry: return q, i
    return 1, 0 # merely acceptable, unless *;q=0 is explicitly given

