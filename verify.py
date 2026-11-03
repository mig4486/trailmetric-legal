from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).parent

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.language = None
        self.forbidden = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.language = a.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if 'id' in a:
            assert a['id'] not in self.ids
            self.ids.add(a['id'])
        if tag in ('script','iframe','form'):
            self.forbidden.append(tag)
        for key in ('href','src'):
            if a.get(key):
                self.links.append(a[key])

files = list(ROOT.glob('*.html')) + list((ROOT/'ru').glob('*.html'))
assert len(files) == 8
for path in files:
    text = path.read_text(encoding='utf-8')
    doc = Document()
    doc.feed(text)
    assert doc.h1 == 1 and doc.language in ('en','ru'), path
    assert not doc.forbidden, path
    assert 'tgstartup@icloud.com' in text and '[email]' not in text, path
    assert 'viewport' in text and 'style.css' in text, path
    for href in doc.links:
        u = urlsplit(href)
        if u.scheme or u.netloc:
            assert u.scheme in ('https','mailto'), href
            continue
        target = path.parent / unquote(u.path) if u.path else path
        assert target.exists(), (path, href)
        if u.fragment and target == path:
            assert u.fragment in doc.ids, (path,href)
data=json.loads((ROOT/'content.json').read_text(encoding='utf-8-sig'))
assert len(data)==3 and (ROOT/'.nojekyll').exists()
assert not (ROOT/'.github/workflows').exists()
print('Verified 8 EN/RU pages: local links, anchors, titles, language, contact, assets; no scripts, frames or forms.')

