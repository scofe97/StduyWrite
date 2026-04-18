# 05: Test Parallelization & Performance - 면접 정리

## 1. 핵심 개념 상세 설명

### 워커(Worker) 기반 병렬화 모델

```
Playwright 병렬화 구조:
┌─────────────────────────────────────────────────────────────────┐
│                    Test Runner                                  │
│                        │                                        │
│        ┌───────────────┼───────────────┐                        │
│        ▼               ▼               ▼                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │ Worker 1 │    │ Worker 2 │    │ Worker 3 │                   │
│  │(Process) │    │(Process) │    │(Process) │                   │
│  │    │     │    │    │     │    │    │     │                   │
│  │    ▼     │    │    ▼     │    │    ▼     │                   │
│  │ Browser  │    │ Browser  │    │ Browser  │                   │
│  │    │     │    │    │     │    │    │     │                   │
│  │    ▼     │    │    ▼     │    │    ▼     │                   │
│  │ Context1 │    │ Context3 │    │ Context5 │                   │
│  │ Context2 │    │ Context4 │    │ Context6 │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘

격리 수준:
├── Worker: 독립적인 Node.js 프로세스 (완전 격리)
├── Browser: 워커당 하나의 브라우저 인스턴스
├── Context: 테스트별 독립된 BrowserContext (쿠키/세션 격리)
└── Page: Context 내의 브라우저 탭
```

### 워커 설정 방법

```
CLI에서 워커 제어:
┌─────────────────────────────────────────────────────────────────┐
│  npx playwright test                   # 기본: CPU 코어의 절반  │
│  npx playwright test --workers=4       # 4개 워커               │
│  npx playwright test --workers=1       # 순차 실행 (디버깅용)   │
│  npx playwright test --workers=50%     # CPU의 50%              │
└─────────────────────────────────────────────────────────────────┘

playwright.config.ts 설정:
export default defineConfig({
  workers: process.env.CI ? 2 : undefined,  // CI: 2개, 로컬: 자동
  fullyParallel: true,                      // 파일 내 병렬 실행
  retries: process.env.CI ? 2 : 0,          // CI에서 재시도
  maxFailures: process.env.CI ? 10 : undefined,  // 빠른 실패
});
```

### 파일 내 병렬 실행

```typescript
// 병렬 실행 (독립적인 테스트)
test.describe.parallel('Independent Tests', () => {
  test('test 1', async ({ page }) => { /* ... */ });
  test('test 2', async ({ page }) => { /* ... */ });
});

// 순차 실행 (의존성 있는 테스트)
test.describe.serial('Dependent Tests', () => {
  test('step 1: login', async ({ page }) => { /* ... */ });
  test('step 2: checkout', async ({ page }) => { /* ... */ });
});
```

### 샤딩(Sharding)

```
샤딩으로 테스트 분산:
┌─────────────────────────────────────────────────────────────────┐
│  300개 테스트를 3개 머신에서 분산                               │
│                                                                 │
│  Machine 1: npx playwright test --shard=1/3                     │
│  ├── Tests 1-100                                                │
│                                                                 │
│  Machine 2: npx playwright test --shard=2/3                     │
│  ├── Tests 101-200                                              │
│                                                                 │
│  Machine 3: npx playwright test --shard=3/3                     │
│  ├── Tests 201-300                                              │
└─────────────────────────────────────────────────────────────────┘
```

**GitHub Actions 예시:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
```

### Fixture 스코프

```
Fixture 스코프 비교:
┌─────────────────────────────────────────────────────────────────┐
│  scope: 'test' (기본)                                           │
│  ├── 각 테스트마다 생성/정리                                    │
│  └── 테스트 간 완전 격리                                        │
│                                                                 │
│  scope: 'worker'                                                │
│  ├── 워커당 1회 생성, 워커 종료 시 정리                         │
│  └── 비용이 큰 리소스 공유 (브라우저 인스턴스 등)               │
└─────────────────────────────────────────────────────────────────┘

Worker 스코프 Fixture 예시:
const test = base.extend<{}, { workerBrowser: Browser }>({
  workerBrowser: [async ({ playwright }, use) => {
    const browser = await playwright.chromium.launch();
    await use(browser);
    await browser.close();
  }, { scope: 'worker' }],  // 워커당 1회
});
```

### Performance API 활용

```
Navigation Timing API:
┌─────────────────────────────────────────────────────────────────┐
│  startTime ─► domainLookup ─► connect ─► request ─► response   │
│      │            │             │           │          │        │
│      │            │             │           │          │        │
│      │        dnsLookup     tcpConnect    TTFB    download     │
│      │                                                          │
│      └──────────────────── totalLoad ──────────────────────────►│
└─────────────────────────────────────────────────────────────────┘

측정 예시:
const timing = await page.evaluate(() => {
  const perf = performance.getEntriesByType('navigation')[0];
  return {
    ttfb: perf.responseStart - perf.requestStart,
    totalLoad: perf.loadEventEnd - perf.startTime,
  };
});
```

### Core Web Vitals

```
Core Web Vitals:
┌─────────────────────────────────────────────────────────────────┐
│  LCP (Largest Contentful Paint)                                 │
│  ├── 가장 큰 콘텐츠 요소가 렌더링되는 시간                     │
│  └── Good: < 2.5초                                              │
│                                                                 │
│  FID (First Input Delay) → INP (Interaction to Next Paint)     │
│  ├── 사용자 입력에 대한 응답 시간                              │
│  └── Good: < 100ms (FID), < 200ms (INP)                        │
│                                                                 │
│  CLS (Cumulative Layout Shift)                                  │
│  ├── 레이아웃 이동 누적 점수                                   │
│  └── Good: < 0.1                                                │
└─────────────────────────────────────────────────────────────────┘
```

### CDP (Chrome DevTools Protocol)

```
CDP 활용:
┌─────────────────────────────────────────────────────────────────┐
│  const client = await context.newCDPSession(page);              │
│                                                                 │
│  // Performance 도메인 활성화                                   │
│  await client.send('Performance.enable');                       │
│                                                                 │
│  // 메트릭 수집                                                 │
│  const { metrics } = await client.send('Performance.getMetrics');
│                                                                 │
│  수집 가능한 메트릭:                                            │
│  ├── JSHeapUsedSize: 사용 중인 JS 힙 메모리                    │
│  ├── JSHeapTotalSize: 총 JS 힙 메모리                          │
│  ├── Documents: 문서 수                                        │
│  ├── Frames: 프레임 수                                         │
│  ├── LayoutCount: 레이아웃 발생 횟수                           │
│  └── TaskDuration: 작업 소요 시간                              │
└─────────────────────────────────────────────────────────────────┘
```

### Playwright Tracing

```
Tracing 워크플로우:
┌─────────────────────────────────────────────────────────────────┐
│  1. 트레이스 시작                                               │
│     await context.tracing.start({                               │
│       screenshots: true,                                        │
│       snapshots: true,                                          │
│       sources: true,                                            │
│     });                                                         │
│                                                                 │
│  2. 테스트 실행                                                 │
│     await page.goto(...);                                       │
│     await page.click(...);                                      │
│                                                                 │
│  3. 트레이스 저장                                               │
│     await context.tracing.stop({ path: 'trace.zip' });          │
│                                                                 │
│  4. 트레이스 분석                                               │
│     npx playwright show-trace trace.zip                         │
└─────────────────────────────────────────────────────────────────┘

트레이스 내용:
├── Actions Timeline: 액션 타임라인
├── Network Requests: 네트워크 요청
├── Console Logs: 콘솔 로그
├── DOM Snapshots: DOM 스냅샷
├── Screenshots: 스크린샷
└── Source Code: 소스 코드
```

---

## 2. 비교표

### 병렬화 옵션 비교

| 옵션 | 설명 | 사용 시점 |
|------|------|----------|
| `workers` | 워커 수 (프로세스 수) | 항상 설정 |
| `fullyParallel` | 파일 내 테스트도 병렬 | 독립적인 테스트 |
| `test.describe.parallel` | 특정 describe 병렬 | 일부만 병렬 |
| `test.describe.serial` | 순차 실행 강제 | 의존성 있는 테스트 |
| `--shard` | 머신 간 분산 | CI/CD에서 대규모 스위트 |

### Fixture 스코프 비교

| 스코프 | 생성 시점 | 정리 시점 | 용도 |
|--------|----------|----------|------|
| `test` | 각 테스트 전 | 각 테스트 후 | 완전 격리 필요 시 |
| `worker` | 워커 시작 시 | 워커 종료 시 | 비용 큰 리소스 공유 |

### Performance 측정 방법 비교

| 방법 | 측정 대상 | 장점 | 단점 |
|------|----------|------|------|
| Navigation Timing | TTFB, 로드 시간 | 표준 API | 기본 메트릭만 |
| Performance Observer | LCP, CLS | Core Web Vitals | 비동기 처리 필요 |
| CDP | JS 힙, 레이아웃 횟수 | 상세 메트릭 | Chromium만 지원 |

### 아티팩트 저장 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| `screenshot` | `'on'`, `'off'`, `'only-on-failure'` | 스크린샷 저장 시점 |
| `video` | `'on'`, `'off'`, `'on-first-retry'` | 비디오 저장 시점 |
| `trace` | `'on'`, `'off'`, `'on-first-retry'`, `'retain-on-failure'` | 트레이스 저장 시점 |

---

## 3. 면접 예상 질문 및 모범 답안

### Q1. Playwright에서 테스트 격리는 어떻게 보장되나요?

**모범 답안:**

Playwright는 **계층적 격리 모델**을 사용합니다:

```
격리 계층:
├── Worker (Node.js 프로세스): 프로세스 레벨 완전 격리
├── Browser: 워커당 독립된 브라우저 인스턴스
├── BrowserContext: 테스트별 독립된 컨텍스트
│   ├── 쿠키 격리
│   ├── 로컬스토리지 격리
│   └── 세션 격리
└── Page: 컨텍스트 내 브라우저 탭
```

각 테스트는 독립된 BrowserContext를 가지므로:
- 이전 테스트의 쿠키/세션이 영향을 주지 않음
- 테스트 순서에 관계없이 동일한 결과
- 병렬 실행 시에도 경쟁 조건 없음

---

### Q2. fullyParallel과 test.describe.parallel()의 차이는?

**모범 답안:**

| 구분 | fullyParallel | test.describe.parallel() |
|------|--------------|-------------------------|
| **적용 범위** | 전체 프로젝트 | 특정 describe 블록만 |
| **설정 위치** | playwright.config.ts | 테스트 파일 내 |
| **세밀한 제어** | 불가능 | 가능 |

**fullyParallel:**
```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,  // 모든 테스트 병렬 실행
});
```

**test.describe.parallel():**
```typescript
// 이 블록만 병렬
test.describe.parallel('Independent Tests', () => {
  test('test 1', async ({ page }) => { });
  test('test 2', async ({ page }) => { });
});

// 이 블록은 순차
test.describe.serial('Dependent Tests', () => {
  test('step 1', async ({ page }) => { });
  test('step 2', async ({ page }) => { });
});
```

**권장:** 대부분 `fullyParallel: true`로 설정하고, 의존성 있는 테스트만 `serial`로 지정.

---

### Q3. 샤딩과 워커의 차이점과 사용 시나리오는?

**모범 답안:**

| 구분 | 워커 | 샤딩 |
|------|------|------|
| **분산 단위** | 프로세스 (같은 머신) | 머신 (다른 서버) |
| **사용 환경** | 로컬/단일 CI 러너 | 다중 CI 러너 |
| **명령어** | `--workers=4` | `--shard=1/3` |

**사용 시나리오:**

```
워커 (단일 머신 최적화):
├── 로컬 개발 환경
├── 단일 CI 러너
└── CPU 코어 활용

샤딩 (다중 머신 분산):
├── 대규모 테스트 스위트 (300+ 테스트)
├── CI 빌드 시간 단축
└── GitHub Actions matrix 전략
```

**조합 사용:**
```yaml
# 4개 머신에 분산, 각 머신에서 2개 워커
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4 --workers=2
```

---

### Q4. Core Web Vitals(LCP, FID, CLS)가 무엇이고, Playwright로 어떻게 측정하나요?

**모범 답안:**

**Core Web Vitals 정의:**
```
├── LCP (Largest Contentful Paint): 가장 큰 콘텐츠 렌더링 시간
│   └── Good: < 2.5초
├── FID/INP (입력 응답 시간)
│   └── Good: < 200ms
└── CLS (Cumulative Layout Shift): 레이아웃 이동 점수
    └── Good: < 0.1
```

**Playwright 측정 코드:**
```typescript
// LCP 측정
const lcp = await page.evaluate(() => {
  return new Promise<number>((resolve) => {
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      resolve(entries[entries.length - 1].startTime);
    }).observe({ entryTypes: ['largest-contentful-paint'] });
  });
});

// 검증
expect(lcp).toBeLessThan(2500);  // 2.5초 미만
```

**용도:** 성능 회귀 방지, 릴리스 게이트로 활용

---

### Q5. Fixture의 scope 옵션(test, worker)은 언제 사용하나요?

**모범 답안:**

**scope: 'test' (기본):**
```typescript
// 각 테스트마다 생성/정리
authenticatedPage: async ({ page }, use) => {
  await page.goto('/login');
  await page.fill('#email', 'user@example.com');
  // ...
  await use(page);
  await page.goto('/logout');  // 정리
},
```
- 완전한 테스트 격리 필요 시
- 테스트별 상태 초기화 필요 시

**scope: 'worker':**
```typescript
// 워커당 1회 생성
workerBrowser: [async ({ playwright }, use) => {
  const browser = await playwright.chromium.launch();
  await use(browser);
  await browser.close();
}, { scope: 'worker' }],
```
- 비용이 큰 리소스 (브라우저 인스턴스)
- 워커 내 모든 테스트가 공유해도 되는 경우

---

### Q6. 테스트 실행 속도를 최적화하는 방법들은?

**모범 답안:**

**최적화 방법:**
```
1. 병렬화
   ├── workers 수 최적화
   └── fullyParallel: true

2. 네트워크 최적화
   // 불필요한 리소스 차단
   await context.route('**/*.{png,jpg}', route => route.abort());
   await context.route('**/*analytics*', route => route.abort());

3. 아티팩트 최적화
   screenshot: 'only-on-failure',
   video: 'on-first-retry',
   trace: 'on-first-retry',

4. Fixture 스코프 최적화
   // 비용 큰 리소스는 worker 스코프
   { scope: 'worker' }

5. 샤딩 (CI/CD)
   --shard=1/4
```

**주의사항:**
- 워커 수를 무작정 늘리면 리소스 경쟁으로 오히려 느려질 수 있음
- 테스트 간 의존성이 있으면 fullyParallel 사용 불가

---

## 4. 실무 체크리스트

### 병렬화 설정

- [ ] workers 수 최적화 (CI vs 로컬 분기)
- [ ] fullyParallel 활성화 (테스트 독립성 확인 후)
- [ ] 의존성 있는 테스트는 serial로 설정
- [ ] CI에서 샤딩 적용 검토

### 리소스 관리

- [ ] 불필요한 리소스(이미지, 분석) 차단
- [ ] 비용 큰 Fixture는 worker 스코프
- [ ] 아티팩트는 실패 시에만 저장

### 성능 측정

- [ ] Core Web Vitals 측정 테스트 추가
- [ ] 성능 임계치 assertion 설정
- [ ] CI에서 성능 회귀 모니터링

### 디버깅

- [ ] 실패 시 트레이스 저장 설정
- [ ] npx playwright show-trace 활용
- [ ] CDP로 상세 메트릭 수집 (필요 시)

---

## 5. 참고 자료

- [Playwright Test Parallelism](https://playwright.dev/docs/test-parallel)
- [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
- [Playwright Tracing](https://playwright.dev/docs/trace-viewer)
- [Web.dev Core Web Vitals](https://web.dev/vitals/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
