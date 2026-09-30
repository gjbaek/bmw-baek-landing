# -*- coding: utf-8 -*-
"""Generate static model/finance pages. No runtime API or Vercel build required."""
from pathlib import Path
from html import escape as e
from urllib.parse import quote
from site_sections import header, lineup_hub, category_pages, finance_body, home_sections, comment_block
from advisor_content import GUIDE_PATH, buying_guide, model_faq, color_section, edition_cards, consultation, FAQ
from new_model_preview import PREVIEW_PATH, ASSETS, PRESS_SOURCE, home_hero, preview_body, model_preview_link
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
ORIGIN = 'https://www.bmwgjbaek.com'
MODELS = json.loads((ROOT / 'data/models.json').read_text())
FINANCE = json.loads((ROOT / 'data/finance.json').read_text())
BY_SLUG = {m['slug']: m for m in MODELS}
KAKAO = 'https://open.kakao.com/o/stXSvxki'
YEAR, MONTH = FINANCE['validFrom'][:7].split('-')
PERIOD = f'{YEAR}년 {int(MONTH)}월'
DATE_RANGE = FINANCE['validFrom'].replace('-', '.') + '–' + FINANCE['validThrough'].replace('-', '.')
CHECK_DATE = FINANCE['checkedAt'].replace('-', '.')

CATEGORIES = ['전체', '컴팩트', '세단', 'SUV', '전기차', '투어링', '쿠페', 'M']


def safe_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def external(url, text, css='source-link'):
    return f'<a class="{css}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(text)} <span aria-hidden="true">↗</span><span class="sr-only"> (새 창)</span></a>'


def footer():
    return f'''<footer class="catalog-footer wrap"><a class="footer-wordmark" href="/">BMW · 백경재 대리</a><p>도이치모터스 한남 전시장 · 서울특별시 용산구 이태원로 249<br><a href="tel:01083089819">010-8308-9819</a></p><p>백경재 대리의 개인 상담 사이트이며 BMW Korea·도이치모터스 기업 공식 홈페이지와 별도로 운영됩니다.<br>차량 이미지 © BMW AG. 이미지는 국내 판매 사양과 다를 수 있습니다.</p><div><a href="/privacy.html">개인정보·이용 안내</a> {external('https://www.bmw.co.kr/ko/all-models.html', 'BMW 공식 모델 정보')}</div></footer>'''


def contact(model='BMW'):
    sms = 'sms:01083089819?body=' + quote(f'안녕하세요. {model} 모델과 구매 조건을 상담받고 싶습니다.')
    return f'''<div class="detail-contact"><div><strong>{e(model)} 상담</strong><span>관심 트림과 구매 예정 시기를 알려주세요.</span></div><div>{external(KAKAO, '카카오톡 상담', 'button kakao-button')}<a class="button outline-button" data-model-sms="{e(model)}" href="{sms}">문자로 문의</a></div></div>'''


def document(title, description, path, body, schema=None, image='/assets/baek-gyeongjae.webp'):
    schema = schema or {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'url': ORIGIN + path, 'inLanguage': 'ko-KR'}
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{ORIGIN}{path}"><link rel="icon" href="/assets/bmw-logo.webp"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/catalog.css"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="{ORIGIN}{image}"><meta name="twitter:card" content="summary_large_image"><script src="/catalog.js" defer></script><script type="application/ld+json">{safe_json(schema)}</script></head><body class="catalog-page">{header()}<main id="main">{body}</main>{footer()}</body></html>'''


def write_page(path, html):
    target = DIST / path.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)


def card(m):
    v = m['variants'][0]
    names = ' '.join(v['name'] for v in m['variants'] + m.get('additionalVariants', []))
    return f'''<article class="car-card" data-category="{m['category']}" data-search="{e(m['name'] + ' ' + names)}"><a href="/models/{m['slug']}/"><div class="car-card-heading"><span class="car-category">{m['category']}</span><span class="car-count">대표 구성 {len(m['variants'])}종</span></div><h3>{e(m['name'].replace('BMW ', ''))}</h3><div class="car-card-photo"><img src="{v['image']}" width="1128" height="921" alt="{e(v['name'])} 외관" loading="lazy" decoding="async"></div><p>{e(m['tagline'])}</p><span class="car-card-link">모델 살펴보기 <span aria-hidden="true">↗</span></span></a></article>'''


def catalog():
    filters = ''.join(f'<button type="button" data-filter="{c}" aria-pressed="{str(i == 0).lower()}">{c}</button>' for i, c in enumerate(CATEGORIES))
    body = f'''<section class="catalog-intro wrap"><p class="kicker">백경재 대리의 모델 안내</p><h1>BMW 전체 모델</h1><p class="lead">1시리즈부터 액티브 투어러, 투어링, BMW M까지.<br>사진으로 살펴보고, 나의 일상에 맞는 모델을 찾아보세요.</p></section><section class="wrap catalog-list" aria-labelledby="catalog-heading"><div class="catalog-toolbar"><h2 id="catalog-heading">BMW 모델 살펴보기</h2><label class="model-search"><span class="sr-only">모델 검색</span><input type="search" id="model-search" placeholder="모델명 검색 · 예: 액티브 투어러" autocomplete="off"></label></div><div class="catalog-filters" aria-label="차체별 필터">{filters}</div><p class="result-count" id="result-count" role="status">{len(MODELS)}개 모델 · 파생 구성은 상세 페이지에서 확인</p><div class="catalog-grid">{''.join(card(m) for m in MODELS)}</div><div class="catalog-empty" hidden><p>검색한 모델을 찾지 못했어요.</p><button type="button" id="reset-catalog">전체 모델 보기</button></div><p class="source-note">2026.09.22 BMW Korea 공개 라인업 기준. 사진은 대표 구성으로, 국내 판매·시승 가능 여부와 정확한 사양은 상담 시 확인합니다. {external('https://www.bmw.co.kr/ko/all-models.html','공식 라인업 확인')}</p></section><section class="wrap catalog-finance-link"><div><p class="kicker">YOUR NEXT STEP</p><h2>모델을 골랐다면,<br>구매 조건도 나란히.</h2><p>월 납입금과 선납금, 계약기간을 함께 살펴보세요.</p></div><a href="/finance/" class="button primary">금융 혜택 살펴보기 ↗</a></section>'''
    schema = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'BMW 모델별 안내', 'url': ORIGIN + '/models/all/', 'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': ORIGIN + '/models/' + m['slug'] + '/', 'name': m['name']} for i, m in enumerate(MODELS)]}}
    write_page('/models/all/', document('BMW 전체 모델·파생모델 안내 | 한남 전시장 백경재', 'BMW 1시리즈, 2시리즈 액티브 투어러, 세단·SUV·전기차·투어링·M 모델의 사진과 선택 포인트를 비교하세요.', '/models/all/', body, schema))


CHECKS = {
    '컴팩트': [('주차와 승하차', '평소 주차 공간과 문을 여는 여유를 확인하세요.'), ('뒷좌석과 짐', '동승자와 자주 싣는 짐을 기준으로 공간을 살펴보세요.'), ('차체부터 비교', '해치백·그란 쿠페·액티브 투어러의 사용 방식을 비교하세요.')],
    '세단': [('평소 이동 거리', '시내와 장거리의 비중에 맞춰 구동 방식을 비교하세요.'), ('동승자의 자리', '뒷좌석 승차감과 필요한 편의 사양을 함께 확인하세요.'), ('옵션 우선순위', '자주 쓰는 주차·운전 보조 기능부터 정리하세요.')],
    'SUV': [('탑승 인원', '카시트나 동승자가 실제로 사용할 자리를 확인하세요.'), ('짐을 싣는 방식', '자주 사용하는 가방과 장비를 기준으로 비교하세요.'), ('주차 동선', '차체 크기와 운전석 시야를 생활 공간에 맞춰 확인하세요.')],
    '전기차': [('충전할 장소', '집과 직장에서 이용할 충전 환경을 먼저 확인하세요.'), ('일상 이동 경로', '평일 출퇴근과 주말 장거리 경로를 나눠 생각해 보세요.'), ('같은 조건의 견적', '보조금·선납금·지원금 반영 여부를 함께 비교하세요.')],
    '투어링': [('실제 사용하는 짐', '유모차·여행 가방을 기준으로 적재 편의를 확인하세요.'), ('좌석 활용', '뒷좌석을 사용할 때와 접었을 때를 각각 살펴보세요.'), ('세단과 비교', '운전 감각과 짐을 싣는 방식의 차이를 확인하세요.')],
    '쿠페': [('도어와 좌석', '뒷좌석을 얼마나 자주 사용하는지 먼저 정리하세요.'), ('주차 환경', '문을 여는 공간과 차체 크기를 함께 확인하세요.'), ('일상에서의 사용', '주행 성격뿐 아니라 승하차와 적재 편의도 살펴보세요.')],
    'M': [('원하는 주행 성격', '일상과 드라이브의 비중을 기준으로 시승해 보세요.'), ('비교할 M 구성', '일반 모델·M 퍼포먼스·M 모델의 차이를 확인하세요.'), ('동승과 유지', '승차감, 사용 환경, 유지 계획을 함께 정리하세요.')]
}


def compact_comparison(slug):
    if slug not in {'1-series', '2-active-tourer', '2-gran-coupe'}:
        return ''
    choices = [
        ('1-series', '1시리즈', '5도어 해치백', '도심 운전과 뒷문 활용성을 함께 고려할 때', '주차 공간 · 뒷좌석 승하차'),
        ('2-active-tourer', '액티브 투어러', '실내·적재 활용 중심', '동승자와 짐을 함께 싣는 일이 잦을 때', '카시트 설치 · 유모차 적재'),
        ('2-gran-coupe', '2시리즈 그란 쿠페', '4도어 쿠페 스타일', '뒷문을 유지하면서 쿠페 형태를 원할 때', '뒷좌석 머리 공간 · 승하차')
    ]
    rows = ''.join(f'<tr><th scope="row"><a href="/models/{key}/">{name} ↗</a></th><td>{body}</td><td>{usage}</td><td>{test}</td></tr>' for key, name, body, usage, test in choices)
    return '<section class="compact-comparison"><h2>비슷한 크기, 다른 쓰임새.</h2><p>어느 차가 더 좋은지보다, 자주 마주하는 장면을 기준으로 골라보세요.</p><div class="comparison-scroll" role="region" aria-label="컴팩트 모델 비교표" tabindex="0"><table><thead><tr><th scope="col">모델</th><th scope="col">차체의 성격</th><th scope="col">고려할 상황</th><th scope="col">시승에서 확인</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>'


def model_page(m):
    slug, name = m['slug'], m['name']
    heading = e(name)
    for ending in ['액티브 투어러', '그란 쿠페', '컨버터블', '투어링', '세단', '로드스터', '쿠페']:
        if name.endswith(' ' + ending):
            heading = '<span class="model-title-part">' + e(name[:-len(ending)].strip()) + '</span> <span class="model-title-part">' + e(ending) + '</span>'
            break
    v = m['variants'][0]
    options = ''.join(f'<option value="{i}">{e(x["name"])}</option>' for i, x in enumerate(m['variants']))
    variant_rows = ''.join(f'<li><div><strong>{e(x["name"])}</strong><span>{x["fuel"]}</span></div>{external(x["source"], "공식 정보")}</li>' for x in m['variants'])
    for item in m.get('additionalVariants', []):
        variant_rows += f'<li><div><strong>{e(item["name"])}</strong><span>{e(item["fuel"])} · {e(item["note"])}</span><p class="source-note">{e(item["sourcePeriod"])} · 확인 {e(item["checkedAt"])}</p></div>{external(item["source"], "공식 정보")}</li>'
    if slug == '5-series':
        offer_520 = next(o for o in FINANCE['benefits'] if o['modelSlug'] == '5-series')
        variant_rows += '<li><div><strong>BMW 520i</strong><span>가솔린 · 공식 금융 예시에서 확인된 트림</span></div>' + external(offer_520['source'], '공식 정보') + '</li>'
    checks = ''.join(f'<article><span>0{i + 1}</span><h3>{title}</h3><p>{text}</p></article>' for i, (title, text) in enumerate(CHECKS[m['category']]))
    related = [x for x in MODELS if x['category'] == m['category'] and x['slug'] != slug][:3]
    # Editorial comparisons for the otherwise single-member Touring category.
    if slug == '3-touring':
        related = [BY_SLUG[x] for x in ['3-series', '2-active-tourer', 'x3']]
    if slug == '2-active-tourer':
        related = [BY_SLUG[x] for x in ['1-series', '2-gran-coupe', 'x1']]
    specs = ''
    if slug == '1-series':
        specs = '<div class="verified-specs"><div><strong>5<span>도어</span></strong><p>뒷문이 있는 해치백</p></div><div><strong>204<span>마력</span></strong><p>120 최고 출력</p></div><div><strong>12.0<span>km/L</span></strong><p>120 복합연비 · 3등급</p></div></div><p class="source-note">BMW 120 공식 제원 기준. 복합 CO₂ 배출량 140g/km. 연비와 성능은 운전·적재·도로 조건 등에 따라 달라집니다.</p>'
    if slug == '2-active-tourer':
        specs = '<div class="verified-specs"><div><strong>470–1,455<span>L</span></strong><p>트렁크 용량 · 공식 안내</p></div><div><strong>204<span>마력</span></strong><p>220i 최고 출력</p></div><div><strong>11.9<span>km/L</span></strong><p>220i 복합연비 · 3등급</p></div></div><p class="source-note">220i 공식 제원 기준. 복합 CO₂ 배출량 140g/km. 연비와 성능은 운전·적재·도로 조건 등에 따라 달라집니다.</p>'
    benefit = next((o for o in FINANCE['benefits'] if o['modelSlug'] == slug), None)
    finance = '<p class="kicker">구매 혜택</p><h2>납입 지원도 챙겨보세요.</h2><p>구매 방식에 따라 받을 수 있는 지원이 달라집니다.</p><a class="button outline-button" href="/finance/#benefit-'+slug+'">이 모델의 구매 혜택 보기 →</a>' if benefit else '<p class="kicker">구매 상담</p><h2>구매 방식도 함께 고민해 드릴게요.</h2><p>관심 트림과 구매 예정 시기를 알려주시면 적용 가능한 조건부터 확인하겠습니다.</p>'
    body = f'''<div class="wrap breadcrumb"><a href="/">홈</a><span>/</span><a href="/models/">모델 살펴보기</a><span>/</span>{e(name)}</div><section class="model-detail wrap" data-model-detail><div class="model-detail-top"><div><p class="kicker">백경재 대리의 모델 안내 · {m['category']}</p><h1>{heading}</h1><p class="detail-tagline">{e(m['tagline'])}</p></div><a href="/models/" class="text-link">다른 모델 보기 ↗</a></div><div class="model-stage"><span class="stage-word" aria-hidden="true">{e(name.replace('BMW ', '').split(' ')[0])}</span><img id="detail-image" src="{v['image']}" width="1128" height="921" alt="{e(v['name'])} 전면 사선" fetchpriority="high"><div class="angle-switch" aria-label="사진 방향"><button type="button" data-angle="front" aria-pressed="true">전면 사선</button><button type="button" data-angle="side" aria-pressed="false">측면</button></div></div><div class="model-selector-row"><label>사진으로 살펴볼 구성<select id="variant-select">{options}</select></label><p><span id="variant-fuel">{v['fuel']}</span><br><span class="muted">{m['availability']}</span></p></div><p class="source-note">사진은 구성별 대표 이미지입니다. 색상·옵션은 실제 판매 차량과 다를 수 있습니다.</p>{comment_block(m)}{specs}<div class="model-story"><p class="kicker">이 모델은요</p><h2>{e(m['tagline'])}</h2><p>{e(m['description'])}</p></div>{compact_comparison(slug)}{color_section(m)}{edition_cards(slug)}<div class="variant-list"><h2>같은 모델, 다른 구성.</h2><p>공식 모델 안내·가격표에서 확인한 구성입니다. 사진으로 보는 대표 구성 외에 함께 상담할 구성도 정리했습니다. 현재 판매·배정 가능 여부와 옵션은 상담 시 확인합니다.</p><ul>{variant_rows}</ul></div><section class="check-section"><h2>시승에서 확인할 세 가지.</h2><div class="check-grid">{checks}</div></section><section class="model-finance">{finance}</section>{model_faq(m)}{consultation(m)}<p class="source-note">공식 정보 확인: 2026.09.22 · {external(v['source'], 'BMW Korea 모델 안내')}</p><section class="related-models"><h2>함께 살펴보면 좋은 모델.</h2><div class="catalog-grid related-grid">{''.join(card(x) for x in related)}</div></section></section><script type="application/json" id="model-data">{safe_json({'variants': [{k: v for k, v in variant.items() if not k.endswith('Source')} for variant in m['variants']]})}</script>'''
    if slug in {'3-series', 'i3'}:
        body = body.replace('<div class="model-stage">', model_preview_link() + '<div class="model-stage">', 1)
    path = f'/models/{slug}/'
    schema = {'@context': 'https://schema.org', '@graph': [{'@type': 'WebPage', 'name': name + ' 모델·구매 상담 안내', 'url': ORIGIN + path, 'inLanguage': 'ko-KR', 'description': m['description'], 'about': {'@type': 'Car', 'name': name, 'brand': {'@type': 'Brand', 'name': 'BMW'}, 'image': ORIGIN + v['image']}, 'author': {'@type': 'Person', '@id': ORIGIN + '/#advisor', 'name': '백경재'}}, {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': '홈', 'item': ORIGIN + '/'}, {'@type': 'ListItem', 'position': 2, 'name': '모델 안내', 'item': ORIGIN + '/models/'}, {'@type': 'ListItem', 'position': 3, 'name': name, 'item': ORIGIN + path}]}]}
    write_page(path, document(name + ' 모델·파생 구성·상담 | 한남 전시장 백경재', m['description'], path, body, schema, v['image']))


def finance_page():
    write_page('/finance/', document('BMW 구매 혜택·납입 지원 안내 | 백경재 대리', f'{PERIOD} BMW 5시리즈·i5의 납입 지원 혜택을 백경재 대리가 쉽게 정리했습니다. 적용 조건과 공식 원문을 확인하세요.', '/finance/', finance_body(FINANCE, MODELS)))


def homepage():
    p = DIST / 'index.html'
    html = p.read_text()
    section = home_sections(MODELS, FINANCE)
    if '<!-- catalog-home:start -->' in html:
        html = re.sub(r'<!-- catalog-home:start -->[\s\S]*?<!-- catalog-home:end -->', lambda _: section, html)
    else:
        html, n = re.subn(r'<section class="models section wrap"[\s\S]*?</section>', lambda _: section, html, count=1)
        assert n == 1, 'Home model section not found'
    if '/catalog.css' not in html:
        html = html.replace('<link rel="stylesheet" href="/styles.css">', '<link rel="stylesheet" href="/styles.css">\n<link rel="stylesheet" href="/catalog.css">')
    if '/catalog.js' not in html:
        html = html.replace('<script src="/app.js" defer></script>', '<script src="/app.js" defer></script>\n<script src="/catalog.js" defer></script>')
    html = re.sub(r'<a class="skip"[^>]*>.*?</a>\s*<header[\s\S]*?</header>(?:<aside class="personal-site-notice">[\s\S]*?</aside>)?', lambda _: header(), html, count=1)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    soup.select_one('#hero').replace_with(BeautifulSoup(home_hero(), 'html.parser'))
    for item in soup.select('#faq [data-advisor-faq]'):
        item.decompose()
    target = soup.select_one('#faq .faq-list')
    for key in ['model-year', 'availability', 'colors']:
        item = FAQ[key]
        row = BeautifulSoup(f'<details data-advisor-faq="{key}"><summary>{e(item["question"])}<span class="faq-toggle" aria-hidden="true"></span></summary><div class="faq-answer">{e(item["answer"])}</div></details>', 'html.parser')
        target.append(row)
    more = soup.select_one('#faq .guide-more-link')
    if not more:
        target.append(BeautifulSoup(f'<p class="guide-more-link"><a href="{GUIDE_PATH}#guide-questions">좌석·에디션·구매 방식도 더 알아보기 →</a></p>', 'html.parser'))
    profile = soup.select_one('.advisor-copy blockquote')
    if profile:
        profile.clear()
        profile.append('“고객의 입장을 먼저 생각합니다.”')
    html = str(soup)
    html = html.replace('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>', '')
    p.write_text(html)


def privacy_header():
    p = DIST / 'privacy.html'
    html = p.read_text()
    if '/catalog.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/catalog.css"></head>')
    html = re.sub(r'(?:<a class="skip"[^>]*>.*?</a>\s*)?<header[\s\S]*?</header>(?:<aside class="personal-site-notice">[\s\S]*?</aside>)?', lambda _: header(), html, count=1)
    p.write_text(html)


if __name__ == '__main__':
    catalog()
    write_page('/models/', document('BMW 세단·SUV·해치백 모델 안내 | 백경재 대리', '세단·SUV·해치백부터 골라보세요. 모델별 사진과 백경재 대리의 한 줄 코멘트로 나에게 맞는 BMW를 살펴보세요.', '/models/', lineup_hub(MODELS)))
    category_pages(MODELS, card, write_page, document)
    for model in MODELS:
        model_page(model)
    finance_page()
    write_page(PREVIEW_PATH, document('신형 BMW 3시리즈·i3 사진 미리보기 | 백경재 대리', '글로벌 공개된 신형 BMW 3시리즈와 i3의 외관·실내 사진 10장. 국내 출시 일정·가격·사양은 별도 확인이 필요한 신차 미리보기입니다.', PREVIEW_PATH, preview_body(), {'@context':'https://schema.org','@type':'Article','headline':'신형 BMW 3시리즈와 i3 사진 미리보기','datePublished':'2026-09-30','dateModified':'2026-09-30','inLanguage':'ko-KR','author':{'@type':'Person','name':'백경재','url':ORIGIN+'/#advisor'},'image':ORIGIN+ASSETS+'duo-1600.webp','mainEntityOfPage':ORIGIN+PREVIEW_PATH,'citation':PRESS_SOURCE}, ASSETS+'duo-1600.webp'))
    write_page(GUIDE_PATH, document('BMW 구매 가이드 · 연식·색상·좌석 선택 | 백경재 대리', '백경재 대리가 영상에서 이야기한 모델 선택 기준과 색상 취향. 연식 변경, 재고 확인, X7 6·7인승, 한정 에디션을 구매 전에 살펴보세요.', GUIDE_PATH, buying_guide(MODELS), {'@context':'https://schema.org','@type':'Article','headline':'BMW 구매 전, 함께 확인할 것들','inLanguage':'ko-KR','url':ORIGIN+GUIDE_PATH,'dateModified':'2026-09-30','author':{'@type':'Person','name':'백경재','url':ORIGIN+'/#advisor'},'mainEntityOfPage':ORIGIN+GUIDE_PATH}))
    homepage()
    privacy_header()
    print(f'Generated {len(MODELS)} model pages, catalogue, finance and homepage sections.')
