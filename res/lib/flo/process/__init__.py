"""Generic processor interface.
"""

from __future__ import absolute_import, division, with_statement

class Processor(object):
    def __init__(self):
        self.priorities = {}

    def add(self, priority, proc):
        self.priorities.setdefault(priority, []).append(proc)

    def process(self, context, data=None):
        for priority, procs in sorted(self.priorities.items()):
            for proc in procs:
                resulttype = proc.accepts(context, context.content_type)
                if resulttype is None: continue
                data = proc(context, data)
                context.content_type = resulttype
        return data

    def __copy__(self):
        obj = Processor(self.app)
        for prio, procs in self.priorities.items():
            obj.priorities[prio] = procs[:]
        return obj

