# 07. TPS 실전 통합 - 조사 (INVESTIGATE)

소크라테스식 질문을 통해 실제 TPS 시스템에 Playwright를 적용하는 방법을 탐구합니다.

---

## 학습 목표

실무 프로젝트에 E2E 테스트를 도입할 때 마주하는 핵심 질문들을 탐구합니다:

1. 실제 환경에서 인증을 어떻게 처리할까? (storageState)
2. 동적 데이터는 어떻게 검증할까?
3. 불안정한(flaky) API 호출은 어떻게 대응할까?
4. 테스트 데이터는 어떻게 관리할까?
5. 복잡한 다단계 워크플로우는 어떻게 테스트할까?
6. CI/CD 환경에서는 어떻게 실행할까?

---

## 질문 1: 실제 환경에서 인증 처리 - storageState란 무엇인가?

### 핵심 질문
Mock 서버는 인증이 필요 없지만, 실제 TPS 시스템은 로그인이 필요합니다. 매 테스트마다 로그인하면 너무 느린데, 더 나은 방법은 없을까?

### 탐구할 하위 질문

#### 1.1 storageState는 무엇을 저장하는가?
```typescript
// 로그인 후 상태 저장
await page.context().storageState({ path: '.auth/user.json' });
```

**질문**:
- storageState에는 정확히 무엇이 저장될까?
  - 쿠키(Cookies)?
  - 로컬 스토리지(localStorage)?
  - 세션 스토리지(sessionStorage)?
- 이 파일을 Git에 커밋해도 될까?
- 토큰이 만료되면 어떻게 될까?

**탐구 활동**:
```bash
# 로그인 후 생성된 .auth/user.json 파일을 열어보세요
cat .auth/user.json

# 어떤 정보가 들어있나요?
# 민감한 정보가 포함되어 있나요?
```

#### 1.2 global-setup.ts 패턴은 무엇인가?
```typescript
// global-setup.ts
import { chromium } from '@playwright/test';

async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // 한 번만 로그인
  await page.goto('http://localhost:3002/login');
  await page.fill('#username', 'admin');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');

  // 상태 저장
  await page.context().storageState({ path: '.auth/user.json' });
  await browser.close();
}

export default globalSetup;
```

**질문**:
- global-setup은 언제 실행되는가?
- 모든 테스트가 시작되기 전? 각 프로젝트마다?
- 병렬 실행과는 어떤 관계가 있을까?

**탐구 활동**:
```typescript
// playwright.config.ts
export default defineConfig({
  globalSetup: './global-setup.ts',
  use: {
    storageState: '.auth/user.json',
  },
});

// 이렇게 설정하면 어떤 일이 일어날까?
```

#### 1.3 로그인 실패 시나리오는 어떻게 테스트할까?
**질문**:
- global-setup으로 로그인한 상태라면, 로그인 실패 테스트는 어떻게 작성할까?
- storageState를 사용하지 않는 테스트는 어떻게 만들까?
- 권한이 다른 여러 사용자 역할(admin, user)을 테스트하려면?

**힌트**:
```typescript
// 특정 테스트에서만 storageState 무시하기
test.use({ storageState: undefined });

test('로그인 실패 테스트', async ({ page }) => {
  // 로그인되지 않은 상태
});
```

---

## 질문 2: 동적 데이터 검증 전략

### 핵심 질문
Mock 서버는 고정된 데이터를 반환하지만, 실제 시스템은 데이터가 계속 변합니다. "정확히 10개의 티켓"을 검증하는 대신 어떻게 테스트할까?

### 탐구할 하위 질문

#### 2.1 정규식(Regex) matcher는 언제 사용하는가?
```typescript
// ❌ Mock 서버에서는 가능
await expect(page.locator('.ticket-id')).toHaveText('TICKET-001');

// ✅ 실제 환경에서는?
await expect(page.locator('.ticket-id')).toHaveText(/TICKET-\d+/);
```

**질문**:
- 왜 정규식이 필요한가?
- 티켓 ID가 "CICD-12345" 또는 "PMS-67890" 형태라면?
- 날짜 형식(2024-02-05)을 검증하려면?

**탐구 활동**:
```typescript
// 다음 중 어떤 assertion이 실무에 적합한가?
await expect(page.locator('.created-at')).toHaveText('2024-02-05 14:30:00'); // ❌
await expect(page.locator('.created-at')).toHaveText(/\d{4}-\d{2}-\d{2}/);   // ✅?
await expect(page.locator('.created-at')).not.toBeEmpty();                   // ✅?
```

#### 2.2 유연한 assertion 전략은?
```typescript
// ❌ 취약한 테스트
await expect(page.locator('tbody tr')).toHaveCount(10);

// ✅ 유연한 테스트
const rows = await page.locator('tbody tr').count();
expect(rows).toBeGreaterThan(0);

// 또는
await expect(page.locator('tbody tr')).not.toHaveCount(0);
```

**질문**:
- "최소 1개 이상의 티켓이 있다"를 검증하면 될까?
- "최대 100개까지만 표시한다"는 어떻게 검증할까?
- 빈 상태(empty state)는 어떻게 테스트할까?

#### 2.3 동적 데이터와 스크린샷 비교는?
**질문**:
- 스크린샷 비교는 Mock 서버에서만 유용한가?
- 실제 환경에서 스크린샷 테스트를 하려면 어떻게 해야 할까?
- 타임스탬프나 동적 텍스트를 마스킹할 수 있을까?

**힌트**:
```typescript
await expect(page).toHaveScreenshot({
  mask: [page.locator('.timestamp')], // 동적 영역 마스킹
});
```

---

## 질문 3: 네트워크 인터셉션으로 불안정한 API 대응

### 핵심 질문
실제 API는 간헐적으로 느리거나 실패할 수 있습니다. 테스트를 안정적으로 만들려면 어떻게 해야 할까?

### 탐구할 하위 질문

#### 3.1 route interception은 언제 사용하는가?
```typescript
// API 응답을 모킹
await page.route('**/api/tickets', async (route) => {
  await route.fulfill({
    status: 200,
    body: JSON.stringify({ tickets: [], total: 0 }),
  });
});
```

**질문**:
- 실제 TPS API를 호출하지 않고 테스트할 수 있을까?
- Mock 서버와 route interception의 차이는 무엇인가?
- 언제 실제 API를 호출하고, 언제 모킹해야 할까?

**탐구 활동**:
```typescript
// 실패하는 API를 시뮬레이션
await page.route('**/api/tickets', async (route) => {
  await route.fulfill({ status: 500, body: 'Internal Server Error' });
});

// 이때 UI는 어떻게 동작해야 할까?
// 에러 메시지가 표시되는가?
// 로딩 상태가 끝나는가?
```

#### 3.2 느린 API 응답 시뮬레이션은?
```typescript
await page.route('**/api/tickets', async (route) => {
  await new Promise(resolve => setTimeout(resolve, 5000)); // 5초 지연
  await route.continue();
});
```

**질문**:
- 로딩 인디케이터(spinner)가 제대로 표시되는가?
- 타임아웃 처리가 되는가?
- 사용자 경험이 어떻게 달라지는가?

#### 3.3 실제 API와 Mock을 조합할 수 있을까?
**질문**:
- 목록 조회는 실제 API, 생성/수정은 모킹?
- 언제 이런 전략이 유용할까?
- 테스트 데이터 오염을 어떻게 방지할까?

**힌트**: 읽기 작업은 실제 API, 쓰기 작업은 모킹하면 데이터베이스를 오염시키지 않습니다.

---

## 질문 4: 테스트 데이터 관리 전략

### 핵심 질문
테스트마다 티켓을 생성한다면, 데이터베이스가 점점 더러워집니다. 어떻게 깨끗하게 관리할까?

### 탐구할 하위 질문

#### 4.1 테스트 데이터 생성 전략은?
**전략 A: 실제 UI로 생성**
```typescript
test('티켓 생성 테스트', async ({ page }) => {
  await page.goto('/tickets/new');
  await page.fill('#title', 'Test Ticket');
  await page.click('button[type="submit"]');
  // 이 티켓은 누가 삭제할까?
});
```

**전략 B: API로 직접 생성**
```typescript
test('티켓 목록 테스트', async ({ page, request }) => {
  // API로 테스트 데이터 생성
  const response = await request.post('/api/tickets', {
    data: { title: 'Test Ticket' }
  });
  const ticket = await response.json();

  // UI 테스트
  await page.goto('/tickets');
  await expect(page.locator(`text=${ticket.title}`)).toBeVisible();

  // API로 정리
  await request.delete(`/api/tickets/${ticket.id}`);
});
```

**질문**:
- 어느 전략이 더 나을까?
- E2E 테스트의 범위는 어디까지여야 할까?
- Setup/Teardown을 어떻게 구조화할까?

#### 4.2 테스트 격리(Isolation) vs 속도는?
**질문**:
- 각 테스트가 독립적인 데이터를 가지면 안전하지만 느립니다.
- 공통 테스트 데이터를 공유하면 빠르지만 순서 의존성이 생깁니다.
- 어떤 균형점을 찾아야 할까?

**탐구 활동**:
```typescript
// 패턴 A: 완전한 격리
test.beforeEach(async ({ request }) => {
  await request.post('/api/tickets', { data: testData });
});
test.afterEach(async ({ request }) => {
  await request.delete('/api/tickets/test-*');
});

// 패턴 B: 공유 데이터
test.beforeAll(async ({ request }) => {
  await request.post('/api/tickets', { data: sharedData });
});

// 어느 패턴이 언제 적합한가?
```

#### 4.3 실제 환경에서 테스트 데이터 식별은?
**질문**:
- 테스트 데이터와 실제 데이터를 어떻게 구분할까?
- "TEST-" 접두사? 특정 태그? 별도 계정?
- 운영 환경에 영향을 주지 않으려면?

**힌트**: 개발/스테이징 환경 전용 테스트 계정을 만들고, 데이터에 메타데이터 추가.

---

## 질문 5: 복잡한 다단계 워크플로우 테스트

### 핵심 질문
"로그인 → 티켓 목록 → 필터링 → 상세 보기 → 수정 → 검증" 같은 긴 시나리오를 어떻게 테스트할까?

### 탐구할 하위 질문

#### 5.1 하나의 긴 테스트 vs 여러 짧은 테스트?
**패턴 A: 하나의 긴 E2E 테스트**
```typescript
test('전체 티켓 관리 워크플로우', async ({ page }) => {
  // 1. 로그인
  await page.goto('/login');
  await page.fill('#username', 'admin');
  await page.click('button[type="submit"]');

  // 2. 티켓 생성
  await page.goto('/tickets/new');
  await page.fill('#title', 'Test');
  await page.click('button[type="submit"]');

  // 3. 목록에서 확인
  await page.goto('/tickets');
  await expect(page.locator('text=Test')).toBeVisible();

  // 4. 상세 보기
  await page.click('text=Test');
  await expect(page.locator('.ticket-detail')).toBeVisible();

  // ... 계속
});
```

**패턴 B: 독립적인 여러 테스트**
```typescript
test.describe('티켓 관리', () => {
  test('티켓 생성', async ({ page }) => { /* ... */ });
  test('티켓 목록 조회', async ({ page }) => { /* ... */ });
  test('티켓 상세 보기', async ({ page }) => { /* ... */ });
});
```

**질문**:
- 어느 패턴의 장단점은?
- 중간 단계가 실패하면?
- 유지보수는 어느 쪽이 쉬울까?

#### 5.2 Page Object Model과의 조합은?
```typescript
// POM을 사용한 워크플로우
test('워크플로우', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const ticketListPage = new TicketListPage(page);
  const ticketDetailPage = new TicketDetailPage(page);

  await loginPage.login('admin', 'password');
  await ticketListPage.searchTicket('CICD-001');
  await ticketListPage.clickFirstTicket();
  await ticketDetailPage.verifyTitle('CI/CD 구축');
});
```

**질문**:
- POM이 복잡한 워크플로우를 어떻게 단순화하는가?
- 페이지 간 이동은 누가 관리할까?
- 공통 로직(로그인, 네비게이션)은 어디에 둘까?

#### 5.3 조건부 로직과 상태 관리는?
**질문**:
- "티켓이 이미 있으면 수정, 없으면 생성"은 어떻게 테스트할까?
- 테스트 중 상태를 어떻게 추적할까?
- 이전 단계의 결과를 다음 단계에 전달하려면?

**탐구 활동**:
```typescript
test('조건부 워크플로우', async ({ page }) => {
  const ticketExists = await page.locator('text=CICD-001').isVisible();

  if (ticketExists) {
    // 수정 플로우
  } else {
    // 생성 플로우
  }

  // 이런 조건부 로직이 테스트에 적합한가?
});
```

---

## 질문 6: CI/CD 통합과 실행 전략

### 핵심 질문
로컬에서는 잘 동작하는데 GitHub Actions에서는 실패합니다. 무엇이 다를까?

### 탐구할 하위 질문

#### 6.1 CI 환경의 제약사항은?
**질문**:
- Headless 모드가 아니면 실행이 안 되는가?
- 네트워크가 느리면?
- 병렬 실행 worker 수는?
- 타임아웃 설정을 더 넉넉히 해야 할까?

**탐구 활동**:
```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  use: {
    actionTimeout: process.env.CI ? 30000 : 10000,
  },
});

// CI 환경을 감지해서 다르게 설정하는 이유는?
```

#### 6.2 테스트 아티팩트(Artifacts) 관리는?
**질문**:
- 실패한 테스트의 스크린샷을 어떻게 저장할까?
- Trace 파일은?
- HTML 리포트는 어디서 볼까?

**힌트**:
```yaml
# .github/workflows/test.yml
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

#### 6.3 선택적 테스트 실행 전략은?
**질문**:
- 모든 커밋마다 전체 E2E 테스트를 실행해야 할까?
- PR에서만? 특정 브랜치만?
- 변경된 기능과 관련된 테스트만 실행할 수 있을까?

**탐구 활동**:
```bash
# 태그를 사용한 선택적 실행
npx playwright test --grep @smoke    # 스모크 테스트만
npx playwright test --grep @critical # 중요 테스트만
npx playwright test --grep-invert @slow # 느린 테스트 제외

# 이런 전략을 CI에 어떻게 적용할까?
```

---

## 질문 7: 권한과 역할 기반 테스트

### 핵심 질문
Admin과 일반 User가 볼 수 있는 화면이 다릅니다. 어떻게 테스트할까?

### 탐구할 하위 질문

#### 7.1 여러 사용자 역할을 어떻게 테스트할까?
**패턴 A: 각 역할마다 storageState 분리**
```typescript
// global-setup.ts
// admin 로그인 → .auth/admin.json
// user 로그인 → .auth/user.json

// playwright.config.ts
projects: [
  {
    name: 'admin-tests',
    use: { storageState: '.auth/admin.json' },
    testMatch: '**/admin-*.spec.ts',
  },
  {
    name: 'user-tests',
    use: { storageState: '.auth/user.json' },
    testMatch: '**/user-*.spec.ts',
  },
]
```

**질문**:
- 이 패턴의 장점은?
- 역할이 10개라면?
- 테스트 실행 시간은?

#### 7.2 권한 검증 테스트 작성법은?
```typescript
test('일반 유저는 삭제 버튼을 볼 수 없다', async ({ page }) => {
  // user.json으로 로그인된 상태
  await page.goto('/tickets/CICD-001');
  await expect(page.locator('button:has-text("삭제")')).not.toBeVisible();
});

test('관리자는 삭제 버튼을 볼 수 있다', async ({ page }) => {
  // admin.json으로 로그인된 상태
  await page.goto('/tickets/CICD-001');
  await expect(page.locator('button:has-text("삭제")')).toBeVisible();
});
```

**질문**:
- 같은 페이지를 다른 권한으로 테스트하는 것이 효율적인가?
- 어떻게 DRY하게 만들까?

#### 7.3 동적 권한 체크는?
**질문**:
- 사용자가 생성한 티켓만 수정 가능하다면?
- 런타임에 권한이 변경된다면?
- 권한 에러를 어떻게 테스트할까?

---

## 종합 탐구 활동

### 실습 1: 인증 시스템 구축
1. `global-setup.ts` 작성 (Mock 서버 로그인)
2. `.auth/user.json` 생성 확인
3. storageState를 사용하는 테스트 작성
4. storageState 없이 실행하면 어떻게 되는지 확인

### 실습 2: 동적 데이터 검증
1. Mock 서버의 티켓 데이터를 요청마다 랜덤하게 변경
2. 정규식과 유연한 assertion으로 테스트 작성
3. 스크린샷 비교 테스트에 마스킹 적용

### 실습 3: 네트워크 인터셉션
1. API 지연 시뮬레이션 (5초)
2. API 실패 시뮬레이션 (500 에러)
3. UI가 적절하게 대응하는지 검증

### 실습 4: 전체 워크플로우
1. 로그인 → 티켓 생성 → 목록 확인 → 상세 보기 → 수정 → 검증
2. POM 적용해서 리팩토링
3. 실패 시 어느 단계인지 명확하게 표시

---

## 생각해볼 점

### 설계 질문
1. **E2E 테스트의 범위는 어디까지여야 할까?**
   - 모든 기능을 E2E로 테스트?
   - 핵심 사용자 시나리오만?
   - 단위/통합 테스트와의 균형은?

2. **Mock vs 실제 환경 전략은?**
   - Mock 서버로 빠른 피드백
   - 실제 환경으로 주기적 검증
   - 하이브리드 접근법?

3. **테스트 안정성 vs 현실성은?**
   - 완벽하게 통제된 Mock 환경 (안정적이지만 비현실적)
   - 실제 환경 (현실적이지만 불안정)
   - 어떻게 균형을 잡을까?

### 실무 질문
1. **TPS 프로젝트 도입 계획**
   - 어떤 화면부터 테스트할까?
   - 개발/스테이징/프로덕션 중 어느 환경에서?
   - 누가 테스트를 작성하고 유지보수할까?

2. **실패 대응 전략**
   - 테스트가 실패하면 배포를 막을까?
   - 불안정한 테스트는 어떻게 관리할까?
   - Flaky test 대시보드?

3. **팀 협업**
   - 개발자가 E2E 테스트를 작성할까?
   - QA 팀이 전담할까?
   - 테스트 코드 리뷰 프로세스는?

### 철학적 질문
1. **E2E 테스트의 가치는 무엇인가?**
   - 버그 발견?
   - 리그레션 방지?
   - 문서화?
   - 자신감?

2. **언제 E2E 테스트를 작성하지 말아야 할까?**
   - 너무 자주 변경되는 UI?
   - 단위 테스트로 충분한 경우?
   - 테스트 작성/유지보수 비용 > 가치?

3. **완벽한 E2E 테스트 커버리지는 가능한가?**
   - 모든 조합을 테스트할 수 있을까?
   - 80/20 법칙은?
   - 언제 "충분하다"고 판단할까?

---

## 다음 단계

이 질문들을 탐구한 후:
1. `LEARN.md`에서 패턴과 Best Practice 학습
2. `practice/` 폴더에서 실전 테스트 작성
   - `tps-login.spec.ts`: 인증 테스트
   - `tps-ticket-list.spec.ts`: 목록 및 필터링
   - `tps-ticket-create.spec.ts`: 티켓 생성
   - `tps-workflow.spec.ts`: 전체 워크플로우
   - `tps-permission.spec.ts`: 권한 테스트
3. Python 자동화 스크립트 작성 (`python/tps_ticket_screenshot.py`)

**핵심 원칙**: 실무에서는 완벽보다 실용성입니다. 가장 중요한 사용자 시나리오부터 시작하세요.
