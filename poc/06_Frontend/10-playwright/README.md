# Playwright E2E 테스트 PoC

> TPS 티켓 관리 시스템을 대상으로 한 Playwright E2E 테스트 실습 프로젝트

## 학습 목표

- Playwright의 핵심 기능 이해 (Auto-wait, Test Isolation, Cross-browser)
- TPS UI 기반 실전 E2E 테스트 작성
- Page Object Model 패턴 적용
- CI/CD 파이프라인 통합

---

## 환경 설정

### 설치

```bash
yarn install
npx playwright install
```

### Mock Server 기동

```bash
yarn mock-server
```

Mock Server는 http://localhost:3002에서 실행됩니다.

### 테스트 실행

```bash
# 전체 테스트
yarn test

# UI 모드 (인터랙티브)
yarn test:ui

# 브라우저 표시 모드
yarn test:headed

# 특정 섹션 테스트
npx playwright test 01-*

# 특정 파일 테스트
npx playwright test 01-setup-first-test/practice/first-test.spec.ts

# 디버그 모드
yarn test:debug
```

### 리포트 확인

```bash
yarn report
```

---

## 3단계 학습 방법

각 섹션은 다음 3단계 학습 흐름을 따릅니다:

1. **INVESTIGATE.md** - 사전 질문으로 탐색
   - 주제에 대한 핵심 질문
   - 스스로 답을 찾아보는 탐구 활동

2. **LEARN.md** - 핵심 개념 학습
   - 개념 설명 및 코드 예시
   - Best Practices 및 안티패턴

3. **practice/** - 실습 코드 작성
   - 직접 테스트 코드 작성
   - 실제 TPS 시나리오 적용

---

## 커리큘럼

| 섹션 | 주제 | 난이도 | 설명 |
|------|------|--------|------|
| 00 | Playwright 개론 | ⭐ | E2E 도구 비교, 아키텍처 |
| 01 | 설치 & 첫 테스트 | ⭐ | 환경 설정, test/expect, Hook |
| 02 | 로케이터 & 동적 콘텐츠 | ⭐⭐ | getBy*, CSS/XPath, 다이얼로그, iframe |
| 03 | 크로스 브라우저 | ⭐⭐ | 멀티 브라우저, 디바이스 에뮬레이션 |
| 04 | Codegen & AI | ⭐⭐ | Codegen 도구, AI 테스트 생성 |
| 05 | 병렬화 & 성능 | ⭐⭐⭐ | Worker, Sharding, Tracing, Performance API |
| 06 | Page Object Model | ⭐⭐⭐ | POM 패턴, TPS 페이지 객체 |
| 07 | TPS 실전 적용 | ⭐⭐⭐⭐ | 캡스톤 - 인증, 워크플로우, CI/CD |

---

## Mock Server

TPS 티켓 관리 UI를 재현한 Express 서버 (포트 3002):

| 페이지 | 경로 | 설명 |
|--------|------|------|
| 로그인 | `/login` | 인증 (admin/admin123) |
| 티켓 목록 | `/tickets` | 검색, 필터, 페이지네이션 |
| CI/CD 등록 | `/tickets/create/cicd` | CICD 티켓 생성 폼 |
| PMS 등록 | `/tickets/create/pms` | PMS 티켓 생성 폼 |
| 티켓 상세 | `/tickets/:no/progress` | 워크플로우 진행 상태 |
| 컴포넌트 | `/components` | 다이얼로그, iframe, Shadow DOM |

### Mock Server 특징

- EJS 템플릿 기반 SSR
- 실제 TPS UI/UX 재현
- 티켓 데이터 JSON 파일 관리 (`mock-server/data/`)
- CORS 설정 완료

---

## 디렉토리 구조

```
10-playwright/
├── README.md                           # 이 파일
├── package.json                        # 의존성 및 스크립트
├── playwright.config.ts                # Playwright 설정
├── tsconfig.json                       # TypeScript 설정
├── .env.example                        # 환경 변수 예시
├── .gitignore                          # Git 제외 파일
│
├── 00-playwright-overview/             # 섹션 0: Playwright 개론
│   ├── INVESTIGATE.md                  # 사전 탐구 질문
│   └── LEARN.md                        # 핵심 개념 학습
│
├── 01-setup-first-test/                # 섹션 1: 설치 & 첫 테스트
│   ├── INVESTIGATE.md
│   ├── LEARN.md
│   └── practice/
│       ├── first-test.spec.ts          # 기본 테스트 작성
│       ├── hooks-demo.spec.ts          # Hook 사용법
│       └── python/                     # Python Playwright 예시
│           └── test_first.py
│
├── 02-locators-dynamic-content/        # 섹션 2: 로케이터 & 동적 콘텐츠
│   ├── INVESTIGATE.md
│   ├── LEARN.md
│   └── practice/
│       ├── locators.spec.ts            # 다양한 로케이터
│       ├── dialog-handling.spec.ts     # 다이얼로그 처리
│       ├── iframe-handling.spec.ts     # iframe 처리
│       └── python/
│           └── test_locators.py
│
├── 03-cross-browser-testing/           # 섹션 3: 크로스 브라우저
│   ├── INVESTIGATE.md
│   ├── LEARN.md
│   └── practice/
│       ├── multi-browser.spec.ts       # 멀티 브라우저 테스트
│       └── device-emulation.spec.ts    # 디바이스 에뮬레이션
│
├── 04-codegen-ai-testing/              # 섹션 4: Codegen & AI
│   ├── INVESTIGATE.md
│   └── practice/
│       ├── codegen-generated.spec.ts   # Codegen으로 생성된 테스트
│       └── ai-enhanced.spec.ts         # AI 개선 테스트
│
├── 05-parallel-performance/            # 섹션 5: 병렬화 & 성능
│   └── practice/
│       ├── parallel-demo.spec.ts       # 병렬 실행 데모
│       ├── performance-api.spec.ts     # Performance API
│       └── tracing-demo.spec.ts        # Tracing & Trace Viewer
│
├── 06-page-object-model/               # 섹션 6: Page Object Model
│   ├── INVESTIGATE.md
│   └── practice/
│       ├── pages/                      # 페이지 객체
│       │   ├── LoginPage.ts
│       │   ├── TicketListPage.ts
│       │   └── TicketCreatePage.ts
│       └── pom-tests.spec.ts           # POM 기반 테스트
│
├── 07-tps-real-world/                  # 섹션 7: TPS 실전 적용
│   └── practice/
│       ├── auth-workflow.spec.ts       # 인증 워크플로우
│       ├── ticket-e2e.spec.ts          # 티켓 전체 시나리오
│       └── python/
│           └── test_tps_e2e.py
│
└── mock-server/                        # Mock Server
    ├── server.js                       # Express 서버
    ├── data/                           # 티켓 JSON 데이터
    │   ├── tickets.json
    │   └── users.json
    └── views/                          # EJS 템플릿
        ├── login.ejs
        ├── tickets.ejs
        ├── ticket-create-cicd.ejs
        ├── ticket-create-pms.ejs
        ├── ticket-progress.ejs
        └── components.ejs
```

---

## 기술 스택

- **Playwright Test** (@playwright/test) - TypeScript
- **Playwright** (playwright) - Python (보조)
- **Express** - Mock Server
- **Node.js 18+**

---

## 주요 명령어

### Codegen (테스트 자동 생성)

```bash
# Mock Server 대상
yarn codegen

# 실제 TPS 환경 (환경변수 필요)
export TPS_BASE_URL=https://tps.okestro.com
yarn codegen:tps
```

### Trace Viewer

```bash
# Trace 파일 확인
npx playwright show-trace test-results/traces/trace.zip
```

### 디버깅

```bash
# UI 모드로 디버깅
yarn test:ui

# Step-by-Step 디버깅
yarn test:debug
```

---

## 학습 가이드

### 초급 (1주차)

1. 섹션 00: Playwright 개론 이해
2. 섹션 01: 첫 테스트 작성
3. 섹션 02: 로케이터 마스터하기

### 중급 (2주차)

4. 섹션 03: 크로스 브라우저 테스트
5. 섹션 04: Codegen 활용
6. 섹션 05: 병렬화 및 성능 최적화

### 고급 (3주차)

7. 섹션 06: Page Object Model 패턴
8. 섹션 07: TPS 실전 E2E 시나리오 작성

---

## 참고 자료

### 공식 문서

- [Playwright 공식 문서](https://playwright.dev)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)

### 커뮤니티

- [Playwright GitHub](https://github.com/microsoft/playwright)
- [Playwright Discord](https://discord.com/invite/playwright-807756831384403968)

### 관련 도구

- [Trace Viewer](https://trace.playwright.dev) - 온라인 Trace 뷰어
- [Playwright Inspector](https://playwright.dev/docs/debug#playwright-inspector) - 내장 디버거

---

## CI/CD 통합 (섹션 7에서 다룸)

### GitHub Actions 예시

```yaml
name: Playwright Tests
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - name: Install dependencies
        run: yarn install
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: yarn test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

## 문제 해결

### Mock Server가 시작되지 않을 때

```bash
# 포트 3002가 사용 중인지 확인
lsof -i :3002

# 프로세스 종료 후 재시작
kill -9 <PID>
yarn mock-server
```

### 브라우저 설치 오류

```bash
# 브라우저 재설치
npx playwright install --force
```

### 테스트 타임아웃

```bash
# 타임아웃 연장
npx playwright test --timeout=60000
```

---

## 라이선스

MIT

---

## 작성자

- **프로젝트**: TPS E2E Testing PoC
- **작성일**: 2026-02-05
- **버전**: 1.0.0

---

## 변경 이력

### v1.0.0 (2026-02-05)
- 초기 프로젝트 구조 생성
- Mock Server 구현
- 섹션 0-7 커리큘럼 완성
- Tracing 데모 추가
