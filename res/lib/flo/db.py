"""Database utilities, mainly based on SQLAlchemy.
"""

from __future__ import absolute_import, division, with_statement

__all__ = ['Column', 'Integer', 'String', 'Unicode', 'ModelBase']

from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()

