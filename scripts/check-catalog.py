# -*- coding: utf-8 -*-
"""Check generated SEO pages, internal destinations and financial disclosure coverage."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree
from datetime import date
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
ORIGIN = 'https://www.bmwgjbaek.com'
models = json.loads((ROOT / 'data/models.json').read_text())
finance = json.loads((ROOT / 'data/finance.json').read_text())
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


pages = {p: BeautifulSoup(p.read_text(), 'html.parser') for p in DIST.rglob('*.html')}
titles = set()
urls = set()
for path, soup in pages.items():
    rel = path.relative_to(DIST)
    route = '/' + str(rel)
    if route.endswith('index.html'):
        route = route[:-10]
    check(len(soup.select('h1')) == 1, f'{rel}: expected exactly one H1')
    canonical = soup.select_one('link[rel=canonical]')
    check(canonical and canonical.get('href') == ORIGIN + route, f'{rel}: wrong canonical')
    title = soup.title.get_text() if soup.title else ''
    check(title and title not in titles, f'{rel}: missing/duplicate title')
    titles.add(title)
    if route != '/privacy.html':
        urls.add(ORIGIN + route)
    check('bmw-baek-landing.vercel.app' not in path.read_text(), f'{rel}: old domain')
    for block in soup.select('script[type="application/ld+json"],script[type="application/json"]'):
        try:
            json.loads(block.string or block.get_text())
        except json.JSONDecodeError as exc:
            errors.append(f'{rel}: invalid JSON: {exc}')
    for element in soup.select('a[href],img[src],script[src],link[href]'):
        raw = element.get('href') or element.get('src')
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (DIST / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
        if target.is_dir():
            target /= 'index.html'
        check(target.is_file(), f'{rel}: broken internal URL {raw}')
    for img in soup.select('img'):
        check(img.has_attr('alt'), f'{rel}: missing alt text')

sitemap = ElementTree.parse(DIST / 'sitemap.xml')
listed = {loc.text for loc in sitemap.findall('.//{*}loc')}
check(listed == urls, 'Sitemap must include exactly all indexable HTML pages')
check(f'Sitemap: {ORIGIN}/sitemap.xml' in (DIST / 'robots.txt').read_text(), 'Wrong sitemap host')
slugs = {m['slug'] for m in models}
check(len(slugs) == len(models), 'Duplicate model slugs')
for model in models:
    check((DIST / 'models' / model['slug'] / 'index.html').is_file(), f'Missing {model["slug"]} page')
    for variant in model['variants']:
        for key in ['image', 'sideImage']:
            check((DIST / variant[key].lstrip('/')).is_file(), f'Missing {variant[key]}')
        check(variant['source'].startswith('https://www.bmw.co.kr/'), 'Non-BMW model source')

check(date.fromisoformat(finance['validFrom']) <= date.fromisoformat(finance['checkedAt']) <= date.fromisoformat(finance['validThrough']), 'Finance verification date is outside its validity period')
finance_page = pages[DIST / 'finance/index.html']
cards = finance_page.select('.benefit-card')
check(len(cards) == len(finance['benefits']), 'Missing benefits')
check(not finance_page.select('input,select,.finance-panel'), 'The benefits page must not contain quote/calculator controls')
for benefit in finance['benefits']:
    check(benefit['modelSlug'] in slugs, f'Unknown benefit model {benefit["modelSlug"]}')
    card = finance_page.select_one('#benefit-' + benefit['modelSlug'])
    text = card.get_text(' ', strip=True) if card else ''
    check(benefit['source'] in str(card), 'Missing official benefit source')
    for item in benefit['items']:
        for token in [item['label'], f"{item['monthlyMax']}만 원", f"{item['months']}개월", f"{item['totalMax']:,}만 원"]:
            check(token in text, f'Missing benefit condition {token}')
        check(item['monthlyMax'] * item['months'] == item['totalMax'], 'Benefit support arithmetic mismatch')
    if benefit['modelSlug'] == 'i5':
        check('이미 반영' in text, 'i5 support must not be subtracted twice')
shared_header = str(pages[DIST / 'index.html'].select_one('header'))
for path, soup in pages.items():
    check(str(soup.select_one('header')) == shared_header, f'{path.relative_to(DIST)}: inconsistent navigation')
    check(soup.select_one('.personal-site-notice'), f'{path.relative_to(DIST)}: missing personal site disclosure')
for route in ['index.html', 'models/index.html']:
    soup = pages[DIST / route]
    check([urlsplit(a['href']).path for a in soup.select('.lineup-entry')] == ['/models/sedan/', '/models/suv/', '/models/hatchback/'], f'{route}: expected three lineup entry points')
for model in models:
    soup = pages[DIST / 'models' / model['slug'] / 'index.html']
    check(model['advisorComment'] in soup.get_text(), f'{model["slug"]}: missing advisor comment')
check('MPV' in pages[DIST / 'models/hatchback/index.html'].get_text(), 'Active Tourer must be distinguished from hatchbacks')

font_bytes = sum(p.stat().st_size for p in (DIST / 'assets/fonts').glob('*.woff2'))
check(font_bytes < 300_000, 'Total subset font budget exceeded')
print(f'{len(pages)} HTML pages, {len(listed)} sitemap URLs, {len(models)} model pages, {sum(len(m["variants"]) for m in models)} photographed variants, {len(cards)} benefit cards; fonts {font_bytes:,} bytes.')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: canonical, JSON, H1/title, internal links/assets, sitemap, shared navigation, three lineup entry points, advisor comments and benefit disclosures.')
