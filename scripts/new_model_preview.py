"""Editorial preview of user-supplied global press images, separate from sale models."""
from html import escape as e

PREVIEW_PATH = '/stories/new-3-series/'
ASSETS = '/assets/new-3-series/'
PRESS_SOURCE = 'https://www.press.bmwgroup.com/global/photo/compilation/T0460993EN/the-new-bmw-3-series?language=en'
PHOTOS = [
    ('duo', 'exterior', '3시리즈와 i3, 나란히.', '신형 3시리즈와 순수전기 i3의 외관을 함께 살펴보세요.', 'P90657627', 1600, 1067),
    ('duo-driving', 'exterior', '움직임 속의 두 모델.', '주행 장면에서 보이는 전면과 차체의 비례.', 'P90657629', 1600, 1067),
    ('320-driving', 'exterior', 'BMW 320의 옆모습.', '낮게 이어지는 보닛과 루프 라인을 살펴보세요.', 'P90657728', 1600, 1067),
    ('duo-portrait', 'exterior', '앞과 뒤, 다른 인상.', '같은 장면 안에서 전면과 후면 디자인을 비교해 보세요.', 'P90658030', 1254, 1500),
    ('320-cockpit', '3-interior', 'BMW 320 · 운전석.', '스티어링 휠, 가로로 이어지는 표시 영역과 중앙 화면.', 'P90657778', 1600, 1067),
    ('320-wheel', '3-interior', 'BMW 320 · 디테일.', '창 너머로 보이는 밝은 색상의 스티어링 휠.', 'P90657777', 1600, 1067),
    ('320-rear-seat', '3-interior', 'BMW 320 · 뒷좌석.', '시트 색상과 뒷좌석, 유리 지붕이 만드는 실내 분위기.', 'P90657783', 1600, 1067),
    ('i3-cockpit', 'i3-interior', 'BMW i3 50 xDrive · 운전석.', '서로 다른 색상을 조합한 대시보드와 실내 구성.', 'P90657750', 1600, 1098),
    ('i3-rear-seat', 'i3-interior', 'BMW i3 50 xDrive · 뒷좌석.', '밝은 시트와 어두운 천장으로 대비를 준 실내.', 'P90657762', 1600, 1067),
    ('i3-m60-cockpit', 'i3-interior', 'BMW i3 M60 xDrive · 프로토타입.', 'M 스티어링 휠과 화면 구성. 최종 양산 사양과 다를 수 있습니다.', 'P90657927', 1600, 1600),
]


def home_hero():
    return f'''<section class="hero launch-hero" id="hero" aria-labelledby="hero-title">
<picture class="launch-hero-photo"><source media="(max-width: 700px)" srcset="{ASSETS}duo-portrait-800.webp"><img src="{ASSETS}duo-1600.webp" width="1600" height="1067" alt="해외 공개된 신형 BMW 3시리즈와 순수전기 i3" fetchpriority="high" decoding="async"></picture>
<div class="launch-shade" aria-hidden="true"></div><div class="wrap launch-copy"><p class="launch-kicker">백경재 대리의 신차 미리보기 <span>글로벌 공개</span></p><h1 id="hero-title">새로운 3시리즈,<br>먼저 만나보세요.</h1><p class="launch-description">3시리즈와 순수전기 i3의 새로운 모습.<br>외관부터 실내까지, 사진으로 살펴보세요.</p><div class="launch-actions"><a class="button white-button" href="{PREVIEW_PATH}">외관·실내 미리보기 <span aria-hidden="true">↗</span></a><a href="/models/">상담할 BMW 찾기 <span aria-hidden="true">→</span></a></div></div>
<div class="wrap launch-caption"><span>THE NEW 3 SERIES <b>&amp; i3</b></span><p>글로벌 공개 이미지 · 국내 출시 일정·가격·사양은 별도 확인<br>사진 © BMW AG</p></div></section>'''


def model_preview_link():
    return f'<aside class="model-preview-link"><div><span class="editorial-label">해외 신차 소식</span><strong>새로운 3시리즈와 i3가 궁금하신가요?</strong><p>국내 판매 안내와 구분한 외관·실내 사진 미리보기입니다.</p></div><a href="{PREVIEW_PATH}">공개 사진 보기 →</a></aside>'


def preview_body():
    cards = []
    for i, (asset, group, title, caption, photo_id, width, height) in enumerate(PHOTOS):
        cards.append(f'''<figure class="preview-photo" data-photo-group="{group}"><a class="preview-photo-open" href="{ASSETS}{asset}-1600.webp" data-photo-index="{i}" aria-label="{e(title)} 사진 크게 보기"><img src="{ASSETS}{asset}-800.webp" srcset="{ASSETS}{asset}-800.webp 800w, {ASSETS}{asset}-1600.webp {width}w" sizes="(max-width: 760px) calc(100vw - 44px), (max-width: 1200px) 46vw, 560px" width="{width}" height="{height}" alt="{e(title+' '+caption)}" loading="lazy" decoding="async"><span class="photo-expand" aria-hidden="true">크게 보기 ＋</span></a><figcaption><strong>{e(title)}</strong><p>{e(caption)}</p><small>글로벌 공개 이미지 · {photo_id} · © BMW AG</small></figcaption></figure>''')
    return f'''<div class="wrap breadcrumb"><a href="/">홈</a><span>/</span>신형 3시리즈 미리보기</div><article class="new-model-story wrap"><header class="preview-heading"><p class="kicker">백경재 대리의 신차 미리보기</p><h1>새로운 3시리즈.<br><span>다음 BMW가 궁금해지는 순간.</span></h1><p class="lead">바뀐 앞모습부터 운전석과 뒷좌석까지.<br>신형 3시리즈와 순수전기 i3의 글로벌 공개 사진을 모았습니다.</p><p class="source-note">사진 공개 2026.09.30 · 백경재 대리 정리</p></header>
<div class="preview-scope"><strong>먼저 사진으로 만나는 글로벌 공개 모델입니다.</strong><p>국내 출시 일정, 가격과 판매 트림은 별도 확인이 필요합니다. 사진의 색상·옵션·화면 구성은 국내 판매 사양과 다를 수 있습니다.</p></div>
<nav class="preview-filters" aria-label="사진 분류" hidden><button type="button" data-photo-filter="all" aria-pressed="true">전체 <span>10</span></button><button type="button" data-photo-filter="exterior" aria-pressed="false">외관 <span>4</span></button><button type="button" data-photo-filter="3-interior" aria-pressed="false">3시리즈 실내 <span>3</span></button><button type="button" data-photo-filter="i3-interior" aria-pressed="false">i3 실내 <span>3</span></button></nav><p id="photo-result" class="source-note" role="status">사진 10장 · 사진을 누르면 크게 볼 수 있습니다.</p>
<div class="preview-gallery">{''.join(cards)}</div>
<section class="preview-reading"><p class="kicker">사진을 볼 때 함께 확인하세요</p><h2>3시리즈와 i3,<br>구분해서 살펴보세요.</h2><div><p>이 갤러리에는 BMW 320 등 3시리즈의 사진과 전기 세단 i3의 사진이 함께 있습니다. 각 사진에 모델명을 표시했으니, 마음에 드는 실내가 어느 모델의 구성인지 확인해 보세요.</p><p>i3 M60 xDrive 실내는 BMW가 프로토타입으로 공개한 이미지입니다. 사진에 보이는 장비나 디자인이 모든 모델에 동일하게 적용된다는 뜻은 아닙니다.</p><a class="source-link" href="{PRESS_SOURCE}" target="_blank" rel="noopener noreferrer">BMW 공식 공개 사진 확인 ↗<span class="sr-only"> (새 창)</span></a></div></section>
<section class="preview-next"><div><p class="kicker">백경재 대리와 함께</p><h2>지금 살펴볼 BMW도<br>함께 비교해 보세요.</h2><p>구매를 생각하시는 시기와 관심 모델을 알려주세요.<br>현재 안내 가능한 모델부터 차근차근 이야기하겠습니다.</p></div><div class="preview-next-links"><a class="button outline-button" href="/models/3-series/">기존 3시리즈 안내 →</a><a class="button outline-button" href="/models/5-series/">5시리즈 함께 보기 →</a><a class="button kakao-button" href="https://open.kakao.com/o/stXSvxki" target="_blank" rel="noopener noreferrer">백경재 대리에게 문의 ↗<span class="sr-only"> (새 창)</span></a></div></section></article>
<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-dialog-title"><div class="photo-dialog-bar"><p id="photo-dialog-counter"></p><button type="button" id="photo-dialog-close" aria-label="사진 닫기">닫기 ✕</button></div><img id="photo-dialog-image" alt=""><div class="photo-dialog-bottom"><button type="button" id="photo-dialog-prev" aria-label="이전 사진">←</button><div><h2 id="photo-dialog-title"></h2><p id="photo-dialog-caption"></p></div><button type="button" id="photo-dialog-next" aria-label="다음 사진">→</button></div></dialog><script src="/preview-gallery.js" defer></script>'''
