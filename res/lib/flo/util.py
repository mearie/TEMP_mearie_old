"""Utilities. Mainly for compatibility with older versions of Python.
"""

from __future__ import absolute_import, division, with_statement

import sys
import collections
from itertools import count, izip, imap
from copy import deepcopy
from operator import itemgetter
from keyword import iskeyword

__all__ = ['nenumerate', 'namedtuple', 'odict']


if sys.hexversion < 0x20600f0:
    def nenumerate(sequence, start=0):
        return izip(count(start), sequence)
else:
    nenumerate = enumerate


# copied from Python 2.6 standard library.
if sys.hexversion < 0x20600f0:
    def namedtuple(typename, field_names):
        if isinstance(field_names, basestring):
            field_names = field_names.replace(',', ' ').split()
        field_names = tuple(map(str, field_names))
        for name in (typename,) + field_names:
            if not all(c.isalnum() or c=='_' for c in name):
                raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
            if iskeyword(name):
                raise ValueError('Type names and field names cannot be a keyword: %r' % name)
            if name[0].isdigit():
                raise ValueError('Type names and field names cannot start with a number: %r' % name)
        seen_names = set()
        for name in field_names:
            if name.startswith('_'):
                raise ValueError('Field names cannot start with an underscore: %r' % name)
            if name in seen_names:
                raise ValueError('Encountered duplicate field name: %r' % name)
            seen_names.add(name)

        numfields = len(field_names)
        argtxt = repr(field_names).replace("'", "")[1:-1]
        reprtxt = ', '.join('%s=%%r' % name for name in field_names)
        dicttxt = ', '.join('%r: t[%d]' % (name, pos) for pos, name in enumerate(field_names))
        template = '''class %(typename)s(tuple):
            '%(typename)s(%(argtxt)s)' \n
            __slots__ = () \n
            _fields = %(field_names)r \n
            def __new__(cls, %(argtxt)s):
                return tuple.__new__(cls, (%(argtxt)s)) \n
            @classmethod
            def _make(cls, iterable, new=tuple.__new__, len=len):
                'Make a new %(typename)s object from a sequence or iterable'
                result = new(cls, iterable)
                if len(result) != %(numfields)d:
                    raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))
                return result \n
            def __repr__(self):
                return '%(typename)s(%(reprtxt)s)' %% self \n
            def _asdict(t):
                'Return a new dict which maps field names to their values'
                return {%(dicttxt)s} \n
            def _replace(self, **kwds):
                'Return a new %(typename)s object replacing specified fields with new values'
                result = self._make(map(kwds.pop, %(field_names)r, self))
                if kwds:
                    raise ValueError('Got unexpected field names: %%r' %% kwds.keys())
                return result \n
            def __getnewargs__(self):
                return tuple(self) \n\n''' % locals()
        for i, name in enumerate(field_names):
            template += '        %s = property(itemgetter(%d))\n' % (name, i)

        namespace = dict(itemgetter=itemgetter, __name__='namedtuple_%s' % typename)
        try:
            exec template in namespace
        except SyntaxError, e:
            raise SyntaxError(e.message + ':\n' + template)
        result = namespace[typename]

        if hasattr(_sys, '_getframe'):
            result.__module__ = _sys._getframe(1).f_globals['__name__']

        return result
else:
    namedtuple = collections.namedtuple


missing = object()

# copied from http://dev.pocoo.org/hg/sandbox/raw-file/1cdd9c8c3716/odict.py
class odict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self._keys = []
        self.update(*args, **kwargs)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        if key not in self:
            self._keys.append(key)
        dict.__setitem__(self, key, item)

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        d = memo.get(id(self), missing)
        if d is not missing:
            return d
        memo[id(self)] = d = self.__class__()
        dict.__init__(d, deepcopy(self.items(), memo))
        d._keys = self._keys[:]
        return d

    def __getstate__(self):
        return {'items': dict(self), 'keys': self._keys}

    def __setstate__(self, d):
        self._keys = d['keys']
        dict.update(d['items'])

    def __reversed__(self):
        return reversed(self._keys)

    def __eq__(self, other):
        if isinstance(other, odict):
            if not dict.__eq__(self, other):
                return False
            return self.items() == other.items()
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        if isinstance(other, odict):
            return cmp(self.items(), other.items())
        elif isinstance(other, dict):
            return dict.__cmp__(self, other)
        return NotImplemented

    @classmethod
    def fromkeys(cls, iterable, default=None):
        return cls((key, default) for key in iterable)

    def clear(self):
        del self._keys[:]
        dict.clear(self)

    def copy(self):
        return self.__class__(self)

    def items(self):
        return zip(self._keys, self.values())

    def iteritems(self):
        return izip(self._keys, self.itervalues())

    def keys(self):
        return self._keys[:]

    def iterkeys(self):
        return iter(self._keys)

    def pop(self, key, default=missing):
        if default is missing:
            return dict.pop(self, key)
        elif key not in self:
            return default
        self._keys.remove(key)
        return dict.pop(self, key, default)

    def popitem(self, key):
        self._keys.remove(key)
        return dict.popitem(key)

    def setdefault(self, key, default=None):
        if key not in self:
            self._keys.append(key)
        dict.setdefault(self, key, default)

    def update(self, *args, **kwargs):
        sources = []
        if len(args) == 1:
            if hasattr(args[0], 'iteritems'):
                sources.append(args[0].iteritems())
            else:
                sources.append(iter(args[0]))
        elif args:
            raise TypeError('expected at most one positional argument')
        if kwargs:
            sources.append(kwargs.iteritems())
        for iterable in sources:
            for key, val in iterable:
                self[key] = val

    def values(self):
        return map(self.get, self._keys)

    def itervalues(self):
        return imap(self.get, self._keys)

    def index(self, item):
        return self._keys.index(item)

    def byindex(self, item):
        key = self._keys[item]
        return (key, dict.__getitem__(self, key))

    def reverse(self):
        self._keys.reverse()

    def sort(self, *args, **kwargs):
        self._keys.sort(*args, **kwargs)

    def __repr__(self):
        return 'odict.odict(%r)' % self.items()

    __copy__ = copy
    __iter__ = iterkeys

