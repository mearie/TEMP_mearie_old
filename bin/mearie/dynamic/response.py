import web
import os.path
import re

from mearie.response import ResponseDB


PATHMAP = {} 
def register_site(id):
    def func(cls): PATHMAP[id] = cls()
    return func

class site(object):
    def basepath(self, path):
        dir, _, _ = path.rpartition('/')
        return self.urlprefix + dir + '/'

    def canonicalize(self, path):
        try:
            path = path.encode('ascii')
        except:
            return None

        path = '/' + path.replace('\\', '/')
        components = []
        for i in path.strip('/').split('/'):
            if i == '..':
                if not components: return None
                del components[-1]
            elif i == '.' or i == '':
                continue
            else:
                components.append(i)

        if path.endswith('/'):
            components.append('index')
        return '/'.join(components)

@register_site(None)
class site_mearie(site):
    urlprefix = 'http://mearie.org/'
    prefix = os.path.join(os.path.dirname(__file__), '../../..')

    def realpath(self, path):
        return os.path.join(self.prefix, path + '.html')

    def exists(self, path):
        return os.path.exists(self.realpath(path))

    def read(self, path):
        return open(self.realpath(path), 'rb').read()

    def canonicalize(self, path):
        path = site.canonicalize(self, path)
        if path is None: return None

        assert path != ''
        if path.endswith('.html'):
            path = path[:-5]
        return path # TODO: language tag?


app = web.auto_application()
render = web.template.render(os.path.join(os.path.dirname(__file__),
                                          '../../../res/dynamic'))
db = ResponseDB(os.path.join(os.path.dirname(__file__),
                             '../../../res/db/response.db'))

class view(app.page):
    path = '/(?:~([a-zA-Z0-9-.])+/)?(.*)'

    def GET(self, site, path):
        try:
            siteobj = PATHMAP[site]
        except KeyError:
            return 'site failed %r' % site
            raise web.notfound()

        normalpath = siteobj.canonicalize(path)
        if normalpath is None:
            return 'path failed %r' % path
            raise web.notfound()
        if not siteobj.exists(normalpath):
            return 'path not exists %r' % path
            raise web.notfound()

        if normalpath != path:
            prefix = '/'
            if site: prefix += '~%s/' % site
            raise web.redirect(prefix + normalpath)

        base = siteobj.basepath(normalpath)
        responses = db.list_by_url(site, path)
        form = str(render.responses(responses=responses))

        input = web.input(format='html', callback='')
        if input.format == 'jsonp' and re.match(ur'^[a-zA-Z0-9_]+$', input.callback):
            web.header('Content-Type', 'application/javascript')
            form = form.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return '%s("%s");' % (input.callback.encode('utf-8'), form)
        else:
            web.header('Content-Type', 'text/html')
            html = siteobj.read(normalpath)
            html = html.replace('<head>', '<head>\n<base href="%s" />' % base)
            html = html.replace('<div id="sitemeta">', form + '\n<div id="sitemeta">')
            return html

if __name__ == '__main__': app.run()

