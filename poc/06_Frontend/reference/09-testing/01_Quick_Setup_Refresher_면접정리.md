# 01: Quick Setup Refresher - 면접 정리

## 1. 핵심 개념 상세 설명

### Playwright Test vs Playwright Library

```
Playwright 제품 구조:
┌─────────────────────────────────────────────────────────────────┐
│                     Playwright Test                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              내장 테스트 러너                                ││
│  │  ├── 병렬 실행                                              ││
│  │  ├── 리포터 (HTML, JSON)                                    ││
│  │  ├── 재시도/타임아웃                                        ││
│  │  └── Fixture 시스템                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Playwright Library                              ││
│  │  ├── 브라우저 자동화 API                                    ││
│  │  ├── 페이지 조작                                            ││
│  │  └── 네트워크 인터셉트                                      ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

설치 명령어:
├── Playwright Test:    npm install --save-dev @playwright/test
└── Playwright Library: npm install playwright
```

**비유**: Playwright Library는 '자동차 엔진'만 제공하고, Playwright Test는 '완성된 자동차'를 제공

### 프로젝트 구조와 설정

```
권장 프로젝트 구조:
my-playwright-project/
├── tests/                    # 테스트 파일
│   ├── example.spec.ts
│   ├── logged-in/            # 로그인 필요 테스트
│   │   ├── api.spec.ts
│   │   └── login.setup.ts
│   └── logged-out/           # 비로그인 테스트
│       └── auth.spec.ts
├── src/
│   ├── pages/                # Page Object Model
│   │   ├── BasePage.ts
│   │   └── DashboardPage.ts
│   └── utils/                # 유틸리티 함수
│       └── apiHelper.ts
├── fixtures/                 # 테스트 데이터
│   └── testData.json
├── test-results/             # 실행 결과
├── playwright-report/        # HTML 리포트
├── playwright.config.ts      # 설정 파일
└── package.json
```

### Hook 생명주기

```
테스트 실행 순서:
┌─────────────────────────────────────────────────────────────────┐
│  test.beforeAll()  ─────────────────────────────────────────────│
│       │                                                         │
│       ▼                                                         │
│  test.beforeEach() ── Test 1 ── test.afterEach()               │
│       │                                                         │
│       ▼                                                         │
│  test.beforeEach() ── Test 2 ── test.afterEach()               │
│       │                                                         │
│       ▼                                                         │
│  test.beforeEach() ── Test 3 ── test.afterEach()               │
│       │                                                         │
│       ▼                                                         │
│  test.afterAll()  ──────────────────────────────────────────────│
└─────────────────────────────────────────────────────────────────┘

Hook 용도:
├── beforeAll  : 파일 내 모든 테스트 전 1회 (DB 연결, 비용 큰 초기화)
├── beforeEach : 각 테스트 전 (페이지 이동, 상태 초기화)
├── afterEach  : 각 테스트 후 (리소스 정리, 로그 기록)
└── afterAll   : 파일 내 모든 테스트 후 1회 (최종 정리)
```

### Fixture 시스템

```
내장 Fixture:
┌─────────────┬─────────────────┬────────────────────────────────┐
│  Fixture    │  타입           │  용도                          │
├─────────────┼─────────────────┼────────────────────────────────┤
│  page       │  Page           │  브라우저 탭 (테스트별 격리)   │
│  context    │  BrowserContext │  브라우저 세션 (쿠키, 스토리지)│
│  browser    │  Browser        │  브라우저 인스턴스 (워커 공유) │
│  browserName│  string         │  현재 브라우저 이름            │
│  request    │  APIRequestCtx  │  API 요청 (HTTP 테스트용)      │
└─────────────┴─────────────────┴────────────────────────────────┘

테스트 격리 모델:
┌────────────────────────────────────────────────────────────────┐
│  Browser (워커 간 공유)                                        │
│  ├── Worker 1                                                  │
│  │   ├── Context 1 (Test A) ── 독립된 쿠키/세션/스토리지       │
│  │   └── Context 2 (Test B) ── 독립된 쿠키/세션/스토리지       │
│  └── Worker 2                                                  │
│      ├── Context 3 (Test C)                                    │
│      └── Context 4 (Test D)                                    │
└────────────────────────────────────────────────────────────────┘
```

### 주요 설정 옵션

```
playwright.config.ts 구조:
┌─────────────────────────────────────────────────────────────────┐
│  defineConfig({                                                  │
│    testDir: './tests',           // 테스트 디렉토리             │
│    timeout: 30000,               // 테스트 타임아웃 (30초)      │
│    workers: 4,                   // 병렬 워커 수                │
│    fullyParallel: true,          // 파일 내 병렬 실행           │
│    retries: 2,                   // 실패 시 재시도              │
│                                                                 │
│    use: {                        // 브라우저 설정               │
│      browserName: 'chromium',                                   │
│      headless: true,                                            │
│      viewport: { width: 1280, height: 720 },                    │
│    },                                                           │
│                                                                 │
│    projects: [                   // 멀티 브라우저               │
│      { name: 'Chromium', use: { browserName: 'chromium' } },    │
│      { name: 'Firefox', use: { browserName: 'firefox' } },      │
│      { name: 'Mobile', use: { device: 'iPhone 16' } },          │
│    ],                                                           │
│  })                                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 비교표

### Playwright Test vs Library 비교

| 구분 | Playwright Test | Playwright Library |
|------|-----------------|-------------------|
| **설치** | `@playwright/test` | `playwright` |
| **용도** | E2E 테스트 프레임워크 | 브라우저 자동화 API |
| **테스트 러너** | 내장 | Jest, Mocha 등 별도 필요 |
| **병렬 실행** | 기본 지원 | 직접 구현 |
| **리포트** | HTML, JSON 내장 | 직접 구현 |
| **권장 상황** | 신규 E2E 테스트 | 기존 Jest 환경 통합 |

### Hook 비교

| Hook | 실행 시점 | 실행 횟수 | 주요 용도 |
|------|----------|----------|----------|
| `beforeAll` | 파일 내 모든 테스트 전 | 1회 | DB 연결, 비용 큰 초기화 |
| `beforeEach` | 각 테스트 전 | 테스트 수만큼 | 페이지 이동, 상태 초기화 |
| `afterEach` | 각 테스트 후 | 테스트 수만큼 | 리소스 정리, 로그 기록 |
| `afterAll` | 파일 내 모든 테스트 후 | 1회 | 최종 정리 |

### 실행 모드 비교

| 명령어 | 설명 | 사용 시점 |
|--------|------|----------|
| `npx playwright test` | Headless 실행 | CI/CD, 일반 실행 |
| `--headed` | 브라우저 UI 표시 | 시각적 확인 필요 시 |
| `--debug` | Inspector 디버깅 | 문제 해결 |
| `--project=chromium` | 특정 브라우저만 | 브라우저별 테스트 |

### Fixture 비교

| Fixture | 스코프 | 격리 수준 | 용도 |
|---------|--------|----------|------|
| `page` | 테스트 | 테스트별 독립 | 일반 테스트 |
| `context` | 테스트 | 세션별 독립 | 쿠키/스토리지 접근 |
| `browser` | 워커 | 워커 간 공유 | 브라우저 옵션 변경 |
| `request` | 테스트 | API 요청용 | HTTP 테스트 |

---

## 3. 면접 예상 질문 및 모범 답안

### Q1. Playwright Test와 Playwright Library의 차이점은 무엇인가요?

**모범 답안:**

```
핵심 차이:
├── Playwright Test: 완성된 테스트 프레임워크 (테스트 러너 포함)
└── Playwright Library: 브라우저 자동화 API만 제공
```

**Playwright Test**는 내장 테스트 러너, 병렬 실행, HTML/JSON 리포터, Fixture 시스템을 포함한 올인원 E2E 테스트 솔루션입니다.

**Playwright Library**는 브라우저 자동화 API만 제공하며, Jest나 Mocha 같은 별도 테스트 러너가 필요합니다.

**선택 기준:**
- 신규 E2E 테스트 프로젝트 → Playwright Test (권장)
- 기존 Jest 환경에 통합 → Playwright Library
- 테스트 외 브라우저 자동화(스크래핑 등) → Playwright Library

---

### Q2. beforeEach와 beforeAll의 차이점과 사용 시나리오를 설명해주세요.

**모범 답안:**

**실행 빈도 차이:**
```
파일에 테스트 3개가 있을 때:
├── beforeAll  : 1회 실행
├── beforeEach : 3회 실행 (테스트마다)
├── afterEach  : 3회 실행 (테스트마다)
└── afterAll   : 1회 실행
```

**사용 시나리오:**

| Hook | 시나리오 | 예시 |
|------|---------|------|
| `beforeAll` | 비용이 큰 일회성 초기화 | DB 연결, 테스트 데이터 생성 |
| `beforeEach` | 테스트별 상태 초기화 | 로그인, 페이지 이동 |

**실전 예시 (로그인 필요 테스트):**
```typescript
test.beforeEach(async ({ page }) => {
  await page.goto('https://example.com/');
  await page.getByPlaceholder('Username').fill('user');
  await page.getByPlaceholder('Password').fill('pass');
  await page.getByRole('button', { name: 'Login' }).click();
});
```

각 테스트가 로그인된 상태로 시작하므로, 테스트 간 독립성이 보장됩니다.

---

### Q3. Playwright의 테스트 격리(Test Isolation)가 왜 중요하고, 어떻게 구현되나요?

**모범 답안:**

**중요성:**
```
테스트 격리가 없으면:
├── 테스트 순서에 따라 결과가 달라짐
├── 이전 테스트의 쿠키/세션이 다음 테스트에 영향
└── 병렬 실행 불가능 (경쟁 조건 발생)
```

**Playwright의 격리 구현:**
```
각 테스트는 독립된 BrowserContext를 가짐:
├── 쿠키 : 공유 안 됨
├── 세션 스토리지 : 공유 안 됨
├── 로컬 스토리지 : 공유 안 됨
└── 인증 상태 : 공유 안 됨
```

이로 인해 테스트가 어떤 순서로 실행되든, 병렬로 실행되든 동일한 결과를 보장합니다.

---

### Q4. Fixture란 무엇이고, 어떤 내장 Fixture가 있나요?

**모범 답안:**

**Fixture 정의:**
Fixture는 테스트에 필요한 리소스를 자동으로 생성하고 정리하는 메커니즘입니다.

**내장 Fixture:**
| Fixture | 용도 |
|---------|------|
| `page` | 브라우저 탭 (테스트별 격리) |
| `context` | 브라우저 세션 (쿠키/스토리지 접근) |
| `browser` | 브라우저 인스턴스 |
| `browserName` | 현재 브라우저 이름 (`chromium`, `firefox`, `webkit`) |
| `request` | API 요청 (HTTP 테스트용) |

**사용 예시:**
```typescript
test('API 테스트', async ({ request }) => {
  const response = await request.get('https://api.github.com');
  expect(response.status()).toBe(200);
});
```

Fixture는 `test.extend()`로 커스텀 확장 가능합니다.

---

### Q5. playwright.config.ts에서 가장 중요한 설정 옵션들을 설명해주세요.

**모범 답안:**

**주요 설정 카테고리:**

```
1. 파일 매칭
├── testDir: 테스트 디렉토리 경로
├── testMatch: 테스트 파일 패턴 (*.spec.ts)
└── testIgnore: 제외 패턴

2. 타임아웃
├── timeout: 개별 테스트 타임아웃 (기본 30초)
├── globalTimeout: 전체 스위트 타임아웃
└── actionTimeout: 개별 액션 타임아웃

3. 병렬화
├── workers: 워커 수 (숫자 또는 비율)
└── fullyParallel: 파일 내 테스트도 병렬 실행

4. 재시도
├── retries: 실패 시 재시도 횟수
└── maxFailures: 최대 실패 허용 수

5. 브라우저
├── browserName: 기본 브라우저
├── headless: Headless 모드
└── viewport: 뷰포트 크기
```

**CI 환경 예시:**
```typescript
export default defineConfig({
  workers: process.env.CI ? 2 : undefined,
  retries: process.env.CI ? 2 : 0,
  headless: true,
});
```

---

### Q6. Playwright 설치 시 `npm init playwright@latest`와 `npm install @playwright/test`의 차이점은?

**모범 답안:**

**비교:**
| 방법 | 결과 |
|------|------|
| `npm install @playwright/test` | 패키지만 설치, 설정 직접 구성 필요 |
| `npm init playwright@latest` | 설정 파일 + 예제 테스트 + 브라우저 자동 설치 |

**`npm init playwright@latest` 실행 시 생성되는 파일:**
```
├── playwright.config.ts  # 기본 설정
├── tests/example.spec.ts # 예제 테스트
└── 브라우저 바이너리 (선택 시)
```

**권장:**
- 신규 프로젝트: `npm init playwright@latest` (빠른 시작)
- 기존 프로젝트: `npm install @playwright/test` + 수동 설정

**주의:** `npm install @playwright/test`만 하면 브라우저 바이너리가 설치되지 않습니다. `npx playwright install` 별도 실행 필요.

---

## 4. 실무 체크리스트

### 프로젝트 초기 설정

- [ ] `npm init playwright@latest`로 프로젝트 초기화
- [ ] `playwright.config.ts` 기본 설정 확인
- [ ] 테스트 디렉토리 구조 설계 (logged-in, logged-out 분리)
- [ ] VS Code Playwright 확장 프로그램 설치

### playwright.config.ts 설정

- [ ] testDir 경로 확인
- [ ] timeout 적절히 설정 (네트워크 환경 고려)
- [ ] workers 수 설정 (CI vs 로컬 분기)
- [ ] retries 설정 (CI에서 flaky 테스트 대응)
- [ ] projects로 멀티 브라우저 설정

### 테스트 작성

- [ ] Hook(beforeEach)으로 공통 로직 분리
- [ ] Fixture 적절히 활용
- [ ] 테스트 간 독립성 유지
- [ ] 명시적 assertion 포함

### CI/CD 통합

- [ ] headless: true 설정 확인
- [ ] HTML 리포터 설정
- [ ] 아티팩트(스크린샷, 비디오) 저장 설정

---

## 5. 참고 자료

- [Playwright 공식 문서 - Getting Started](https://playwright.dev/docs/intro)
- [Playwright Configuration](https://playwright.dev/docs/test-configuration)
- [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
- [Playwright GitHub](https://github.com/microsoft/playwright)
