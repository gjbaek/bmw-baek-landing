# GitHub 커밋으로 Vercel 배포하기

현재 대상 주소: https://bmw-baek-landing.vercel.app

기존 저장소에 이 수정본을 덮어 올립니다. `dist` 폴더는 유지하고, 기존 이미지·CSS·JS를 삭제하지 않습니다.

```text
저장소 최상위/
├── vercel.json
├── update-seo.py
├── README.md
├── GITHUB-DEPLOYMENT.md
└── dist/
    ├── index.html
    ├── privacy.html
    ├── robots.txt
    ├── sitemap.xml
    ├── llms.txt
    ├── styles.css        (기존 파일 유지)
    ├── app.js            (기존 파일 유지)
    ├── video-player.js   (기존 파일 유지)
    └── assets/           (기존 파일 유지)
```

1. GitHub에서 기존 저장소의 Vercel 운영 배포 브랜치를 엽니다. 기본 설정이면 `main`입니다.
2. Add file → Upload files에서 수정본 ZIP의 압축을 푼 후, 그 안의 파일들과 `dist` 폴더를 저장소 최상위에 올립니다. ZIP 파일 자체나 ZIP을 감싼 폴더를 올리지 않습니다.
3. 변경 사항을 커밋합니다. Vercel의 GitHub 자동 배포가 연결되어 있으면 이 커밋으로 새 배포가 시작됩니다.

`vercel.json`이 Framework Preset을 Other로, Output Directory를 dist로 지정하며 별도 설치·빌드 명령은 실행하지 않습니다. 현재 확인된 상위 폴더 공개 문제는 Vercel 대시보드 변경 없이 이 설정으로 수정합니다. 정적 파일 폴더만 공개되므로 저장소의 검토 문서와 도구 파일은 사이트 콘텐츠로 제공되지 않습니다.

대표 주소(canonical), 공유 URL과 이미지 주소, 구조화 데이터, robots.txt, sitemap.xml, llms.txt를 위 Vercel 도메인으로 맞췄습니다. 실제 콘텐츠·레이아웃은 변경하지 않았습니다.

배포 완료 후 기본 주소, `/styles.css`, `/privacy.html`, `/robots.txt`, `/sitemap.xml`이 정상 응답하는지 확인합니다. 변경 파일은 로컬에서 검증했으며 아직 GitHub에 커밋하거나 원격 재배포한 것은 아닙니다.

도메인을 나중에 변경하면 `update-seo.py`의 ORIGIN을 바꾸고 `python3 update-seo.py`로 생성된 dist 파일을 함께 커밋하세요.

근거: [Vercel 파일 기반 설정](https://vercel.com/docs/project-configuration/vercel-json), [GitHub 연동 배포](https://vercel.com/docs/git/vercel-for-github).
