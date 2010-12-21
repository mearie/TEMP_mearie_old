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
        (out, err) = popen.communicate(input=text.encode('utf-8'))
        if popen.returncode != 0:
            raise RuntimeError('pandoc failed with code %d' % returncode)
        html = out.decode('utf-8')
        html = re.sub(ur'\n\s*>', ur'>', html)
        html = re.sub(ur'<(/?)h([1-5])\b', lambda m: '<%sh%d' % (m.group(1), int(m.group(2))+1), html)
        html = re.sub(ur'(</?(?:ul|ol|dl|div|blockquote|pre)(?!\w).*?>|</(?:h[1-6]|p|li)>)', ur'\1\n', html)
        html = re.sub(ur'&#(\d+);', lambda m: m.group(0) if int(m.group(1)) < 128 else unichr(int(m.group(1))), html)
        set_cache(key, html)
    return html

