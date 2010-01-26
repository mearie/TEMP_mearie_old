import re
import subprocess
from BeautifulSoup import BeautifulStoneSoup

from mearie.cache import get_cache, set_cache

def markdown(text, opts=()):
    key = ('markdown', text)
    html = get_cache(key)
    if html is None:
        popen = subprocess.Popen(['pandoc'] + list(opts),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        popen.stdin.write(text.encode('utf-8'))
        popen.stdin.close()
        returncode = popen.wait()
        if returncode != 0:
            raise RuntimeError('pandoc failed with code %d' % returncode)
        html = popen.stdout.read().decode('utf-8')
        html = re.sub(ur'\n\s*>', ur'>', html)
        html = re.sub(ur'(&lt;)?(?<!<pre>)<code\b', lambda m: '<code' if m.group(1) else '<tt', html)
        html = re.sub(ur'</code>(?!</pre>)(&gt;)?', lambda m: '</code>' if m.group(1) else '</tt>', html)
        html = re.sub(ur'(</?(?:ul|ol|dl|div|blockquote|pre)(?!\w).*?>|</(?:h[1-6]|p|li)>)', ur'\1\n', html)
        html = re.sub(ur'&#(\d+);', lambda m: m.group(0) if int(m.group(1)) < 128 else unichr(int(m.group(1))), html)
        set_cache(key, html)
    return html

