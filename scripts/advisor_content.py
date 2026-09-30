"""Render reviewed advisor content. Inventory and financial offers are not inferred from video."""
from pathlib import Path
from html import escape as e
from urllib.parse import quote
import json

ROOT = Path(__file__).resolve().parents[1]
GUIDE = json.loads((ROOT / 'data/advisor-guide.json').read_text())
GUIDE_PATH = '/guides/bmw-selection/'
FAQ = {f['id']: f for f in GUIDE['faqs']}


def source_link(url, label):
    return f'<a class="source-link" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗<span class="sr-only"> (새 창)</span></a>'


def faq_list(ids, heading='구매 전 자주 묻는 질문', anchor='buying-questions'):
    rows = ''.join(f'<details id="{anchor}-{key}"><summary>{e(FAQ[key]["question"])}<span class="faq-toggle" aria-hidden="true"></span></summary><div class="faq-answer">{e(FAQ[key]["answer"])}</div></details>' for key in ids)
    return f'<section class="advisor-faq" id="{anchor}"><h2>{e(heading)}</h2><div class="faq-list">{rows}</div></section>'


def model_faq(model):
    slug = model['slug']
    ids = ['availability', 'colors']
    extra = 'edition' if slug in ['i4', 'x2'] else 'seats' if slug == 'x7' else 'body-style' if slug.startswith('4-') else 'online' if slug == 'x5' else 'model-year'
    return faq_list([extra] + ids) + f'<p class="guide-inline-link"><a href="{GUIDE_PATH}">연식·색상·구매 방식 안내 →</a></p>'


def color_section(model):
    colors = GUIDE['colors'].get(model['slug'], [])
    if not colors:
        return ''
    buttons = ''.join(f'<button type="button" class="color-choice" data-consult-color="{e(c)}" aria-pressed="false">{e(c)}<span aria-hidden="true">＋</span></button>' for c in colors)
    return f'''<section class="advisor-colors" aria-labelledby="color-heading"><p class="kicker">외장색 선택</p><h2 id="color-heading">영상에 나온 색상</h2><p>색상을 누르면 아래 문의 내용에 추가됩니다. 목록에 없는 색상은 직접 입력해 주세요.</p><div class="color-choices">{buttons}</div><p class="source-note">모델·연식·패키지에 따라 선택 가능한 색상이 다릅니다. 재고와 실내색 조합은 문의 후 확인합니다.</p></section>'''


def edition_cards(slug=None):
    editions = [item for item in GUIDE['editions'] if not slug or item['slug'] == slug]
    if not editions:
        return ''
    cards = []
    for item in editions:
        photo = f'<figure><img src="{item["image"]}" width="1600" height="960" alt="{e(item["imageAlt"])}" loading="lazy" decoding="async"><figcaption>BMW 공식 에디션 이미지 · © BMW AG</figcaption></figure>' if item.get('image') else '<div class="edition-type" aria-hidden="true">X2 <span>FROZEN PURE GREY</span></div>'
        cards.append(f'''<article class="edition-card">{photo}<div class="edition-copy"><span class="editorial-label">{e(item['release'])} 출시 소개</span><h3>{e(item['name'])}</h3><p class="edition-color">{e(item['color'])}</p><p>{e(item['description'])}</p><p class="source-note">출시 당시 구성을 소개합니다. 현재 판매·배정 여부와 적용 사양은 별도로 확인합니다.</p><div class="edition-links">{source_link(item['source'],'공식 에디션 소개')}<a href="/models/{item['slug']}/?edition={item['slug']}#consultation">이 구성으로 상담하기 →</a></div></div></article>''')
    return '<section class="advisor-editions"><p class="kicker">한정 에디션</p><h2>일반 모델과 다른 색상·옵션</h2><div class="edition-grid">' + ''.join(cards) + '</div></section>'


def consultation(model):
    name = model['name']
    choices = list(dict.fromkeys([v['name'] for v in model['variants']] + [v['name'] for v in model.get('additionalVariants', [])]))
    options = '<option value="">아직 정하지 않았어요</option>' + ''.join(f'<option value="{e(x)}">{e(x)}</option>' for x in choices)
    options += ''.join(f'<option value="{e(item["name"])}" data-edition="{item["slug"]}" data-exterior="{e(item["color"])}">{e(item["name"])} (판매 여부 확인)</option>' for item in GUIDE['editions'] if item['slug'] == model['slug'])
    seats = '''<label>좌석 구성<select id="consult-seats"><option value="">아직 정하지 않았어요</option><option>6인승</option><option>7인승</option></select><small>선택한 트림에 적용 가능한 구성은 확인이 필요합니다.</small></label>''' if model['slug'] == 'x7' else ''
    sms = 'sms:01083089819?body=' + quote(f'안녕하세요. {name} 상담을 받고 싶습니다. 희망 트림과 색상, 출고 시기에 맞는 구성을 확인하고 싶습니다.')
    return f'''<section class="consultation-builder" id="consultation" data-consultation-model="{e(name)}"><div class="consultation-intro"><p class="kicker">백경재 대리에게 물어보세요</p><h2>원하는 트림과 색상을<br>알려주세요.</h2><p>아래에서 조건을 고르면 문의할 내용이 정리됩니다. 해당 조건의 차량이 있는지는 문의 후 확인해 드리겠습니다.</p></div><div class="consultation-fields"><label>관심 트림<select id="consult-variant">{options}</select></label>{seats}<label>희망 외장색<input id="consult-exterior" type="text" maxlength="80" placeholder="예: 화이트 / 다른 색상도 괜찮아요" autocomplete="off"></label><label>희망 실내색<input id="consult-interior" type="text" maxlength="80" placeholder="정하지 않으셨다면 비워두세요" autocomplete="off"></label><label>출고 희망 시기<input id="consult-timing" type="text" maxlength="80" placeholder="예: 11월 중 / 일정 상담" autocomplete="off"></label></div><div class="consultation-preview"><label for="consult-message">문의 내용 미리보기</label><textarea id="consult-message" rows="7" readonly>안녕하세요. {e(name)} 상담을 받고 싶습니다. 희망 트림과 색상, 출고 시기에 맞는 구성을 확인하고 싶습니다.</textarea><p class="source-note">카카오톡에서는 내용을 복사해 붙여넣을 수 있습니다. 메시지는 직접 확인한 뒤 보내주세요.</p><div class="consultation-actions"><button type="button" class="button outline-button" id="copy-consultation" hidden>문의 내용 복사</button><a class="button kakao-button" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">카카오톡 상담 ↗<span class="sr-only"> (새 창)</span></a><a class="button outline-button" id="consult-sms" href="{sms}">문자로 문의</a><a class="text-link" href="tel:01083089819">전화 상담 ↗</a></div><p id="consult-status" class="consultation-status" role="status" aria-live="polite"></p><noscript><p>희망 조건을 전화나 카카오톡으로 알려주세요. 내용 자동 정리 기능은 JavaScript를 켜면 사용할 수 있습니다.</p></noscript></div></section>'''


def home_teaser():
    return f'''<section class="section advisor-guide-teaser"><div class="wrap"><div><p class="kicker">백경재 대리의 구매 가이드</p><h2>연식·색상·좌석,<br>구매 전에 확인하세요.</h2><p>연식 변경과 풀체인지의 차이, 색상별 재고, X7 좌석 구성 등<br>구매 전에 확인할 내용을 정리했습니다.</p><a class="button outline-button" href="{GUIDE_PATH}">구매 가이드 보기 →</a></div><div class="guide-teaser-quote"><span class="editorial-label">백경재 대리의 취향</span><blockquote>“4시리즈 색상 중에서는<br>케이프 요크 그린이<br>제일 마음에 듭니다.”</blockquote><a href="/models/4-gran-coupe/">4시리즈 그란 쿠페 살펴보기 →</a></div></div></section>'''


def buying_guide(models):
    by = {m['slug']: m for m in models}
    body = f'''<div class="wrap breadcrumb"><a href="/">홈</a><span>/</span><a href="/models/">BMW 라인업</a><span>/</span>구매 가이드</div><article class="wrap buying-guide"><header class="guide-hero"><div><p class="kicker">백경재 대리의 구매 가이드</p><h1>BMW 구매 전,<br>이것부터 확인하세요.</h1><p class="lead">연식 변경과 풀체인지는 무엇이 다를까요?<br>모델 비교부터 색상·좌석 선택까지 정리했습니다.</p><p class="source-note">백경재 대리 · 2026.09.30 정리</p></div><img src="/assets/baek-gyeongjae.webp" width="260" height="320" alt="BMW 한남전시장 백경재 대리"></header><nav class="guide-jump-links" aria-label="구매 가이드 목차"><a href="#selection">모델별 체크포인트</a><a href="#taste">백경재 대리의 취향</a><a href="#guide-questions">구매 FAQ</a></nav><div class="guide-principle"><strong>모델을 아직 못 정하셨다면</strong><p>예산과 주로 타실 인원을 알려주세요. 비교할 모델부터 말씀드리겠습니다. 재고와 구매 조건은 문의하실 때 확인합니다.</p></div><section id="selection"><p class="kicker">모델 비교</p><h2>모델별로 확인할 점</h2><div class="selection-grid">'''
    for item in GUIDE['selection']:
        links = ''.join(f'<a href="/models/{slug}/">{e(by[slug]["name"].replace("BMW ",""))} →</a>' for slug in item['models'])
        body += f'<article class="selection-card"><span class="editorial-label">{e(item["label"])}</span><h3>{e(item["title"])}</h3><p>{e(item["description"])}</p><div class="selection-links">{links}</div></article>'
    body += '</div></section><section id="taste" class="guide-taste"><p class="kicker">백경재 대리의 한 줄</p><h2>영상에서 고른 모델과 색상</h2><div class="taste-grid">'
    for slug in ['2-active-tourer', '4-gran-coupe', 'x2', 'x6', 'z4']:
        model = by[slug]
        body += f'<article><h3>{e(model["name"])}</h3><p>{e(model["advisorComment"])}</p><a href="/models/{slug}/">모델 보기 →</a></article>'
    body += '</div></section>' + edition_cards() + faq_list(list(FAQ), anchor='guide-questions')
    body += f'''<section class="guide-source" id="source"><h2>자료 출처</h2><p>백경재 대리의 10월 모델 안내 영상을 바탕으로 작성했습니다. 개인 코멘트는 영상의 실제 발언을 짧게 정리한 문장입니다.</p><p>재고와 출고 안내는 촬영 당시 기준입니다. 현재 판매 여부와 구매 조건은 별도로 확인해 주세요. 사양과 에디션 구성은 각 항목에 연결한 BMW 공식 자료를 참고했습니다.</p>{source_link('https://www.youtube.com/@bmw_gjbaek','BMW는 끼쟁이 유튜브 채널')}<p class="source-note">정리일 2026.09.30 · 백경재 대리 개인 상담 사이트</p></section><div class="guide-final-contact"><h2>원하는 모델의 재고를<br>문의해 주세요.</h2><a class="button primary" href="/models/">모델을 골라 상담하기 →</a><a class="button kakao-button" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">카카오톡으로 물어보기 ↗<span class="sr-only"> (새 창)</span></a></div></article>'''
    return body
