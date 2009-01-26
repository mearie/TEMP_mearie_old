"""Partial implementation of HTTP/1.1.
"""

from __future__ import absolute_import, division, with_statement

import re

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

def parse_acceptlike(value, parsefunc, keyfunc, moreparams=False):
    """Parse Accept and Accept-* header ("Accept-like"). It handles most practical
    cases correctly, but doesn't fully conform as it can accept some wrong header."""
    tokens = tokenize(value)

    i = 0
    types = []
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
            types.append((q, entry, params))
        else:
            types.append((q, entry))

    if moreparams:
        types.sort(key=lambda (q,e,p): (-q, keyfunc(e), -len(p), p))
    else:
        types.sort(key=lambda (q,e): (-q, keyfunc(e)))
    return types

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
    return tuple(token.split('-')), i+1

def parse_accept(value):
    """Parses Accept header. Returns a list of (q, (type, subtype), params)."""
    return parse_acceptlike(value, _parsefunc_type,
            lambda (t,st): (t is None, t, st is None, st), moreparams=True)

def parse_acceptlang(value):
    """Parse Accept-Language header. Returns a list of (q, (lang, sublang, ...))."""
    return parse_acceptlike(value, _parsefunc_lang, lambda lang: (-len(lang), lang))

