# GitHub 커밋으로 Vercel 배포하기

운영 주소: https://www.bmwgjbaek.com / 수정본 확인일: 2026-09-30

기존 저장소의 파일을 유지하면서 수정본을 반영합니다. 이번에는 정적 화면뿐 아니라 YouTube 목록용 Vercel Function도 포함합니다. ZIP 안의 `dist`만 업로드하면 자동 갱신은 동작하지 않습니다.

```text
저장소 최상위/
├── vercel.json
├── api/videos.js
├── lib/youtube-feed.cjs
├── scripts/preview.cjs
├── scripts/render-videos.cjs
├── data/
└── dist/
    ├── index.html
    ├── videos.json
    ├── video-player.js
    ├── styles.css
    ├── models/
    ├── stories/new-3-series/
    ├── guides/bmw-selection/
    ├── finance/
    └── assets/
```

## 영상 자동 갱신과 선택적 API 설정

채널: https://www.youtube.com/@bmw_gjbaek

확인된 채널 ID는 `UCam_yvB4qEmWmAWfT8uy3SQ`, 업로드 재생목록은 `UUam_yvB4qEmWmAWfT8uy3SQ`입니다. 사용자 제공 영상 3편의 채널 정보를 확인했습니다.

API 키가 없으면 YouTube 공식 공개 피드를 사용합니다. 9월 30일 공개 피드가 200과 404를 번갈아 반환했지만, 최종 브라우저 검증에서 9월 29일 신규 영상을 자동으로 가져오는 데 성공했습니다. 키 없이도 동작하며, 피드 연결이 불안정할 때 공식 API를 선택적으로 연결할 수 있습니다. 실패 상태를 동기화 성공으로 간주하지 않습니다. 최근 공개 영상은 최대 12편을 보여 주며 Shorts도 포함될 수 있습니다.

1. 소유자의 Google Cloud 프로젝트에서 **YouTube Data API v3**를 활성화하고 API 키를 준비합니다. API 제한은 YouTube Data API v3로 지정합니다.
2. Vercel 프로젝트의 **Settings → Environment Variables**에 `YOUTUBE_API_KEY`를 등록합니다. Production과 필요한 Preview 환경에 적용합니다. 서버에서 호출하므로 브라우저 HTTP referrer 제한 방식은 사용하지 않습니다.
3. `api/`, `lib/`, `dist/`, `vercel.json`을 포함한 수정본을 연결된 운영 브랜치에 반영하고 배포합니다. Vercel의 Root Directory는 이 파일들이 있는 저장소 최상위여야 합니다. API 키를 새로 등록했다면 새 배포가 필요합니다.
4. 배포된 `/api/videos`에서 `status: "live"`, `source: "youtube-api"` 또는 `"youtube-feed"`와 실제 게시일 순의 영상 목록을 확인합니다. `fallback`은 저장된 목록을 반환한 것이며 자동 동기화 성공이 아닙니다.
5. 홈페이지에서 영상 선택·이전·다음·원본 보기 링크를 확인합니다. 키 값을 응답이나 소스 코드에 넣지 않습니다.

설치할 npm 패키지는 없으며 `installCommand`와 `buildCommand`는 기존처럼 빈 문자열입니다. Output Directory는 `dist`, 함수는 저장소 최상위의 `/api`에서 Vercel이 감지합니다. Node.js 20 이상을 사용합니다.

자동 갱신은 방문 요청을 기준으로 실행하며 별도의 Cron이나 GitHub Actions가 필요 없습니다. 정상 목록의 CDN 캐시는 10분, 실패 응답은 캐시하지 않습니다. YouTube 갱신 지연·방문 시점·백그라운드 갱신에 따라 실제 반영 시간은 달라집니다. 재생 중인 목록은 다음 페이지 방문 때 새 목록으로 바뀝니다.

## 검증

```sh
node --test qa/youtube-feed.test.cjs qa/video-refresh.test.cjs
node qa/video-player.test.cjs
node scripts/preview.cjs
```

로컬 주소: http://127.0.0.1:4173/#videos

원격 배포 후 `/`, `/stories/new-3-series/`, `/guides/bmw-selection/`, `/models/x7/`, `/models/i4/?edition=i4#consultation`, `/finance/`, `/api/videos`, `/robots.txt`, `/sitemap.xml`을 확인합니다. canonical과 sitemap은 `https://www.bmwgjbaek.com`을 가리켜야 합니다. 예전 Vercel 도메인의 리디렉션은 Vercel 도메인 설정에서 별도로 확인합니다.

GitHub의 최신 커밋에 연결된 Vercel 배포가 성공했는지 확인합니다. 운영 API 키는 저장소에 포함하지 않습니다. 실제 API 키를 이용한 성공 응답은 키 등록 후 위 4번에서 확인합니다.

공식 참고: [Vercel Node.js Functions](https://vercel.com/docs/functions/runtimes/node-js), [CDN 캐시](https://vercel.com/docs/caching/cache-control-headers), [YouTube 업로드 목록 API](https://developers.google.com/youtube/v3/docs/playlistItems/list), [YouTube 공개 피드](https://developers.google.com/youtube/v3/guides/push_notifications).
