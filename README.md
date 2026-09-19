# BMW 백경재 대리 랜딩페이지

모바일 상담 중심의 정적 웹사이트입니다. 서버와 데이터베이스 없이 `dist` 폴더를 호스팅하면 동작합니다.

## 파일

- `dist/index.html`: 모든 본문, 메뉴, 전화·문자·카카오톡·지도·SNS 링크, 영상 목록
- `dist/styles.css`: Pretendard 웹폰트와 반응형 스타일
- `dist/app.js`: 동일 크기의 차종 카드 4개와 24개 모델 선택, 상담창, 문자 문구, 하단 상담 버튼, 주소 복사
- `dist/video-player.js`: 클릭 시 로드하는 YouTube 플레이어, 영상 선택, 이전·다음 및 순차 재생
- `dist/videos.json`: 큐레이션한 6편의 영상 ID·제목·원제·썸네일 자료
- `dist/privacy.html`: 개인정보·외부 서비스 이용 안내
- `dist/assets`: 최적화한 실제 BMW 사진, 제공된 프로필과 로고
- `update-seo.py`: 본문의 FAQ를 읽어 구조화 데이터와 검색 파일을 갱신
- `vercel.json`: Vercel에서 `dist`만 공개하고 설치·빌드를 생략하는 배포 설정
- `GITHUB-DEPLOYMENT.md`: GitHub 파일 변경만으로 기존 Vercel 배포를 수정하는 방법
- `audit-seo.py`: 25개 항목의 로컬 구현 검사 (공식 SEO 점수 아님)
- `REVIEW.md`: 디자인·문구·SEO·법적 표시 검토 결과와 남은 공개 검증 항목

## 실제 연결

- 딜러: 010-8308-9819
- 전시장: 02-749-7301
- 이메일: gyungjae.baek@deutschmotors.com
- 주소: 서울특별시 용산구 이태원로 249
- 유튜브: https://www.youtube.com/@bmw_gjbaek (제공된 명함 QR의 리디렉션으로 확인)
- 카카오톡 상담: https://open.kakao.com/o/stXSvxki
- 네이버 블로그: https://blog.naver.com/back03278
- 인스타그램: https://www.instagram.com/bmw_gjbaek/

전화와 문자 링크는 기기의 기본 앱으로 연결합니다. 이 사이트 자체에서는 상담 내용을 저장하거나 전송하지 않습니다. 앱 실행 및 실제 통화·문자 발송은 방문자가 진행합니다. 카카오톡과 SNS는 제공된 주소로 새 창에서 연결됩니다. 자체 분석·광고 스크립트는 추가하지 않았습니다. 영상 썸네일은 YouTube에서 로드하며, 재생 또는 목록 선택 시 YouTube API와 `youtube-nocookie.com` 임베드를 불러옵니다. 영상 재생에는 YouTube의 서비스와 정책이 적용됩니다.

## 디자인과 영상

흰색 상단 바와 개인 이름 중심의 표기를 적용했습니다. 큰 차량 배너와 어두운 인물 소개 영역은 유지합니다. Pretendard 본문 400·500, 소제목·버튼 600, 핵심 제목 800으로 강약을 구분합니다.

상단의 백경재와 SC는 크기·색상·굵기가 같습니다. 주요 제목·본문·보조 문구의 크기를 통일하고, 대표 차량 카드의 높이와 버튼 위치를 맞췄습니다. 차종 카드 4개 중 하나를 누르면 아래 공통 영역에 해당 모델만 펼쳐집니다. FAQ 제목은 두 줄이며, 첫 질문은 모바일 두 줄·PC 한 줄로 표시됩니다.

영상 목록은 채널의 자동차 관련 영상 6편을 사이트에 구성한 목록입니다. YouTube 계정의 재생목록을 만들거나 변경한 것은 아닙니다. 방문자가 재생을 시작하면 현재 영상 종료 후 다음 영상으로 이동하며 마지막 영상에서 멈춥니다. 재생 실패 시 다시 시도하거나 YouTube 원본 링크로 이동할 수 있습니다. 브라우저의 자동 재생 제한이 적용되면 플레이어 내부 재생 버튼을 누르면 됩니다.

재생 버튼 또는 영상 목록을 누르면 페이지 안에서 바로 재생합니다. 별도 동의 팝업은 없습니다. 외부 서비스 안내는 플레이어 아래와 푸터에 연결했습니다.

영상 교체 시 `dist/index.html`의 `.playlist-item`에 있는 `data-video-id`, 제목·분류·썸네일·길이를 수정하고 첫 영상의 포스터와 제목, 원본 링크도 맞춰주세요. `dist/videos.json`에도 같은 자료를 보관합니다. 실제 재생은 HTML 목록을 읽으므로 API 키나 서버가 필요 없습니다.

## 콘텐츠를 추가할 때

1. 승인된 실제 출고 사례와 사진: 모델, 선택 이유, 상담 과정, 작성일. 고객 정보는 공개 동의 범위에 맞게 작성.
2. 현재 유효한 프로모션: 적용 모델, 기간, 조건, 포함·제외 항목, 갱신일과 담당자 확인.
3. 실제 비교 안내: 예산, 차체, 주행 환경, 충전 여건을 기준으로 BMW 5시리즈·X3·i5를 비교.
4. 전시장 방문 안내: 확인된 영업시간, 주차, 대중교통, 시승 예약 조건.
5. 영상 큐레이션: 모델 리뷰·출고 사례·딜러 일상 중심으로 갱신하고 지난 프로모션 조건을 현재 혜택으로 오해하지 않도록 설명.

검증되지 않은 할인액·재고·납기·수상·후기·순위는 넣지 않았습니다.

## SEO / AI 검색 준비

주요 내용은 JavaScript 실행 없이 HTML로 제공됩니다. `lang=ko`, 고유 제목·설명, canonical, Open Graph 제목·설명, 의미 있는 제목 구조, 이미지 대체 텍스트, Person·AutoDealer·WebSite·WebPage·FAQPage JSON-LD, robots.txt, sitemap.xml을 포함했습니다. JSON-LD의 FAQ는 보이는 본문과 동일합니다. `llms.txt`는 정보 확인을 돕는 보조 파일이며 검색 순위나 AI 인용을 보장하는 표준은 아닙니다.

공유 이미지와 Twitter 카드 정보도 포함합니다. 자체 25개 구현 항목은 수정 전 84/100에서 100/100으로 개선됐습니다. Lighthouse나 실제 공개 사이트 SEO 점수는 측정하지 않았습니다. 검사 범위·근거·공개 전 필요한 작업은 `REVIEW.md`에 명시했습니다.

현재 대표 도메인은 `https://bmw-baek-landing.vercel.app`으로 맞췄습니다. 도메인을 변경하면 `update-seo.py`의 ORIGIN을 바꾼 뒤 `python3 update-seo.py`를 실행하세요. 비공개 또는 인증이 필요한 사이트는 검색엔진이 정상 수집할 수 없습니다. 공개 후 소유자 계정으로 Google Search Console과 네이버 서치어드바이저의 사이트 소유권 인증 및 사이트맵 제출이 필요합니다. 인증 토큰은 제공되지 않아 임의로 추가하지 않았습니다.

상위 노출은 경쟁도, 사이트 신뢰, 콘텐츠 품질과 축적, 운영 이력, 검색 플랫폼의 정책 등 영향을 받으므로 보장할 수 없습니다. FAQ 구조화 데이터가 검색결과의 FAQ 확장 표시를 보장하지도 않습니다.

공식 참고:
- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/appearance/ai-features
- https://searchadvisor.naver.com/guide

## 이미지 출처

프로필과 BMW 로고는 사용자가 제공했습니다. 원본 파일은 수정하지 않았습니다. 제공된 포스터와 채널 로고는 콘텐츠 확장용으로 남겨두고, 현재 페이지에는 원본 프로필과 BMW 로고를 사용합니다.

- 5시리즈: https://www.bmw.co.kr/ko/all-models/5-series/sedan/bmw-5-series-sedan-overview.html
- X3: https://www.bmw.co.kr/ko/all-models/x-series/x3/bmw-x3.html
- i5: https://www.bmw.co.kr/ko/all-models/bmw-i/i5/bmw-i5-overview.html

차량 사진: © BMW AG. 실제 판매 사양과 다를 수 있습니다. 사용자가 BMW 로고·공식 차량 사진에 대한 사용 허락 또는 가이드가 있음을 확인했습니다. 해당 확인을 전제로 유지했으며, 허락 문서의 세부 범위 자체는 제공되지 않았습니다.

## 로컬 미리보기

프로젝트 폴더에서 `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`를 실행하고 http://127.0.0.1:4173/ 를 엽니다.

## Vercel 배포

저장소 최상위의 `vercel.json`이 배포 폴더를 `dist`로 지정합니다. Vercel과 연결된 운영 배포 브랜치에 커밋하면 자동 배포가 시작됩니다. 기존 이미지·CSS·JS는 유지하며, 별도 빌드 명령이나 패키지 설치가 필요하지 않습니다. 적용 순서는 `GITHUB-DEPLOYMENT.md`를 참고하세요.

## 이전 Sites 연결 기록

기존 Site ID는 `.openai/hosting.json`에 보존되어 있습니다. 게시를 재개할 때 새 Site를 만들지 말고 이 ID를 재사용하세요. 기본 비공개 범위를 공개로 바꾸려면 별도 공개 요청이 필요합니다.

상담 절차 제목은 모바일에서 “어떻게 / 시작하나요?” 두 줄, PC에서 “어떻게 시작하나요?” 한 줄로 표시합니다.
