# -*- coding: utf-8 -*-
"""Shared navigation and the advisor-led entry points used on every page."""
from html import escape as e
from advisor_content import home_teaser, GUIDE_PATH

GROUPS = [
    {'slug': 'sedan', 'name': '세단', 'photo': '5-series', 'intro': '3·5·7시리즈와 i3·i5·i7 전기 세단.', 'models': ['3-series', '5-series', '7-series', 'i3', 'i5', 'i7', 'm3', 'm5'], 'related': ['2-gran-coupe', '4-gran-coupe', '8-gran-coupe', 'i4', '3-touring', 'm3-touring', 'm5-touring'], 'relatedTitle': '그란 쿠페·투어링도 비교하기'},
    {'slug': 'suv', 'name': 'SUV', 'photo': 'x3', 'intro': 'X1부터 X7, 전기 SUV와 M까지.', 'models': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'ix1', 'ix2', 'ix3', 'ix', 'xm', 'x5-m', 'x6-m'], 'related': [], 'relatedTitle': ''},
    {'slug': 'hatchback', 'name': '해치백', 'photo': '1-series', 'intro': '5도어 해치백 1시리즈.', 'models': ['1-series'], 'related': ['2-active-tourer', '2-gran-coupe', 'x1'], 'relatedTitle': '액티브 투어러·그란 쿠페·X1 비교'}
]


def header():
    return '''<a class="skip" href="#main">본문으로 바로가기</a><header class="header site-header"><a class="brand" href="/" aria-label="백경재 대리 개인 상담 사이트 홈"><img class="brand-portrait" src="/assets/baek-gyeongjae.webp" width="46" height="46" alt="백경재 대리"><span><strong class="dealer-brand-name">백경재 대리</strong><small>BMW 도이치모터스 · 한남 전시장</small></span></a><nav class="desktop-nav" aria-label="주요 메뉴"><a href="/models/">BMW 라인업</a><a href="/finance/">구매 혜택</a><a href="/#advisor">백경재 소개</a><a href="/#showroom">전시장 안내</a><a href="/#videos">BMW는 끼쟁이</a></nav><a class="header-contact" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">카카오톡 상담 <span aria-hidden="true">↗</span><span class="sr-only"> (새 창)</span></a></header><aside class="personal-site-notice">백경재 대리가 직접 운영하는 개인 상담 사이트입니다. <span>BMW Korea 기업 공식 홈페이지와 별도로 운영됩니다.</span></aside>'''


def group_cards(models):
    by_slug = {m['slug']: m for m in models}
    cards = []
    for group in GROUPS:
        model = by_slug[group['photo']]
        cards.append(f'''<a class="lineup-entry" href="/models/{group['slug']}/"><div><span class="lineup-eyebrow">BMW 라인업</span><h3>{group['name']}</h3></div><img src="{model['variants'][0]['image']}" width="1128" height="921" alt="{e(model['name'])} 대표 이미지" loading="lazy"><p>{group['intro']}</p><span class="lineup-action">모델 고르기 <span aria-hidden="true">→</span></span></a>''')
    return '<div class="lineup-entries">' + ''.join(cards) + '</div>'


def lineup_hub(models):
    return f'''<section class="wrap lineup-hub"><p class="kicker">백경재 대리의 모델 안내</p><h1>어떤 차를<br>생각하고 계신가요?</h1><p class="lead">세단·SUV·해치백 중에서 고르면 모델별 사진과 설명을 볼 수 있습니다.</p>{group_cards(models)}<p class="lineup-other">쿠페·컨버터블·투어링도 찾으시나요? <a href="/models/all/">전체 모델 보기 →</a></p><div class="advisor-intro-note"><img src="/assets/baek-gyeongjae.webp" width="64" height="64" alt="백경재 대리"><p>연식과 옵션은 무엇이 다른지,<br>원하는 색상은 언제 출고되는지 궁금하신가요?</p><a href="{GUIDE_PATH}">구매 가이드 보기 →</a></div></section>'''


def category_pages(models, card, write_page, document):
    by_slug = {m['slug']: m for m in models}
    for group in GROUPS:
        related = ''
        if group['related']:
            note = '<p class="source-note">액티브 투어러는 MPV입니다. 1시리즈와 차체 형태가 다르니 뒷좌석과 짐 공간을 비교해 보세요.</p>' if group['slug'] == 'hatchback' else ''
            related = f'<section class="category-related"><h2>{group["relatedTitle"]}</h2>{note}<div class="catalog-grid">' + ''.join(card(by_slug[slug]) for slug in group['related']) + '</div></section>'
        body = f'''<div class="wrap breadcrumb"><a href="/models/">BMW 라인업</a><span>/</span>{group['name']}</div><section class="wrap category-models"><p class="kicker">백경재 대리의 모델 안내</p><h1>BMW {group['name']}</h1><p class="lead">{group['intro']}<br>모델을 누르면 사진과 설명을 볼 수 있습니다.</p><div class="lineup-tabs" aria-label="라인업 선택">{''.join(f'<a href="/models/{g["slug"]}/" aria-current="{"page" if g["slug"] == group["slug"] else "false"}">{g["name"]}</a>' for g in GROUPS)}</div><div class="catalog-grid">{''.join(card(by_slug[slug]) for slug in group['models'])}</div>{related}<p class="lineup-other"><a href="/models/all/">쿠페·투어링·M을 포함한 전체 모델 보기 →</a></p></section>'''
        path = '/models/' + group['slug'] + '/'
        write_page(path, document(f'BMW {group["name"]} 모델 고르기 | 백경재 대리', group['intro'] + ' 모델별 사진, 트림과 구매 전 확인할 점을 정리했습니다.', path, body))


def comment_block(model):
    source = model.get('advisorCommentSource')
    label = '백경재 대리의 한 줄 코멘트' if source else '구매 전 확인할 점'
    caption = '영상에서 한 말' if source else '차량 선택 가이드'
    portrait = '<img src="/assets/baek-gyeongjae.webp" width="56" height="56" alt="백경재 대리">' if source else ''
    note = f'<p class="comment-source"><a href="{GUIDE_PATH}#source">모델 안내 영상에서 정리</a> · {e(source["time"])} · {e(source["reviewedAt"])}</p>' if source else ''
    return f'''<aside class="advisor-comment"><div class="comment-author">{portrait}<div><p>{label}</p><span>{caption}</span></div></div><p class="comment-copy">{e(model['advisorComment'])}</p>{note}</aside>'''


def benefit_cards(finance, models):
    by_slug = {m['slug']: m for m in models}
    cards = []
    for benefit in finance['benefits']:
        model = by_slug[benefit['modelSlug']]
        rows = ''.join(f'''<li class="benefit-row"><div><span>{e(item['label'])}</span><strong>월 최대 {item['monthlyMax']}만 원 × {item['months']}개월</strong></div><p>총 최대 <b>{item['totalMax']:,}만 원</b> 지원</p></li>''' for item in benefit['items'])
        cards.append(f'''<article class="benefit-card" id="benefit-{benefit['modelSlug']}"><div class="benefit-heading"><div><p class="kicker">월 납입금 지원 프로그램</p><h2>{benefit['name']}</h2></div><img src="{model['variants'][0]['image']}" width="1128" height="921" alt="{e(model['name'])} 대표 이미지" loading="lazy"></div><ul>{rows}</ul><p class="benefit-note">{e(benefit['note'])}</p><div class="benefit-links"><a href="{benefit['source']}" target="_blank" rel="noopener noreferrer">BMW 공식 조건 확인 ↗<span class="sr-only"> (새 창)</span></a><a href="/models/{model['slug']}/">모델 살펴보기 →</a></div></article>''')
    return '<div class="benefit-grid">' + ''.join(cards) + '</div>'


def period_label(finance):
    year, month = finance['validFrom'][:7].split('-')
    period = f'{year}년 {int(month)}월'
    return f'''<p class="period-label" data-promotion-period data-from="{finance['validFrom']}" data-through="{finance['validThrough']}" data-period="{period}">{period} 안내 · 적용 {finance['validFrom'].replace('-', '.')}–{finance['validThrough'].replace('-', '.')} · 확인 {finance['checkedAt'].replace('-', '.')}</p>'''


def finance_body(finance, models):
    return f'''<section class="wrap benefits-intro"><p class="kicker">백경재 대리가 정리한 구매 혜택</p><h1>할부·리스<br>납입 지원 안내</h1><p class="lead">5시리즈와 i5의 납입 지원금과 적용 조건입니다.<br>지원 여부는 모델과 구매 방식에 따라 다릅니다.</p>{period_label(finance)}</section><section class="wrap benefits-content" aria-label="모델별 납입 지원 혜택">{benefit_cards(finance,models)}<p class="source-note">BMW 파이낸셜 서비스의 공개 프로모션을 요약한 정보입니다. 대상 차량·상품·계약 조건에 따라 적용 여부가 달라지며, 지원 금액이 차량 가격에서 바로 할인되는 금액을 뜻하지는 않습니다. 실제 적용 조건은 최종 견적에서 확인해 주세요.</p><section class="benefits-guide" id="finance-guide"><h2>지원 대상인지<br>확인하려면</h2><div class="benefit-checks"><article><span>01</span><h3>관심 있는 모델</h3><p>모델과 트림, 구매 예정 시기를 알려주세요.</p></article><article><span>02</span><h3>생각 중인 구매 방식</h3><p>현금·할부·리스 중 고민하는 방식을 말씀해 주세요.</p></article><article><span>03</span><h3>적용 가능한 혜택</h3><p>지원 기간과 지급 방식, 다른 혜택과의 중복 여부를 확인합니다.</p></article></div><div class="benefit-contact"><img src="/assets/baek-gyeongjae.webp" width="72" height="72" alt="백경재 대리"><div><strong>관심 모델과 구매 방식을 알려주세요.</strong><p>적용 가능한 지원금과 조건을 확인해 드리겠습니다.</p></div><a class="button kakao-button" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">백경재 대리에게 문의 ↗<span class="sr-only"> (새 창)</span></a></div></section></section>'''


def home_sections(models, finance):
    return f'''<!-- catalog-home:start --><section class="section wrap home-catalog" id="models" aria-labelledby="models-title"><div class="section-heading"><div><p class="eyebrow dark-eyebrow">백경재 대리의 모델 안내</p><h2 id="models-title">어떤 차를<br>생각하고 계신가요?</h2></div><p class="section-description">세단·SUV·해치백 중에서 고르면<br>모델별 사진과 설명을 볼 수 있습니다.</p></div>{group_cards(models)}<p class="lineup-other"><a href="/models/all/">쿠페·투어링·M을 포함한 전체 모델 보기 →</a></p></section>{home_teaser()}<section class="section home-benefits" id="finance"><div class="wrap"><div><p class="kicker">할부·리스 혜택</p><h2>5시리즈·i5<br>납입 지원 안내</h2><p>할부와 리스는 지원 금액과 기간이 다릅니다.<br>모델별 지원 내용과 적용 조건을 확인하세요.</p>{period_label(finance)}<a class="button outline-button" href="/finance/">구매 혜택 살펴보기 →</a></div><div class="home-benefits-note"><img src="/assets/baek-gyeongjae.webp" width="70" height="70" alt="백경재 대리"><p>같은 모델이라도<br>할부·리스 조건은 다릅니다.</p><span>어떤 방식으로 구매할지 알려주시면 확인해 드리겠습니다.</span></div></div></section><!-- catalog-home:end -->'''
