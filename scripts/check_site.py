#!/usr/bin/env python3
"""Check deployable output: links, metadata, JSON-LD, sitemap and staging policy."""
import json
from hashlib import sha256
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs'
config = json.loads((ROOT/'source/config.json').read_text())
origin = config['site_url'].rstrip('/')+'/'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.meta, self.jsonld = set(), [], {}, []
        self.h1 = 0
        self.canonical = None
        self.title = ''
        self.in_title = False
        self.in_json = False
        self.buffer = ''
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        for key in ('href','src','data-src','poster'):
            if a.get(key): self.refs.append(a[key])
        if tag=='h1': self.h1 += 1
        if tag=='meta': self.meta[a.get('name',a.get('property',''))] = a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canonical = a['href']
        if tag=='title': self.in_title = True
        if tag=='script' and a.get('type')=='application/ld+json': self.in_json, self.buffer = True,''
        if tag=='img': assert 'alt' in a, 'Missing image alt'
        if tag=='iframe': assert a.get('title'), 'Missing iframe title'
    def handle_data(self,data):
        if self.in_title: self.title += data
        if self.in_json: self.buffer += data
    def handle_endtag(self,tag):
        if tag=='title': self.in_title = False
        if tag=='script' and self.in_json:
            self.jsonld.append(json.loads(self.buffer))
            self.in_json = False

homepage = (OUT/'index.html').read_bytes()
assert homepage == (ROOT/'source/homepage.html').read_bytes(), 'ARG homepage differs from its source'
assert sha256(homepage).hexdigest() == '7dc7f6afb0126e6d712137bf9fb7b4c10af2fa7ef8f920d26cbd51fac3d8cd58', 'ARG homepage differs from the original pasted HTML'

pages={}
for path in OUT.rglob('*.html'):
    if path == OUT/'index.html':
        continue
    parsed = Page()
    text = path.read_text()
    parsed.feed(text)
    assert 'secret_token' not in text and 's-WMVF' not in text, 'Unlisted media token in output'
    assert parsed.h1 == 1, f'{path}: expected one H1'
    assert parsed.title.strip(), f'{path}: missing title'
    pages[path.resolve()] = parsed

canonicals=[origin]
for path,p in pages.items():
    if path.name != '404.html':
        expected = origin + ('' if path == OUT/'index.html' else str(path.relative_to(OUT)).removesuffix('index.html'))
        assert p.canonical == expected, f'{path}: wrong canonical'
        assert len(p.meta.get('description','')) >= 80, f'{path}: missing description'
        assert p.meta.get('og:url') == expected, f'{path}: wrong sharing URL'
        assert p.meta.get('og:image','').startswith(origin), f'{path}: wrong sharing image'
        assert ('noindex' in p.meta['robots']) == (not config['indexing']), f'{path}: wrong indexing policy'
        assert p.jsonld, f'{path}: missing structured data'
        group = next(n for n in p.jsonld[0]['@graph'] if n['@type']=='MusicGroup')
        assert group['@id'] == config['band_id'], f'{path}: unstable band identity'
        assert len(group['subjectOf']) == 8, f'{path}: missing press evidence'
        canonicals.append(expected)
    for ref in p.refs:
        url = urlsplit(ref)
        if url.scheme in ('mailto','tel'): continue
        if url.scheme or url.netloc:
            if ref.startswith(origin):
                local = OUT / unquote(url.path.removeprefix(urlsplit(origin).path))
            else: continue
        else: local = path.parent / unquote(url.path)
        if local.is_dir(): local /= 'index.html'
        local = local.resolve()
        assert local.exists(), f'{path}: broken local link {ref}'
        if url.fragment and local in pages:
            assert url.fragment in pages[local].ids, f'{path}: missing anchor {ref}'

sitemap=ET.parse(OUT/'sitemap.xml')
locations=[node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert sorted(locations) == sorted(canonicals), 'Sitemap and canonical URLs disagree'
assert (OUT/'.nojekyll').exists(), 'Missing GitHub Pages marker'
assert not (OUT/'CNAME').exists() or config['indexing'], 'Custom domain set during staging'
for file in (OUT/'assets').iterdir():
    assert file.stat().st_size < 1_000_000, f'Oversized published asset: {file.name}'
print(f'PASS: exact original ARG homepage; {len(pages)} supporting HTML pages; secondary links, metadata, JSON-LD, sitemap and staging policy.')
