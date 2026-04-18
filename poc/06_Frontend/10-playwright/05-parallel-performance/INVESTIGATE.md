# 05. 병렬 실행과 성능 측정 - 조사 (INVESTIGATE)

**작성일**: 2026-02-05
**목표**: Playwright의 병렬 실행 메커니즘과 성능 측정 방법 이해
**학습 유형**: 소크라테스식 질문 → 탐구 → 이해

---

## 핵심 질문 (7개)

### 1. Playwright는 어떻게 병렬 실행을 달성하는가? (Worker 모델)

**탐구 목표**: Worker 프로세스의 동작 원리와 테스트 분배 메커니즘을 이해합니다.

**질문 세부사항**:
- Worker는 OS 레벨 프로세스인가 스레드인가?
- 각 Worker는 독립적인 브라우저 인스턴스를 가지나?
- Worker 간 데이터 공유는 어떻게 이루어지나?
- Worker 개수는 어떻게 결정되나?

**탐구 활동**:
```typescript
// 활동 1: Worker 정보 확인
test('Worker 정보 출력', async ({ page }, testInfo) => {
  console.log('Worker Index:', testInfo.workerIndex);
  console.log('Parallel Index:', testInfo.parallelIndex);
  console.log('Project Name:', testInfo.project.name);

  // 질문: workerIndex와 parallelIndex의 차이는?
  // workerIndex: 0, 1, 2... (재사용되는 Worker 식별)
  // parallelIndex: 각 테스트의 고유 병렬 실행 순서
});
```

**실험 과제**:
```bash
# 1 Worker로 실행 (순차)
npx playwright test --workers=1

# 4 Worker로 실행 (병렬)
npx playwright test --workers=4

# CPU 코어 수만큼 (기본값)
npx playwright test --workers=100%

# 질문: 실행 시간이 어떻게 달라지나?
# 예상: 4 Worker 시 약 4배 빠름 (오버헤드 제외)
```

**Worker 모델 이해**:
```
Master Process (테스트 러너)
├─ Worker 1 (Process)
│  └─ Browser Context 1
│     ├─ test1.spec.ts
│     └─ test2.spec.ts
├─ Worker 2 (Process)
│  └─ Browser Context 2
│     ├─ test3.spec.ts
│     └─ test4.spec.ts
└─ Worker 3 (Process)
   └─ Browser Context 3
      └─ test5.spec.ts
```

**핵심 질문**:
- 각 Worker는 완전히 격리되어 있나?
- Worker 간 테스트 순서는 보장되나?
- Worker 재시작 조건은?

---

### 2. Worker와 Browser Context의 관계는? 각 테스트는 독립적인가?

**탐구 목표**: 테스트 격리(isolation) 메커니즘을 이해합니다.

**질문 세부사항**:
- 각 테스트는 새로운 BrowserContext를 생성하나?
- Cookie, LocalStorage는 테스트 간 공유되나?
- Page는 재사용되나 매번 생성되나?
- 테스트 간 상태 오염(pollution)을 어떻게 방지하나?

**탐구 활동**:
```typescript
// 활동 2: Context 격리 확인
test.describe('Context 격리 테스트', () => {
  test('Test 1 - localStorage 설정', async ({ page }) => {
    await page.goto('http://localhost:3002');
    await page.evaluate(() => {
      localStorage.setItem('test-key', 'value-from-test1');
    });

    const value = await page.evaluate(() => localStorage.getItem('test-key'));
    console.log('Test 1 - localStorage:', value);
    expect(value).toBe('value-from-test1');
  });

  test('Test 2 - localStorage 확인', async ({ page }) => {
    await page.goto('http://localhost:3002');
    const value = await page.evaluate(() => localStorage.getItem('test-key'));
    console.log('Test 2 - localStorage:', value);

    // 질문: Test 1의 localStorage가 남아있나?
    // 답: null (새로운 BrowserContext 생성)
    expect(value).toBeNull();
  });
});
```

**Browser Context 구조**:
```typescript
// Playwright의 내부 동작 (의사 코드)
class Worker {
  async runTest(testFile: string) {
    const browser = await chromium.launch(); // Worker당 1개

    for (const test of tests) {
      const context = await browser.newContext(); // 테스트당 1개 (격리)
      const page = await context.newPage();

      await test.run(page);

      await context.close(); // 테스트 종료 시 Context 정리
    }

    await browser.close();
  }
}
```

**실험 과제**:
```typescript
// 실험: 같은 Worker에서 연속 실행되는 테스트 2개
test.describe.serial('Serial Tests (같은 Worker)', () => {
  let sharedData: string;

  test('Test A', async ({ page }) => {
    sharedData = 'data-from-A';
    console.log('Test A - sharedData:', sharedData);
  });

  test('Test B', async ({ page }) => {
    console.log('Test B - sharedData:', sharedData);
    // 질문: sharedData가 'data-from-A'인가?
    // 답: Yes (같은 Worker의 메모리 공유)
  });
});
```

**핵심 이해**:
- **BrowserContext**: 테스트마다 새로 생성 (완전 격리)
- **Worker 메모리**: 같은 Worker 내 테스트는 메모리 공유 (변수)
- **쿠키/스토리지**: Context별로 격리

---

### 3. fullyParallel과 test.describe.serial의 차이는?

**탐구 목표**: 병렬/순차 실행 제어 방법을 이해합니다.

**질문 세부사항**:
- `fullyParallel: true`는 언제 사용하나?
- `test.describe.serial()`은 무엇을 보장하나?
- 같은 파일 내 테스트는 기본적으로 순차 실행인가?
- 파일 간 병렬 실행과 파일 내 병렬 실행의 차이는?

**탐구 활동**:
```typescript
// 활동 3-1: 기본 동작 (파일 단위 병렬, 파일 내 순차)
// test1.spec.ts
test('Test 1-1', async ({ page }) => {
  console.log('Test 1-1 시작', new Date().toISOString());
  await page.waitForTimeout(2000);
  console.log('Test 1-1 종료', new Date().toISOString());
});

test('Test 1-2', async ({ page }) => {
  console.log('Test 1-2 시작', new Date().toISOString());
  await page.waitForTimeout(2000);
  console.log('Test 1-2 종료', new Date().toISOString());
});

// 질문: Test 1-2는 Test 1-1이 끝난 후 시작하나?
// 답: 기본적으로 Yes (파일 내 순차)
```

```typescript
// 활동 3-2: fullyParallel 적용
// test2.spec.ts
test.describe.configure({ mode: 'parallel' });

test('Test 2-1', async ({ page }) => {
  console.log('Test 2-1 시작', new Date().toISOString());
  await page.waitForTimeout(2000);
  console.log('Test 2-1 종료', new Date().toISOString());
});

test('Test 2-2', async ({ page }) => {
  console.log('Test 2-2 시작', new Date().toISOString());
  await page.waitForTimeout(2000);
  console.log('Test 2-2 종료', new Date().toISOString());
});

// 질문: Test 2-1과 2-2가 동시에 시작하나?
// 답: Yes (병렬 모드)
```

**실행 모드 비교**:

| 모드 | 설정 | 동작 | 사용 시점 |
|------|------|------|----------|
| **기본 (순차)** | 없음 | 파일 내 순차, 파일 간 병렬 | 테스트 간 의존성 있을 때 |
| **fullyParallel** | `test.describe.configure({ mode: 'parallel' })` | 파일 내 병렬 | 독립적인 테스트들 |
| **serial** | `test.describe.serial()` | 순차 실행 강제 | E2E 플로우 (로그인 → 작업) |

**실험 과제**:
```typescript
// 실험: serial vs parallel 시간 비교
test.describe('Serial Tests', () => {
  test.describe.serial('Serial Group', () => {
    test('Test A (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
    test('Test B (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
    test('Test C (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
    // 총 시간: 6초
  });
});

test.describe('Parallel Tests', () => {
  test.describe.configure({ mode: 'parallel' });

  test('Test A (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
  test('Test B (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
  test('Test C (2초)', async () => await new Promise(r => setTimeout(r, 2000)));
  // 총 시간: 2초 (3개 Worker 가정)
});
```

---

### 4. Test Sharding이란? CI 환경에서 어떻게 활용하나?

**탐구 목표**: 대규모 테스트 스위트를 여러 머신에 분배하는 방법을 이해합니다.

**질문 세부사항**:
- Sharding은 Worker와 어떻게 다른가?
- `--shard=1/3`의 의미는?
- CI에서 3개 머신에 분배하려면?
- Sharding과 재시도(retry)의 관계는?

**탐구 활동**:
```bash
# 활동 4: Sharding 실험
# 전체 테스트를 3개 샤드로 분할

# Shard 1 (첫 번째 1/3)
npx playwright test --shard=1/3

# Shard 2 (두 번째 1/3)
npx playwright test --shard=2/3

# Shard 3 (마지막 1/3)
npx playwright test --shard=3/3

# 질문: 각 샤드는 어떤 테스트를 실행하나?
# 답: 테스트 파일을 해시하여 균등 분배
```

**Sharding vs Workers 비교**:

```
Workers (한 머신 내 병렬)
Machine 1
├─ Worker 1 → test1.spec.ts
├─ Worker 2 → test2.spec.ts
└─ Worker 3 → test3.spec.ts

Sharding (여러 머신 분산)
Machine 1 (--shard=1/3)
├─ Worker 1 → test1.spec.ts
└─ Worker 2 → test2.spec.ts

Machine 2 (--shard=2/3)
├─ Worker 1 → test3.spec.ts
└─ Worker 2 → test4.spec.ts

Machine 3 (--shard=3/3)
├─ Worker 1 → test5.spec.ts
└─ Worker 2 → test6.spec.ts
```

**CI 설정 예시 (GitHub Actions)**:
```yaml
# .github/workflows/playwright.yml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3] # 3개 머신으로 분산
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --shard=${{ matrix.shard }}/3
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report-${{ matrix.shard }}
          path: playwright-report/
```

**샤드별 결과 병합**:
```bash
# 각 샤드의 결과를 하나로 합치기
npx playwright merge-reports --reporter html ./shard-reports
```

**핵심 질문**:
- 테스트 100개, 3개 샤드 → 각각 33개씩 실행하나?
- 샤드 분배는 테스트 실행 시간을 고려하나?
- 한 샤드가 실패하면 전체가 실패하나?

---

### 5. Worker 설정 (CLI vs Config 파일)의 우선순위는?

**탐구 목표**: Worker 설정 방법과 우선순위를 이해합니다.

**질문 세부사항**:
- `playwright.config.ts`의 `workers` 설정
- CLI 플래그 `--workers`
- 환경변수 `PLAYWRIGHT_WORKERS`
- 어떤 설정이 최우선인가?

**탐구 활동**:
```typescript
// 활동 5: 설정 우선순위 확인
// playwright.config.ts
export default defineConfig({
  workers: 2, // Config 파일 설정
});
```

```bash
# 실험: 다양한 설정 조합
npx playwright test # → 2 workers (config 파일)
npx playwright test --workers=4 # → 4 workers (CLI 우선)
PLAYWRIGHT_WORKERS=1 npx playwright test # → 1 worker (환경변수)
PLAYWRIGHT_WORKERS=1 npx playwright test --workers=4 # → 4 workers (CLI 최우선)
```

**우선순위 (높은 순)**:
1. **CLI 플래그** (`--workers=N`)
2. **환경변수** (`PLAYWRIGHT_WORKERS=N`)
3. **Config 파일** (`workers: N`)
4. **기본값** (CPU 코어 수의 50%)

**동적 Worker 설정**:
```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI
    ? 2 // CI: 제한된 리소스
    : undefined, // 로컬: CPU 절반 사용
});
```

**실무 권장 설정**:
```typescript
// playwright.config.ts
const cpuCount = require('os').cpus().length;

export default defineConfig({
  workers: process.env.CI
    ? 2 // CI: 안정성 우선
    : Math.max(1, Math.floor(cpuCount / 2)), // 로컬: 성능 우선
});
```

---

### 6. Performance API를 Playwright에서 어떻게 측정하나?

**탐구 목표**: 웹 페이지 성능 지표를 테스트에서 측정하는 방법을 이해합니다.

**질문 세부사항**:
- Navigation Timing API란?
- Resource Timing API는 무엇을 측정하나?
- LCP, FCP, TTI를 Playwright에서 어떻게 측정?
- 성능 테스트를 E2E 테스트에 포함해야 하나?

**탐구 활동**:
```typescript
// 활동 6: Performance API 측정
test('TPS 티켓 목록 로딩 성능', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket-list');

  // Navigation Timing 측정
  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

    return {
      // DNS 조회 시간
      dnsTime: navigation.domainLookupEnd - navigation.domainLookupStart,

      // TCP 연결 시간
      tcpTime: navigation.connectEnd - navigation.connectStart,

      // 요청 → 응답 시간
      requestTime: navigation.responseEnd - navigation.requestStart,

      // DOM 파싱 시간
      domParseTime: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,

      // 전체 로딩 시간
      loadTime: navigation.loadEventEnd - navigation.fetchStart,
    };
  });

  console.log('성능 지표:', metrics);

  // 검증: 로딩 시간 3초 이내
  expect(metrics.loadTime).toBeLessThan(3000);
});
```

**Resource Timing 측정**:
```typescript
test('정적 리소스 로딩 시간', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket-list');

  const resources = await page.evaluate(() => {
    return performance.getEntriesByType('resource').map((entry: PerformanceResourceTiming) => ({
      name: entry.name,
      duration: entry.duration,
      size: entry.transferSize,
      type: entry.initiatorType,
    }));
  });

  // CSS/JS 파일별 로딩 시간 확인
  const cssFiles = resources.filter(r => r.name.endsWith('.css'));
  const jsFiles = resources.filter(r => r.name.endsWith('.js'));

  console.log('CSS 파일 평균 로딩:', cssFiles.reduce((a, b) => a + b.duration, 0) / cssFiles.length);
  console.log('JS 파일 평균 로딩:', jsFiles.reduce((a, b) => a + b.duration, 0) / jsFiles.length);
});
```

**Core Web Vitals 측정**:
```typescript
test('Core Web Vitals 측정', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket-list');

  // LCP (Largest Contentful Paint) - 가장 큰 콘텐츠 렌더링 시간
  const lcp = await page.evaluate(() => {
    return new Promise<number>((resolve) => {
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1] as any;
        resolve(lastEntry.renderTime || lastEntry.loadTime);
      }).observe({ entryTypes: ['largest-contentful-paint'] });

      // 타임아웃: 5초 후 측정
      setTimeout(() => resolve(0), 5000);
    });
  });

  console.log('LCP:', lcp, 'ms');
  expect(lcp).toBeLessThan(2500); // 2.5초 목표
});
```

**질문**:
- Navigation Timing과 Resource Timing의 차이는?
- LCP는 언제 측정되나? (페이지 로딩 중? 완료 후?)
- 성능 테스트는 매번 실행해야 하나?

---

### 7. Tracing과 Trace Viewer로 병렬 실행 문제를 디버깅하는 방법은?

**탐구 목표**: 병렬 실행 중 발생한 문제를 추적하고 분석하는 방법을 이해합니다.

**질문 세부사항**:
- Trace는 무엇을 기록하나?
- 병렬 실행 시 여러 Trace 파일이 생성되나?
- Trace Viewer에서 Worker 정보를 볼 수 있나?
- 경합 조건(race condition) 디버깅에 유용한가?

**탐구 활동**:
```typescript
// 활동 7: Tracing 활성화
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on', // 모든 테스트에서 Trace 기록
    // 또는
    // trace: 'on-first-retry', // 재시도할 때만
    // trace: 'retain-on-failure', // 실패 시만 보관
  },
});
```

```bash
# Trace 기록하며 테스트 실행
npx playwright test --trace on

# Trace Viewer 열기
npx playwright show-trace trace.zip
```

**Trace Viewer 정보**:
```
┌──────────────────────────────────────┐
│  Trace Viewer                        │
├──────────────────────────────────────┤
│  Timeline:                           │
│  [────▶ Test 시작                    │
│     ├─ page.goto()                   │
│     ├─ page.click()                  │
│     └─ expect() ✅                   │
├──────────────────────────────────────┤
│  Network:                            │
│  GET /api/tickets → 200 (345ms)     │
│  GET /static/app.js → 200 (89ms)    │
├──────────────────────────────────────┤
│  Console:                            │
│  Worker Index: 2                     │
│  Test started at 10:23:45            │
├──────────────────────────────────────┤
│  Screenshots: (각 단계)              │
│  [🖼️ Before] [🖼️ After]              │
└──────────────────────────────────────┘
```

**병렬 실행 문제 디버깅 예시**:
```typescript
// 시나리오: 병렬 실행 시 가끔 실패하는 테스트
test('TPS 티켓 생성 (가끔 실패)', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket-create');
  await page.getByLabel('제목').fill('Test');
  await page.getByRole('button', { name: '저장' }).click();

  // 가끔 실패: "저장되었습니다" 메시지가 안 보임
  await expect(page.getByText('저장되었습니다')).toBeVisible();
});

// Trace Viewer 분석:
// 1. Timeline에서 API 응답 시간 확인
// 2. Network 탭에서 POST /api/tickets 상태 확인
// 3. Screenshots에서 UI 상태 확인
// 4. Console에서 에러 로그 확인

// 발견: API 응답이 느려서 timeout 전에 메시지 표시 안 됨
// 해결: timeout 늘리거나 API 응답 대기 추가
await page.waitForResponse(resp => resp.url().includes('/api/tickets'));
await expect(page.getByText('저장되었습니다')).toBeVisible({ timeout: 5000 });
```

**실험 과제**:
1. 병렬 실행 중 실패하는 테스트의 Trace 기록
2. Trace Viewer에서 Worker Index 확인
3. Network 탭에서 API 호출 순서 분석
4. 경합 조건 패턴 발견 (예: 동시에 같은 리소스 접근)

---

## 실전 시나리오: TPS 티켓 목록 성능 테스트

**시나리오**: TPS 티켓 목록 페이지의 로딩 성능을 측정하고 병렬 실행으로 효율화

```typescript
test.describe('TPS 티켓 목록 성능', () => {
  // 병렬 실행 (독립적인 테스트들)
  test.describe.configure({ mode: 'parallel' });

  test('초기 로딩 성능', async ({ page }) => {
    await page.goto('http://localhost:3002/ticket-list');

    const metrics = await page.evaluate(() => {
      const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      return {
        ttfb: nav.responseStart - nav.requestStart, // Time to First Byte
        domParse: nav.domContentLoadedEventEnd - nav.domContentLoadedEventStart,
        loadTime: nav.loadEventEnd - nav.fetchStart,
      };
    });

    console.log('성능 지표:', metrics);
    expect(metrics.loadTime).toBeLessThan(3000); // 3초 이내
  });

  test('필터 적용 후 렌더링 성능', async ({ page }) => {
    await page.goto('http://localhost:3002/ticket-list');

    const startTime = Date.now();

    // 상태 필터 변경
    await page.getByLabel('상태').selectOption('완료');

    // 결과 렌더링 대기
    await page.getByRole('row').filter({ hasText: '완료' }).first().waitFor();

    const renderTime = Date.now() - startTime;
    console.log('필터 렌더링 시간:', renderTime, 'ms');
    expect(renderTime).toBeLessThan(1000); // 1초 이내
  });

  test('대량 데이터 스크롤 성능', async ({ page }) => {
    await page.goto('http://localhost:3002/ticket-list?count=1000'); // 1000개 티켓

    // 스크롤 전 FPS 측정
    const fps = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        let frames = 0;
        const checkFrame = () => {
          frames++;
          if (frames < 60) {
            requestAnimationFrame(checkFrame);
          } else {
            resolve(60); // 1초에 60프레임
          }
        };
        requestAnimationFrame(checkFrame);
      });
    });

    console.log('FPS:', fps);
    expect(fps).toBeGreaterThan(30); // 30fps 이상
  });
});
```

**탐구 질문**:
1. 위 3개 테스트는 병렬로 실행되나?
2. 각 테스트는 다른 Worker에서 실행되나?
3. 성능 측정 결과가 Worker마다 다를 수 있나?

---

## 다음 단계

### 학습 문서로 이동
→ `LEARN.md`에서 병렬 실행 설정, Worker 관리, 성능 측정 패턴 학습

### 실습 과제
→ `practice/` 폴더에서 병렬 실행 최적화 및 성능 테스트 작성

### 확인 사항
- [ ] Worker 모델 동작 원리 이해했나?
- [ ] fullyParallel vs serial 차이 파악했나?
- [ ] Sharding을 CI에 적용할 수 있나?
- [ ] Performance API로 성능 측정 가능한가?
- [ ] Trace Viewer로 병렬 실행 문제 디버깅할 수 있나?

---

**다음 학습**: `LEARN.md`에서 Worker 아키텍처, 병렬 실행 전략, 성능 최적화 패턴 학습
