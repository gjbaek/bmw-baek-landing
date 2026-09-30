"""Editorial preview of user-supplied global press images, separate from sale models."""
from html import escape as e

PREVIEW_PATH = '/stories/new-3-series/'
ASSETS = '/assets/new-3-series/'
PRESS_SOURCE = 'https://www.press.bmwgroup.com/global/photo/compilation/T0460993EN/the-new-bmw-3-series?language=en'
PHOTOS = [
    ('duo', 'exterior', '3시리즈와 i3 · 외관', '신형 3시리즈와 순수전기 i3가 나란히 선 모습.', 'P90657627', 1600, 1067),
    ('duo-driving', 'exterior', '3시리즈와 i3 · 주행 사진', '두 모델의 앞모습과 옆모습.', 'P90657629', 1600, 1067),
    ('320-driving', 'exterior', 'BMW 320의 옆모습.', '보닛에서 지붕으로 이어지는 옆모습.', 'P90657728', 1600, 1067),
    ('duo-portrait', 'exterior', '전면·후면 비교', '전면과 후면을 한 장에 담은 사진.', 'P90658030', 1254, 1500),
    ('320-cockpit', '3-interior', 'BMW 320 · 운전석.', '스티어링 휠, 가로로 이어지는 표시 영역과 중앙 화면.', 'P90657778', 1600, 1067),
    ('320-wheel', '3-interior', 'BMW 320 · 디테일.', '창 너머로 보이는 밝은 색상의 스티어링 휠.', 'P90657777', 1600, 1067),
    ('320-rear-seat', '3-interior', 'BMW 320 · 뒷좌석.', '뒷좌석 시트와 유리 지붕.', 'P90657783', 1600, 1067),
    ('i3-cockpit', 'i3-interior', 'BMW i3 50 xDrive · 운전석.', '대시보드, 스티어링 휠과 중앙 화면.', 'P90657750', 1600, 1098),
    ('i3-rear-seat', 'i3-interior', 'BMW i3 50 xDrive · 뒷좌석.', '뒷좌석 시트와 천장.', 'P90657762', 1600, 1067),
    ('i3-m60-cockpit', 'i3-interior', 'BMW i3 M60 xDrive · 프로토타입.', 'M 스티어링 휠과 화면 구성. 최종 양산 사양과 다를 수 있습니다.', 'P90657927', 1600, 1600),
]


def home_hero():
    return f'''<section class="hero launch-hero" id="hero" aria-labelledby="hero-title">
<picture class="launch-hero-photo"><source media="(max-width: 700px)" srcset="{ASSETS}duo-portrait-800.webp"><img src="{ASSETS}duo-1600.webp" width="1600" height="1067" alt="해외 공개된 신형 BMW 3시리즈와 순수전기 i3" fetchpriority="high" decoding="async"></picture>
<div class="launch-shade" aria-hidden="true"></div><div class="wrap launch-copy"><p class="launch-kicker">백경재 대리의 신차 미리보기 <span>글로벌 공개</span></p><h1 id="hero-title">신형 3시리즈,<br>사진 공개됐습니다.</h1><p class="launch-description">3시리즈와 순수전기 i3의<br>외관·실내 사진 10장을 모았습니다.</p><div class="launch-actions"><a class="button white-button" href="{PREVIEW_PATH}">외관·실내 미리보기 <span aria-hidden="true">↗</span></a><a href="/models/">상담할 BMW 찾기 <span aria-hidden="true">→</span></a></div></div>
<div class="wrap launch-caption"><span>THE NEW 3 SERIES <b>&amp; i3</b></span><p>글로벌 공개 이미지 · 국내 출시 일정·가격·사양은 별도 확인<br>사진 © BMW AG</p></div></section>'''


def model_preview_link():
    return f'<aside class="model-preview-link"><div><span class="editorial-label">해외 신차 소식</span><strong>신형 3시리즈·i3 공개 사진</strong><p>해외 공개 사진입니다. 국내 판매 사양과는 다를 수 있습니다.</p></div><a href="{PREVIEW_PATH}">공개 사진 보기 →</a></aside>'


def preview_body():
    cards = []
    for i, (asset, group, title, caption, photo_id, width, height) in enumerate(PHOTOS):
        cards.append(f'''<figure class="preview-photo" data-photo-group="{group}"><a class="preview-photo-open" href="{ASSETS}{asset}-1600.webp" data-photo-index="{i}" aria-label="{e(title)} 사진 크게 보기"><img src="{ASSETS}{asset}-800.webp" srcset="{ASSETS}{asset}-800.webp 800w, {ASSETS}{asset}-1600.webp {width}w" sizes="(max-width: 760px) calc(100vw - 44px), (max-width: 1200px) 46vw, 560px" width="{width}" height="{height}" alt="{e(title+' '+caption)}" loading="lazy" decoding="async"><span class="photo-expand" aria-hidden="true">크게 보기 ＋</span></a><figcaption><strong>{e(title)}</strong><p>{e(caption)}</p><small>글로벌 공개 이미지 · {photo_id} · © BMW AG</small></figcaption></figure>''')
    return f'''<div class="wrap breadcrumb"><a href="/">홈</a><span>/</span>신형 3시리즈 미리보기</div><article class="new-model-story wrap"><header class="preview-heading"><p class="kicker">백경재 대리의 신차 미리보기</p><h1>신형 3시리즈·i3<br><span>외관과 실내 사진</span></h1><p class="lead">앞모습, 운전석, 뒷좌석을 사진으로 확인하세요.<br>BMW가 해외에서 공개한 사진 10장입니다.</p><p class="source-note">사진 공개 2026.09.30 · 백경재 대리 정리</p></header>
<div class="preview-scope"><strong>해외 공개 모델의 사진입니다.</strong><p>국내 출시 일정, 가격과 판매 트림은 별도 확인이 필요합니다. 사진의 색상·옵션·화면 구성은 국내 판매 사양과 다를 수 있습니다.</p></div>
<nav class="preview-filters" aria-label="사진 분류" hidden><button type="button" data-photo-filter="all" aria-pressed="true">전체 <span>10</span></button><button type="button" data-photo-filter="exterior" aria-pressed="false">외관 <span>4</span></button><button type="button" data-photo-filter="3-interior" aria-pressed="false">3시리즈 실내 <span>3</span></button><button type="button" data-photo-filter="i3-interior" aria-pressed="false">i3 실내 <span>3</span></button></nav><p id="photo-result" class="source-note" role="status">사진 10장 · 사진을 누르면 크게 볼 수 있습니다.</p>
<div class="preview-gallery">{''.join(cards)}</div>
<section class="preview-reading"><p class="kicker">사진 속 모델 안내</p><h2>사진 아래 모델명을<br>확인하세요.</h2><div><p>BMW 320 등 3시리즈와 전기 세단 i3의 사진이 섞여 있습니다. 사진 아래 모델명을 확인하세요. 실내 구성도 모델에 따라 다릅니다.</p><p>i3 M60 xDrive 실내는 BMW가 프로토타입으로 공개한 이미지입니다. 사진에 보이는 장비나 디자인이 모든 모델에 동일하게 적용된다는 뜻은 아닙니다.</p><a class="source-link" href="{PRESS_SOURCE}" target="_blank" rel="noopener noreferrer">BMW 공식 공개 사진 확인 ↗<span class="sr-only"> (새 창)</span></a></div></section>
<section class="preview-next"><div><p class="kicker">구매 상담</p><h2>지금 구매할 차량을<br>찾고 계신가요?</h2><p>관심 모델과 구매 시기를 알려주세요.<br>현재 판매 중인 차량과 출고 가능 여부를 확인해 드리겠습니다.</p></div><div class="preview-next-links"><a class="button outline-button" href="/models/3-series/">기존 3시리즈 안내 →</a><a class="button outline-button" href="/models/5-series/">5시리즈 보기 →</a><a class="button kakao-button" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">백경재 대리에게 문의 ↗<span class="sr-only"> (새 창)</span></a></div></section></article>
<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-dialog-title"><div class="photo-dialog-bar"><p id="photo-dialog-counter"></p><button type="button" id="photo-dialog-close" aria-label="사진 닫기">닫기 ✕</button></div><img id="photo-dialog-image" alt=""><div class="photo-dialog-bottom"><button type="button" id="photo-dialog-prev" aria-label="이전 사진">←</button><div><h2 id="photo-dialog-title"></h2><p id="photo-dialog-caption"></p></div><button type="button" id="photo-dialog-next" aria-label="다음 사진">→</button></div></dialog><script src="/preview-gallery.js" defer></script>'''
