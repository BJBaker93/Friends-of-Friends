#!/usr/bin/env python3
"""Build a dependency-free static site for GitHub Pages from checked-in sources."""
import json
from datetime import date
from html import escape as e
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
config = json.loads((ROOT / 'source/config.json').read_text())
research = json.loads((ROOT / 'source/press.json').read_text())
origin = config['site_url'].rstrip('/') + '/'
assert origin.startswith('https://'), 'site_url must be an HTTPS URL'
indexing = config['indexing']
profiles = research['official_profiles']
press = research['sources']
band_id = config['band_id']
description = 'Friends of Friends are an Australian alternative rock band from South East Queensland, bringing together indie-rock guitars, pop hooks, electronics and punk energy.'

def link(url, text):
    return f'<a href="{e(url, quote=True)}">{text}</a>'

def press_rows(items):
    rows = []
    for item in items:
        published = ''
        if item['date']:
            display = date.fromisoformat(item['date']).strftime('%d %b %Y').lstrip('0')
            published = f'<time datetime="{item["date"]}">{display}</time>'
        rows.append(f'''<a class="press-item" href="{e(item['url'], quote=True)}">
        <div class="press-meta">{e(item['publisher'])}{published}</div>
        <div><h3>{e(item['title'])}</h3><p>{e(item['summary'])}</p></div><span class="arrow" aria-hidden="true">↗</span></a>''')
    return '\n'.join(rows)

def render(filename, title, desc, body, current='home'):
    prefix = './' if filename == 'index.html' else '../'
    canonical = origin + ('' if filename == 'index.html' else filename.removesuffix('index.html'))
    nav = [('home','ARG home',prefix), ('discover','Discover',prefix+'discover/'), ('press','Press',prefix+'press/'), ('music','Listen',profiles['spotify']), ('live','Live',profiles['bandsintown'])]
    navigation = ''.join(f'<a href="{url}"'+(' aria-current="page"' if key == current and key in ('home','discover','press') else '')+f'>{label}</a>' for key,label,url in nav)
    subject_of = []
    for item in press:
        article = {'@type':'Article','headline':item['title'],'url':item['url'],'publisher':{'@type':'Organization','name':item['publisher']}}
        if item['date']: article['datePublished'] = item['date']
        subject_of.append(article)
    band = {'@type':'MusicGroup','@id':band_id,'name':'Friends of Friends','url':'https://friendsoffriendsband.com/', 'description':description,
        'genre':['Alternative rock','Indie rock','Pop rock'], 'email':'contact@friendsoffriendsband.com',
        'location':{'@type':'Place','name':'South East Queensland, Australia'},'sameAs':list(profiles.values())+['https://soundcloud.com/friendsoffriendsband'],
        'subjectOf':subject_of, 'album':[
        {'@type':'MusicAlbum','name':'Synthetic Flower Chainsaw','datePublished':'2025-10-24','url':'https://ffm.to/sfc','byArtist':{'@id':band_id}},
        {'@type':'MusicAlbum','name':'Real Life, Right Now','url':'https://open.spotify.com/album/4bSglQFwxnZCK0BrTVVBar','byArtist':{'@id':band_id}}]}
    graph = [band, {'@type':'WebSite','@id':origin+'#website','url':origin,'name':'Friends of Friends','publisher':{'@id':band_id}},
        {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'about':{'@id':band_id},'isPartOf':{'@id':origin+'#website'},'inLanguage':'en-AU'}]
    if filename != 'index.html':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':origin},{'@type':'ListItem','position':2,'name':current.title(),'item':canonical}]})
    data = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
    robots = 'index, follow, max-image-preview:large' if indexing else 'noindex, follow'
    html = f'''<!doctype html>
<html lang="en-AU"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc,quote=True)}">
<meta name="robots" content="{robots}"><meta name="theme-color" content="#10100e">
<link rel="canonical" href="{canonical}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:locale" content="en_AU"><meta property="og:site_name" content="Friends of Friends">
<meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(desc,quote=True)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{origin}assets/background-still.jpg"><meta property="og:image:width" content="1600"><meta property="og:image:height" content="900"><meta property="og:image:alt" content="Friends of Friends studio artwork with vintage recording equipment">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title,quote=True)}"><meta name="twitter:description" content="{e(desc,quote=True)}"><meta name="twitter:image" content="{origin}assets/background-still.jpg">
<link rel="stylesheet" href="{prefix}assets/site.css"><script type="application/ld+json">{data}</script>
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="wrap"><a class="brand" href="{prefix}" aria-label="Friends of Friends home">FRIENDS<br>OF FRIENDS</a><nav class="nav" aria-label="Main">{navigation}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div><span class="signal" aria-hidden="true"></span>FRIENDS OF FRIENDS / AUSTRALIA<br>© {date.today().year} Friends of Friends</div><div>{link(profiles['instagram'],'Instagram')}{link(profiles['youtube'],'YouTube')}{link(profiles['spotify'],'Spotify')}{link('https://linktr.ee/fofband','All links')}<br>{link('mailto:contact@friendsoffriendsband.com','contact@friendsoffriendsband.com')}</div></div></footer></body></html>'''
    path = OUT / filename
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(html)

# Keep the ARG homepage byte-for-byte identical to the user's supplied HTML.
# SEO content and metadata belong to the separate discovery and press pages.
(OUT / 'index.html').write_bytes((ROOT / 'source/homepage.html').read_bytes())

discover = f'''
<section class="page-intro"><div class="wrap"><p class="eyebrow">A Friends of Friends listening guide</p><h1>For fans of<br>The 1975.<br>And a little further.</h1><p class="lede">Looking for Australian bands like The 1975, or exploring the guitar-driven world around Sam Fender? Meet Friends of Friends through the influences and stories behind the music.</p><div class="actions"><a class="cta primary" href="https://ffm.to/sfc">Start listening ↗</a></div></div></section>
<section class="section"><div class="wrap reading"><h2>Australian alternative rock, with pop instincts.</h2><p>Friends of Friends bring together indie-rock guitars, electronic production, pop hooks and punk energy. The band come from South East Queensland, with roots and live connections across the Gold Coast and Brisbane. Their music moves between melody and abrasion: a natural meeting point for listeners who like their rock music open to a few different directions.</p>
<p>The connections below come from band interviews and published reviews. They're a way into the songs; the music has its own character.</p>
<h2>Looking for bands like The 1975?</h2><p>The link goes back to the beginning. In {link(press[4]['url'],'Mixdown’s Up Close &amp; Personal interview')}, Barnaby Baker recalls watching The 1975 at Splendour in the Grass with Tom and deciding to give a band a shot. That pull towards ambitious pop and a guitar-band setup is part of the story of Friends of Friends.</p><p>It also shows up in the way others hear the music. {link(press[1]['url'],'HIVE’s review of Synthetic Flower Chainsaw')} draws a comparison with The 1975, while exploring the EP's electronics and alternative-rock sound. {link(press[2]['url'],'scenestr’s All Time Low support review')} hears a related influence in the live performance. Try the EP and follow that thread for yourself.</p>
<h2>For listeners exploring artists like Sam Fender.</h2><p>The connection here is specific. In a {link(press[5]['url'],'2023 interview with Alterwave')}, Friends of Friends describe a then-upcoming single as drawing on Bruce Springsteen and Sam Fender. It opens a window into the band's interest in expansive, guitar-driven songwriting.</p><p>If emotional songs and a sense of scale are what bring you to Sam Fender, put Friends of Friends in your next listening session. Their catalogue also brings in electronics, indie pop and punk influences, so expect a few turns along the way.</p>
<h2>The Cure, Nine Inch Nails and the space between.</h2><p>The jangling guitar idea behind <em>I Like Ya</em> began with a nod to The Cure, according to {link(press[7]['url'],'the band’s songwriting story in With Drums and Colour')}. Barnaby's interest in Nine Inch Nails and production appears in {link(press[4]['url'],'the Mixdown interview')}. Together, those reference points help explain a sound that makes room for both sweetness and sharper edges.</p>
<h2>Discovering bands around Brisbane?</h2><p>There is a real local story here. Mixdown and The AU Review have covered Friends of Friends as a Brisbane indie-rock act; AMPED explores the band's Gold Coast setting. In May 2026, {link(press[3]['url'],'Everblack covered their set at The Tivoli in Brisbane')} on a bill with Enter Shikari and Grandson.</p><p>For listeners searching for good Brisbane bands or new Australian alternative rock, the most useful next step is to hear the records and see the band live. {link(profiles['bandsintown'],'Check listed shows and follow for announcements')}, or explore the {link('../press/','interviews and live reviews')}.</p>
<h2>Where to start.</h2><ul class="track-list"><li><span>Synthetic Flower Chainsaw / EP, 2025</span>{link('https://ffm.to/sfc','Listen ↗')}</li><li><span>Real Life, Right Now / EP, 2024</span>{link('https://open.spotify.com/album/4bSglQFwxnZCK0BrTVVBar','Listen ↗')}</li><li><span>More Friends of Friends</span>{link(profiles['youtube'],'Watch on YouTube ↗')}</li></ul><p>Keep going with {link(profiles['spotify'],'the band’s Spotify catalogue')} and {link(profiles['apple_music'],'Apple Music')}. For the stories behind the sound, read the original sources in {link('../press/','our press archive')}.</p></div></section>'''
render('discover/index.html','Bands Like The 1975 & Sam Fender? | Friends of Friends','Discover Australian alternative rock band Friends of Friends: The 1975 connection, Sam Fender influences, Brisbane live coverage and a guide to the music.',discover,'discover')

press_body = f'''<section class="page-intro"><div class="wrap"><p class="eyebrow">Friends of Friends / In the press</p><h1>Read all<br>about it.</h1><p class="lede">The records, the live shows and the stories behind them. Explore interviews, reviews and features from Australia and beyond.</p></div></section><section class="section"><div class="wrap">{press_rows(sorted(press,key=lambda p:p['date'] or '2025-10-22',reverse=True))}<p class="small" style="margin-top:35px">Article summaries are written for this archive. Each link takes you to the original publisher. Live reviews may cover a shared bill. Publication dates are shown where verified.</p></div></section><section class="section"><div class="wrap two-col"><div><p class="eyebrow">For writers &amp; promoters</p><h2>A quick<br>introduction.</h2></div><div><p>{description}</p><p>Releases include <em>Real Life, Right Now</em> (2024) and <em>Synthetic Flower Chainsaw</em> (2025). For interviews, press materials and bookings: {link('mailto:contact@friendsoffriendsband.com','contact@friendsoffriendsband.com')}.</p><p>Official artist profiles: {link(profiles['spotify'],'Spotify')}, {link(profiles['apple_music'],'Apple Music')} and {link(profiles['triple_j_unearthed'],'triple j Unearthed')}.</p></div></div></section>'''
render('press/index.html','Friends of Friends Press | Interviews, Reviews & Brisbane Live Coverage','Read Friends of Friends interviews, EP reviews and live coverage from AMPED, HIVE, Mixdown, scenestr, Everblack, Alterwave and The AU Review.',press_body,'press')

# A project site is temporarily served below /Friends-of-Friends/. Use an absolute
# home URL so a 404 at any unknown path still has a working route back.
not_found = f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Friends of Friends</title><link rel="stylesheet" href="{origin}assets/site.css"></head><body><main class="wrap error-page"><p class="eyebrow">404 / Wrong turn</p><h1>Lost in<br>the noise?</h1><p>This page could not be found.</p><a class="cta primary" href="{origin}">Back to Friends of Friends</a></main></body></html>'''
(OUT/'404.html').write_text(not_found)
(OUT/'.nojekyll').touch()
urls = [origin,origin+'discover/',origin+'press/']
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{e(url)}</loc></url>\n' for url in urls)+'</urlset>\n')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\n'+(f'Sitemap: {origin}sitemap.xml\n' if indexing else '# Preview pages carry noindex. Enable indexing at the custom-domain launch.\n'))
print(f'Copied exact ARG homepage; built 2 SEO pages + 404. Origin: {origin}; secondary-page indexing: {indexing}.')
