import sqlite3
import time
import web
import re

class ResponseDB(object):
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row

    def setup(self):
        self.db.executescript('''
            begin;
            pragma legacy_file_format = 0;
            create table response(
                id integer primary key not null,
                site text not null,
                url text not null,
                parent integer references response(id),
                author text not null,
                origin text not null, -- one of 'comment', 'trackback', 'admin'
                contents text not null,
                format text not null, -- one of 'plain'
                datetime integer not null
            );
            create index response_idx on response(datetime desc);
            create index response_url_idx on response(site, url, datetime asc);
            create index response_parent_idx on response(parent, datetime asc);
            commit;
        ''')

    def list_all(self, range=(0,-1)):
        cursor = self.db.execute('''select * from response order by datetime desc
                                    limit ? offset ?;''', (range[1], range[0]))
        return map(Response, cursor.fetchall())

    def list_by_url(self, site, url, range=(0,-1)):
        cursor = self.db.execute('''select * from response where site=? and url=? order by datetime asc
                                    limit ? offset ?;''', (site or '', url, range[1], range[0]))
        return map(Response, cursor.fetchall())

class Response(object):
    def __init__(self, row):
        self.id = row['id']
        self.site = row['site']
        self.url = row['url']
        self.parent = row['parent']
        self.author_raw = row['author']
        self.author_name, self.author_emails, self.author_urls, self.author_more = \
                self.parse_author(self.author_raw)
        self.origin = row['origin']
        self.contents_raw = row['contents']
        self.format = row['format']
        self.datetime = row['datetime']

    def parse_author(self, authorstr):
        lines = filter(None, authorstr.splitlines())
        firstline = lines[0]
        emails = []
        websites = []
        while True:
            m = re.search(ur'\s+(?:\((.*?)\)|<(.*?)>|\[(.*?)\])\s*$', firstline)
            if not m: break
            data = (m.group(1) or m.group(2) or m.group(3)).strip()
            if data.startswith('mailto:'):
                emails.append(data[7:].lstrip())
            elif data.startswith('http://') or data.startswith('https://'):
                websites.append(data)
            elif re.match(ur'^\S+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$', data):
                emails.append(data)
            elif re.match(ur'^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}(?:/\S*)$', data):
                websites.append('http://' + data)
            else:
                break
            firstline = firstline[:m.start(0)]
        return (firstline, emails, websites, lines[1:])

    @property
    def datetime_text(self):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(self.datetime))

    @property
    def contents(self):
        if self.format == 'plain':
            return web.websafe(self.contents_raw).replace('\n', '<br />\n')
        raise RuntimeError('unknown format')

