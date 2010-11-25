import os.path
import re

from webase import *
import mako.lookup, mako.exceptions
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


application = Application(show_traceback=False)
tmpl = mako.lookup.TemplateLookup(
        directories=[os.path.join(os.path.dirname(__file__),
                                  '../../../res/dynamic')],
        input_encoding='utf-8', output_encoding='utf-8', format_exceptions=True)
db = ResponseDB(os.path.join(os.path.dirname(__file__),
                             '../../../res/db/response.db'))

def render(name, **kwargs):
    try:
        t = tmpl.get_template(name + '.tmpl.html')
        return t.render(**kwargs)
    except:
        return mako.exceptions.html_error_template().render()

@application.handle(r'^/(?:~(?P<site>[a-zA-Z0-9-.])+/)?(?P<path>.*)$')
def view(env, path, site=None):
    try:
        siteobj = PATHMAP[site]
    except KeyError:
        env.status(404)
        #yield 'site failed %r' % site
        return

    normalpath = siteobj.canonicalize(path)
    if normalpath is None:
        env.status(404)
        #yield 'path failed %r' % path
        return
    if not siteobj.exists(normalpath):
        env.status(404)
        #yield 'path not exists %r' % path
        return

    if normalpath != path:
        prefix = '/'
        if site: prefix += '~%s/' % site
        env.status(301)
        env.header('Location', prefix + normalpath)
        return

    base = siteobj.basepath(normalpath)
    responses = db.list_by_url(site, path)
    responses = db.reorder_responses(responses)
    form = render('responses', responses=responses)

    format = env.GET.getfirst('format', '') or 'html'
    callback = env.GET.getfirst('callback', '')
    if format == 'jsonp' and re.match(ur'^[a-zA-Z0-9_]+$', callback):
        env.header('Content-Type', 'application/javascript')
        form = form.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        form = form.replace('<', '\\<').replace('>', '\\>')
        yield '%s("%s");' % (callback.encode('utf-8'), form)
    else:
        env.header('Content-Type', 'text/html')
        html = siteobj.read(normalpath)
        html = html.replace('<head>', '<head>\n<base href="%s" />' % base)
        html = html.replace('<div id="sitemeta">', form + '\n<div id="sitemeta">')
        yield html


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    root = '' # served in the root path
    make_server('', 8000, application).serve_forever()

