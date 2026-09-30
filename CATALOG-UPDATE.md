# 모델 안내·구매 혜택 수정본

최종 수정 2026-09-30 / 작업 브랜치 `codex/model-catalog-finance`

## 최종 화면

- 담당자 호칭을 **백경재 대리**로 통일했습니다. 상단·하단·소개·검색용 직책 정보의 SC 및 Sales Expert 혼용을 정리했습니다.

- 메인과 `/models/`: **세단 · SUV · 해치백** 세 가지 입구 → 차체별 모델 목록 → 모델 상세.
- 액티브 투어러는 해치백과 다른 **MPV**로 표시하고, 해치백 목록의 비교 모델로 연결했습니다.
- 쿠페·컨버터블·투어링·M은 차체별 관련 모델 또는 `/models/all/`에서 찾아볼 수 있습니다.
- 39개 모델 안내 페이지, 67개 대표 파생 구성, 전면 사선·측면 사진 134개. 520i는 공식 금융 페이지에서 확인한 별도 판매 트림으로 5시리즈 설명에 추가했습니다.
- 모든 페이지의 상단 메뉴·링크·개인 운영 안내를 같은 템플릿으로 통일했습니다. BMW 원형 로고 대신 담당자 사진과 이름을 상단 중심에 배치했습니다.
- 각 차량에 **백경재 대리의 한 줄 코멘트**를 추가했습니다. 상담 말투로 쓴 편집 초안이며, 실제 출고·시승 경험을 주장하는 가공 후기는 넣지 않았습니다. 코멘트는 `data/models.json`의 `advisorComment`에서 수정합니다.
- `/finance/`는 **납입 지원 혜택 안내**입니다. 월 견적, 대출 계산, 상품 선택 기능은 없습니다. 공식 홈페이지의 계산기 코드도 사용하지 않았습니다.
- 확인된 5시리즈·i5 혜택에 적용 기간과 공식 원문을 표시합니다. 금융 예시의 월 납입액에서 지원금을 다시 차감하지 않습니다.
- 좁은 자간을 완화하고 긴 모델명을 의미 단위로 줄바꿈했습니다. 모바일 사진 영역의 과도한 높이를 수정했습니다.

## SEO와 용량

모델 설명은 JavaScript 실행 없이도 읽히는 정적 HTML입니다. 각 페이지에 제목, 설명, canonical, 내부 링크가 있으며 사이트맵은 48개 검색 대상 URL을 포함합니다. 개인정보 안내를 포함한 HTML은 총 49개입니다.

이전 Vercel 주소로 남아 있던 canonical·구조화 데이터·robots·sitemap을 `https://www.bmwgjbaek.com`으로 통일했습니다. 웹폰트 5개 파일 합계를 3,914,876바이트에서 233,500바이트로 약 94.0% 줄였습니다. 이는 파일 용량 측정이며, 배포 후 Lighthouse 성능 점수나 검색 순위 개선을 측정한 결과는 아닙니다.

## 확인한 공식 자료

- 모델과 차량 이미지: <https://www.bmw.co.kr/ko/all-models.html>
- 1시리즈: <https://www.bmw.co.kr/ko/all-models/1-series/bmw-1-series/bmw-1-series.html>
- 액티브 투어러: <https://www.bmw.co.kr/ko/all-models/2-series/2-series-active-tourer/bmw-2-series-active-tourer.html>
- 5시리즈 납입 지원: <https://www.bmw.co.kr/ko/finance/special-offer/financial-promotion/5-series-promotion.html>
- i5 납입 지원: <https://www.bmw.co.kr/ko/finance/special-offer/financial-promotion/special-offer-bmw-i-smart.html>

차량별 원문·이미지 URL과 확인일은 `data/models.json`, 혜택 원문·금액·유효기간은 `data/finance.json`에 기록했습니다. 사진은 BMW 원본 WebP를 사용했고 페이지 구성과 상담 문장은 새로 작성했습니다. 원문의 광고 심의번호를 이 화면의 심의번호처럼 옮기지 않았습니다.

## 수정하고 다시 생성하기

Vercel은 기존처럼 `dist`를 배포합니다. 별도의 운영 서버나 빌드 프레임워크는 필요하지 않습니다.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/build-catalog.py
.venv/bin/python update-seo.py
.venv/bin/python scripts/subset-fonts.py
.venv/bin/python scripts/check-catalog.py
node scripts/check-expiry.cjs
```

- 공통 메뉴·차체별 입구·혜택 화면: `scripts/site_sections.py`
- 모델 설명·코멘트·사진 경로: `data/models.json`
- 구매 혜택: `data/finance.json`
- 모델 상세 템플릿: `scripts/build-catalog.py`
- 화면 스타일: `dist/catalog.css`

혜택이 바뀌면 공식 원문에서 대상·지원금·지원 기간·중복 반영 여부를 확인하고 `data/finance.json`의 혜택과 날짜를 함께 수정합니다. 날짜만 다음 달로 바꾸지 않습니다. 기간이 지나면 브라우저에서 ‘적용 기간 종료’로 표시하며, 자동으로 새 혜택을 수집하지 않습니다. 글을 바꾼 뒤에는 폰트 서브셋도 다시 생성합니다.

## 검증

- 48개 HTML의 내부 링크·이미지 파일·canonical·JSON·제목·H1·사이트맵 확인.
- 모든 페이지 공통 메뉴 일치, 개인 운영 표시, 메인 대표 입구 3개 확인.
- 39개 모델의 코멘트와 혜택 출처·지원 합계 확인.
- 한국 시간 기준 적용 시작일·종료일 자정 경계 테스트 통과.
- 브라우저에서 라인업 → 해치백 → 관련 모델, 파생모델 선택·측면 사진 전환, 모바일 메뉴·사진 높이·구매 혜택 화면 확인.

운영 반영 여부는 GitHub의 최신 커밋과 연결된 Vercel 배포 상태, 실제 도메인의 화면·API 응답으로 확인합니다.


## 2026-09-30 영상 콘텐츠 추가

- 업로드된 12분 15초 분량의 영상에서 확인한 실제 발언을 바탕으로 8개 모델 페이지의 코멘트를 보강했습니다. 축어록이 아니라 뜻을 유지한 편집문이며, 각 페이지에 발언 구간과 정리일을 표시합니다.
- `/guides/bmw-selection/`에 모델 선택 기준 10개, 실제 취향 코멘트 5개, 구매 FAQ 8개, 에디션 소개 2개를 정리했습니다. 홈페이지와 모델 목록·상세에서 연결합니다.
- 15개 모델에 영상 속 색상을 상담 선택지로 제공하고, 39개 모델 페이지에 트림·외장색·실내색·희망 출고 시기를 정리하는 상담 항목과 관련 FAQ를 넣었습니다. X7에는 6·7인승 선택을 추가했습니다.
- 상담 내용은 브라우저에서만 조합됩니다. 저장·자동 전송하지 않으며, 사용자가 복사하거나 문자 앱을 열어 직접 발송합니다. 카카오톡은 내용 복사 후 붙여넣는 방식입니다. 금융 견적 계산 기능은 없습니다.
- 2시리즈 228, 액티브 투어러 220i Luxury/M Sport Design, X5 50e/40d, iX 45를 공식 모델 안내와 2026년 7월 가격표로 확인해 6개 세부 구성을 보강했습니다. 별도 사진이 없는 구성은 다른 트림 사진으로 대체하지 않았습니다.
- i4 BEV 패밀리 에디션과 X2 프로즌 퓨어 그레이 에디션은 공식 출시 자료를 연결합니다. 에디션 상담 링크는 해당 구성과 색상을 미리 선택합니다. i4는 확인한 공식 사진을 사용하고, X2는 해당 에디션 사진을 확보하지 않아 문자 중심 카드로 소개합니다.
- 영상에 없는 할인·금리·지원 금액은 추가하지 않았습니다. 촬영 당시 재고를 현재 재고로 표시하지 않으며, 불명확한 220/228 색상·X1/X3 발언·7시리즈 패키지명·X4 판매 중단 범위는 확정하지 않았습니다.
- 방송 출연 카드와 원본 영상 임베드는 원본 공개 URL·날짜가 확인되지 않아 보류했습니다. 공개 URL 확인 전에는 유튜브 채널 링크로 안내합니다.

데이터는 `data/advisor-guide.json`, 렌더링은 `scripts/advisor_content.py`, 실제 모델 코멘트와 추가 구성은 `data/models.json`에서 관리합니다. `publishingNotes`는 내부 편집 참고용이며 `dist`에 복사하지 않습니다.

공식 에디션 근거:
- [i4 BEV 패밀리 에디션 출시 자료](https://www.press.bmwgroup.com/korea/article/detail/T0459114KO/bmw-코리아-대표-순수전기-라인업으로-구성한-7월-온라인-한정-에디션-3종-출시)
- [X2 프로즌 퓨어 그레이 에디션 출시 자료](https://www.press.bmwgroup.com/korea/article/detail/T0457683KO/bmw-코리아-5월-온라인-한정-에디션-9종-출시)
- i4 사진 원본: https://mediapool.bmwgroup.com/cache/P9/202607/P90649469/P90649469-bmw-july-online-edition-07-2026-1600px.jpg

추가 검증: 48개 페이지의 중복 ID 없음, 빌드 반복 시 FAQ·구조화 데이터 중복 없음, 모바일 색상 선택·가로 넘침, 에디션 자동 선택·사진 방향 전환 시 선택 유지, X7 상담 문구·문자 링크·복사 확인. 기존 유튜브 갱신 테스트 11개와 재생 테스트도 통과했습니다.


## 2026-09-30 신형 3시리즈·i3 사진 미리보기

메인 5시리즈 배너를 신형 3시리즈와 i3의 글로벌 공개 사진으로 변경했습니다. PC는 두 차의 전면 사선 사진, 모바일은 앞·뒷모습이 함께 있는 세로 사진을 사용합니다. 기존 5시리즈 모델·금융 안내와 국내 모델 사진은 유지합니다.

`/stories/new-3-series/`에는 사용자가 제공한 공식 사진 10장을 배치했습니다. 외관 / 3시리즈 실내 / i3 실내 필터, 확대 보기, 이전·다음, 방향키·Escape와 닫기 후 초점 복원을 지원합니다. JavaScript 미사용 시 전체 사진과 이미지 직접 링크를 제공합니다. i3 M60 xDrive 사진은 공식 캡션에 따라 프로토타입으로 표시합니다. 국내 가격·출시일·사전계약 가능 여부는 주장하지 않습니다.

- 템플릿: `scripts/new_model_preview.py`; 갤러리 동작: `dist/preview-gallery.js`
- 사진 이력: `data/new-3-series-photos.json`; 배포 이미지: `dist/assets/new-3-series/`
- 공식 사진: https://www.press.bmwgroup.com/global/photo/compilation/T0460993EN/the-new-bmw-3-series?language=en
- i3 M60 프로토타입 표기: https://www.press.bmwgroup.com/netherlands/photo/detail/P90657927/The-new-BMW-i3-M60-xDrive-09-26

제공 원본은 수정하지 않고 WebP 800/1600px 사본으로 저장했습니다. 원본 10장 합계 약 64.9MB에서 웹용 20개 파일 합계 2,049,786바이트로 줄였습니다. 초기 메인은 화면 폭에 맞는 사진 한 장을 요청하며 상세 사진은 지연 로드합니다. 한 화면에서 모든 고해상도 원본을 읽지 않습니다.

49개 HTML, 48개 사이트맵 URL을 검증했습니다. PC·390px 모바일 배너, 갤러리 필터, 사진 확대, 방향키 전환, Escape 닫기와 초점 복원을 브라우저에서 확인했습니다. 메인 배너 변경에 맞춰 하단 상담 버튼의 관찰 대상을 수정했습니다.
