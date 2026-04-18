# 01. 설치와 첫 테스트 - 조사 (INVESTIGATE)

소크라테스식 질문을 통해 Playwright Test의 핵심 개념을 탐구합니다.

---

## 학습 목표

이 단계에서는 다음 질문들을 스스로 탐구하며 Playwright Test의 기초를 이해합니다:

1. playwright.config.ts의 주요 설정들은 어떤 역할을 하는가?
2. test()와 expect()는 내부적으로 어떻게 동작하는가?
3. beforeEach/afterEach Hook은 언제, 어떤 순서로 실행되는가?
4. Playwright는 어떻게 테스트 파일을 찾아내는가?
5. 다양한 리포터들은 어떤 차이가 있는가?

---

## 질문 1: playwright.config.ts 주요 설정 옵션

### 핵심 질문
`playwright.config.ts` 파일에는 projects, use, webServer 등 다양한 설정이 있습니다. 각 설정은 어떤 역할을 하며, 왜 필요한가?

### 탐구할 하위 질문

#### 1.1 projects 배열은 왜 필요한가?
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

**질문**:
- 왜 하나의 테스트를 여러 브라우저에서 실행하려고 할까?
- 각 project는 독립적으로 실행되는가?
- Mobile Safari와 Desktop Safari는 어떻게 구분할까?

**탐구 활동**:
```bash
# 특정 프로젝트만 실행해보기
npx playwright test --project=chromium
npx playwright test --project=webkit

# 차이점을 관찰하세요
```

#### 1.2 use 블록의 옵션들은 무엇을 제어하는가?
```typescript
use: {
  baseURL: 'http://localhost:3002',
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

**질문**:
- baseURL을 설정하면 테스트 코드에서 어떤 이점이 있을까?
- trace는 정확히 무엇을 기록하며, 'on-first-retry'는 언제 작동할까?
- screenshot과 video의 차이는 무엇일까?

**탐구 활동**:
```typescript
// 테스트를 일부러 실패시켜보세요
test('실패 테스트', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toHaveText('존재하지 않는 텍스트');
});

// test-results/ 폴더를 확인하세요
// 어떤 파일들이 생성되었나요?
```

#### 1.3 webServer 설정은 언제 사용하는가?
```typescript
webServer: {
  command: 'npm run start:mock',
  port: 3002,
  reuseExistingServer: !process.env.CI,
}
```

**질문**:
- 왜 테스트 전에 서버를 자동으로 시작할까?
- `reuseExistingServer`는 어떤 상황에서 유용할까?
- CI 환경에서는 왜 다르게 동작해야 할까?

**힌트**: 로컬 개발과 CI 환경의 차이를 생각해보세요.

---

## 질문 2: test()와 expect()의 내부 동작 - fixture란 무엇인가?

### 핵심 질문
`test()` 함수는 콜백으로 `{ page, context, browser }` 같은 객체를 전달받습니다. 이것들은 어디서 오며, 어떻게 관리되는가?

### 탐구할 하위 질문

#### 2.1 fixture는 무엇인가?
```typescript
test('예시', async ({ page, context, browser }) => {
  // page, context, browser는 어디서 왔을까?
});
```

**질문**:
- page, context, browser는 누가 생성하는가?
- 각 테스트마다 새로운 page가 생성되는가?
- 테스트 종료 후 자동으로 정리되는가?

**탐구 활동**:
```typescript
test('fixture 탐구 1', async ({ page }) => {
  console.log('Test 1 - page:', page);
});

test('fixture 탐구 2', async ({ page }) => {
  console.log('Test 2 - page:', page);
});

// 두 page 객체가 같은가요? 다른가요?
```

#### 2.2 커스텀 fixture를 만들 수 있는가?
```typescript
// 예시: 로그인된 사용자 fixture
const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('#username', 'testuser');
    await page.fill('#password', 'password');
    await page.click('button[type="submit"]');
    await use(page);
  },
});
```

**질문**:
- 왜 커스텀 fixture를 만들까?
- `use()` 함수는 무엇을 하는가?
- 여러 테스트에서 재사용하려면 어떻게 해야 할까?

**힌트**: DRY 원칙과 테스트 설정의 재사용성을 생각해보세요.

#### 2.3 expect()는 일반 assertion과 어떻게 다른가?
```typescript
// Jest/Vitest
expect(value).toBe(10);

// Playwright
await expect(page.locator('h1')).toHaveText('Hello');
```

**질문**:
- 왜 Playwright의 expect()는 `await`를 사용하는가?
- 내부적으로 재시도(retry) 로직이 있다는데, 왜 필요할까?
- 타임아웃은 어떻게 설정하는가?

**탐구 활동**:
```typescript
test('재시도 확인', async ({ page }) => {
  await page.goto('/');

  // 이 요소가 DOM에 늦게 나타난다면?
  await expect(page.locator('.delayed-element')).toBeVisible();

  // expect()가 자동으로 기다려줄까요?
});
```

---

## 질문 3: beforeEach/afterEach Hook의 실행 순서와 활용

### 핵심 질문
테스트 전후로 공통 로직을 실행하는 Hook들은 정확히 언제, 어떤 순서로 실행되는가?

### 탐구할 하위 질문

#### 3.1 Hook의 실행 순서는?
```typescript
test.describe('사용자 기능', () => {
  test.beforeAll(async () => {
    console.log('1. beforeAll');
  });

  test.beforeEach(async ({ page }) => {
    console.log('2. beforeEach');
  });

  test('테스트 A', async ({ page }) => {
    console.log('3. 테스트 A');
  });

  test('테스트 B', async ({ page }) => {
    console.log('4. 테스트 B');
  });

  test.afterEach(async () => {
    console.log('5. afterEach');
  });

  test.afterAll(async () => {
    console.log('6. afterAll');
  });
});
```

**질문**:
- 실제 콘솔 출력 순서는 어떻게 될까?
- beforeAll은 테스트마다 실행되는가, 한 번만 실행되는가?
- afterEach는 테스트가 실패해도 실행되는가?

**탐구 활동**: 위 코드를 실행하고 출력을 기록해보세요.

#### 3.2 중첩된 describe의 Hook 순서는?
```typescript
test.describe('외부 describe', () => {
  test.beforeEach(async () => {
    console.log('외부 beforeEach');
  });

  test.describe('내부 describe', () => {
    test.beforeEach(async () => {
      console.log('내부 beforeEach');
    });

    test('테스트', async () => {
      console.log('테스트 실행');
    });
  });
});
```

**질문**:
- 외부와 내부 beforeEach 중 어느 것이 먼저 실행될까?
- afterEach는 역순으로 실행될까?

#### 3.3 Hook은 언제 사용하는가?
**질문**:
- 모든 테스트에서 로그인이 필요하다면?
- 테스트 후 데이터베이스를 초기화해야 한다면?
- 테스트마다 특정 페이지로 이동해야 한다면?

**탐구 활동**:
```typescript
// 이런 반복을 Hook으로 개선할 수 있을까요?
test('테스트 1', async ({ page }) => {
  await page.goto('/dashboard');
  // 테스트 로직
});

test('테스트 2', async ({ page }) => {
  await page.goto('/dashboard');
  // 테스트 로직
});
```

---

## 질문 4: Playwright Test Runner의 테스트 발견 규칙

### 핵심 질문
Playwright는 프로젝트에서 어떤 파일을 테스트로 인식하는가?

### 탐구할 하위 질문

#### 4.1 testMatch 패턴은 어떻게 동작하는가?
```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
});
```

**질문**:
- `**/*.spec.ts`에서 `**`는 무엇을 의미할까?
- `.test.ts`와 `.spec.ts` 둘 다 인식하려면?
- `tests/` 폴더 외부의 파일도 실행할 수 있을까?

**탐구 활동**:
```bash
# 다양한 패턴 시도
npx playwright test tests/login.spec.ts
npx playwright test --grep "로그인"
npx playwright test --grep-invert "느린 테스트"
```

#### 4.2 testIgnore는 언제 사용하는가?
```typescript
testIgnore: '**/node_modules/**',
```

**질문**:
- 왜 특정 파일을 제외해야 할까?
- `.skip` 메서드와 어떤 차이가 있을까?

#### 4.3 테스트 그룹화 전략은?
**질문**:
- 통합 테스트와 단위 테스트를 분리하려면?
- 느린 테스트를 선택적으로 실행하려면?

**힌트**:
```typescript
test.describe('통합 테스트', () => {
  test('API 호출 테스트 @integration', async () => {});
});

// npx playwright test --grep @integration
```

---

## 질문 5: 리포터 종류와 설정 방법

### 핵심 질문
테스트 결과를 어떤 형식으로 확인할 수 있으며, 각 리포터의 장단점은 무엇인가?

### 탐구할 하위 질문

#### 5.1 기본 제공 리포터들
```typescript
reporter: [
  ['html'],
  ['list'],
  ['json', { outputFile: 'test-results.json' }],
  ['junit', { outputFile: 'junit.xml' }],
]
```

**질문**:
- 각 리포터는 언제 사용하는가?
  - `html`: ?
  - `list`: ?
  - `json`: ?
  - `junit`: ?
- 여러 리포터를 동시에 사용할 수 있는가?

**탐구 활동**:
```bash
# 각 리포터 시도
npx playwright test --reporter=html
npx playwright test --reporter=list
npx playwright test --reporter=json

# 생성된 파일들을 확인하세요
```

#### 5.2 HTML 리포트의 기능은?
**질문**:
- HTML 리포트에서 어떤 정보를 확인할 수 있는가?
- 실패한 테스트의 스크린샷을 볼 수 있는가?
- Trace Viewer는 어떻게 여는가?

**탐구 활동**:
```bash
npx playwright test
npx playwright show-report

# 브라우저에서 열리는 리포트를 탐험해보세요
```

#### 5.3 CI/CD 환경에서는?
**질문**:
- GitHub Actions에서는 어떤 리포터가 적합할까?
- 테스트 결과를 Slack으로 보낼 수 있을까?
- 커스텀 리포터를 만들 수 있는가?

**힌트**: CI 환경에서는 사람이 읽기 쉬운 형식과 기계가 파싱하기 쉬운 형식이 다릅니다.

---

## 종합 탐구 활동

### 실습 1: 설정 파일 해부하기
```typescript
// playwright.config.ts를 열고 각 설정을 하나씩 변경해보세요

// 1. baseURL 제거 → 테스트 코드는 어떻게 바뀌어야 할까?
// 2. retries를 2로 설정 → 실패한 테스트가 몇 번 재시도될까?
// 3. workers를 1로 설정 → 테스트 실행 시간이 바뀔까?
```

### 실습 2: Hook 순서 완전 정복
```typescript
// 다음 코드의 출력 순서를 예측한 후 실행해보세요
test.describe('Level 1', () => {
  test.beforeAll(() => console.log('L1 beforeAll'));
  test.beforeEach(() => console.log('L1 beforeEach'));

  test('Test 1', () => console.log('Test 1'));

  test.describe('Level 2', () => {
    test.beforeEach(() => console.log('L2 beforeEach'));
    test('Test 2', () => console.log('Test 2'));
    test.afterEach(() => console.log('L2 afterEach'));
  });

  test.afterEach(() => console.log('L1 afterEach'));
  test.afterAll(() => console.log('L1 afterAll'));
});
```

### 실습 3: 커스텀 fixture 만들기
```typescript
// 목표: 로그인된 상태의 page fixture 만들기
// 힌트: base.extend() 사용
```

---

## 생각해볼 점

### 설계 질문
1. **왜 Playwright는 브라우저 컨텍스트를 매 테스트마다 새로 만들까?**
   - 힌트: 테스트 격리(isolation)와 상태 공유의 위험성

2. **beforeAll vs beforeEach를 어떻게 선택할까?**
   - 힌트: 성능 vs 테스트 독립성

3. **왜 trace를 매번 기록하지 않고 'on-first-retry'를 사용할까?**
   - 힌트: 디스크 용량과 성능

### 실무 질문
1. **실제 프로젝트에서 테스트를 어떻게 구조화할까?**
   - 페이지별? 기능별? 사용자 시나리오별?

2. **TPS 프로젝트에 적용한다면?**
   - 어떤 브라우저를 테스트할까?
   - 어떤 리포터를 사용할까?
   - Mock 서버 vs 실제 개발 서버?

3. **테스트가 느려지면?**
   - 병렬 실행 최적화
   - 테스트 분할 전략
   - 선택적 테스트 실행

---

## 다음 단계

이 질문들을 탐구한 후:
1. `LEARN.md`에서 공식 설명 확인
2. `practice/` 폴더에서 실습 코드 작성
3. Mock 서버(`http://localhost:3002`)로 실제 테스트 작성

**핵심 원칙**: 문서를 읽기 전에 먼저 실험하고 질문하세요. 실패는 최고의 학습 도구입니다.
