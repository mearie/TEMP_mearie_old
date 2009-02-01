"""Generic processor interface.
"""

from __future__ import absolute_import, division, with_statement

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import html_error_template

class Processor(object):
    def __init__(self):
        self.priorities = {}

    def add(self, priority, proc):
        self.priorities.setdefault(priority, []).append(proc)

    def process(self, context, data=None):
        for priority, procs in sorted(self.priorities.items()):
            for proc in procs:
                if context.content_type not in proc.input_type: continue
                data = proc(context, data)
                context.content_type = proc.output_type
        return data

