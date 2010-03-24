import re
import datetime
import time

def parse_iso8601(d):
    m = re.match(r'^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d):?(\d\d)(?::?(\d\d))?)(Z|[+-]\d\d:\d\d)?$', d)
    if not m: raise ValueError('invalid ISO 8601 datetime')
    if m.group(6):
        return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                 int(m.group(4)), int(m.group(5)), int(m.group(6)))
    elif m.group(4):
        return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                 int(m.group(4)), int(m.group(5)))
    else:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

def to_iso8601(d):
    tz = time.timezone
    return '%s%c%02d:%02d' % (d.strftime('%Y-%m-%dT%H:%M:%S'), '-' if tz<0 else '+',
                              abs(tz)//3600, abs(tz)//60%60)

