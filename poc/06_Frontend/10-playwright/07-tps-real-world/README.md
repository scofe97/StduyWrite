# 07. TPS 실전 통합 (Real World Capstone)

Playwright를 실제 TPS 시스템에 적용하는 종합 실습 섹션입니다.

---

## 학습 구조

### 1. INVESTIGATE.md
소크라테스식 질문을 통한 탐구:
- 실제 환경 인증 처리 방법
- 동적 데이터 검증 전략
- 네트워크 인터셉션과 불안정한 API 대응
- 테스트 데이터 관리
- 복잡한 워크플로우 테스트
- CI/CD 통합
- 권한 기반 테스트

### 2. LEARN.md
실전 패턴과 Best Practices:
- storageState를 활용한 인증 관리
- global-setup.ts 패턴
- 동적 데이터 검증 (정규식, 유연한 assertion)
- API 모킹과 네트워크 제어
- Page Object Model 워크플로우
- 테스트 데이터 Setup/Teardown
- CI/CD 설정 (GitHub Actions)
- 권한 테스트 전략

### 3. practice/ 폴더
실습 테스트 파일:
- `tps-login.spec.ts`: 로그인 및 인증
- `tps-ticket-list.spec.ts`: 목록, 검색, 필터링
- `tps-ticket-create.spec.ts`: 티켓 생성
- `tps-workflow.spec.ts`: E2E 워크플로우
- `tps-permission.spec.ts`: 권한 테스트

### 4. python/ 폴더
Python 자동화 스크립트:
- `tps_ticket_screenshot.py`: 스크린샷 자동 캡처

---

## 실행 방법

### Mock 서버 테스트 (기본)

```bash
# Mock 서버는 자동 시작됨 (playwright.config.ts의 webServer)
npx playwright test 07-tps-real-world/practice

# 특정 테스트만 실행
npx playwright test tps-login.spec.ts
npx playwright test tps-workflow.spec.ts

# UI 모드
npx playwright test 07-tps-real-world/practice --ui

# 디버그 모드
npx playwright test tps-login.spec.ts --debug
```

### 실제 TPS 환경 테스트

1. `.env` 파일 설정:
```bash
cp .env.example .env

# .env 편집
TPS_BASE_URL=https://dev.console.trombone.okestro.cloud
TPS_USERNAME=your-username
TPS_PASSWORD=your-password
```

2. global-setup 생성:
```typescript
// global-setup.ts
import { chromium } from '@playwright/test';

async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(process.env.TPS_BASE_URL + '/login');
  await page.fill('#username', process.env.TPS_USERNAME);
  await page.fill('#password', process.env.TPS_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');

  await page.context().storageState({ path: '.auth/user.json' });
  await browser.close();
}

export default globalSetup;
```

3. playwright.config.ts 수정:
```typescript
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  use: {
    storageState: '.auth/user.json',
  },
  // ...
});
```

4. 테스트 실행:
```bash
npx playwright test 07-tps-real-world/practice --project=tps-real
```

### Python 스크립트 실행

```bash
cd 07-tps-real-world/practice/python

# 패키지 설치
pip install playwright
playwright install chromium

# Mock 서버 대상 (기본)
python tps_ticket_screenshot.py

# 실제 환경 대상
export TPS_BASE_URL=https://dev.console.trombone.okestro.cloud
export TPS_USERNAME=your-username
export TPS_PASSWORD=your-password
python tps_ticket_screenshot.py
```

---

## 테스트 파일 설명

### tps-login.spec.ts (인증)
- 성공/실패 시나리오
- storageState 저장 확인
- 토큰 만료 처리
- 로그인 폼 UI 검증

**주요 테스트:**
- ✅ 올바른 자격증명으로 로그인
- ❌ 잘못된 비밀번호
- ❌ 존재하지 않는 사용자
- 💾 storageState 저장

### tps-ticket-list.spec.ts (목록 및 검색)
- 티켓 목록 로드
- 검색 기능 (제목, ID)
- 필터링 (상태, 타입)
- 페이지네이션
- 정렬
- 동적 데이터 검증

**주요 테스트:**
- 📋 목록 로드 및 표시
- 🔍 검색 (제목, ID)
- 🎯 필터링 (상태, 타입)
- 📄 페이지네이션
- 🔄 정렬
- ⚠️ 에러 처리

### tps-ticket-create.spec.ts (티켓 생성)
- CICD/PMS/ITSM 타입 생성
- 필수 필드 검증
- 릴리즈 선택 (PMS)
- 폼 검증 에러
- 생성 취소

**주요 테스트:**
- ➕ CICD 티켓 생성
- ➕ PMS 티켓 (릴리즈 선택)
- ✅ 필수 필드 검증
- ❌ 검증 에러 시나리오
- 🔙 취소 플로우

### tps-workflow.spec.ts (E2E 워크플로우)
- 완전한 사용자 여정
- 다중 페이지 네비게이션
- 상태 전환
- 검색 + 페이지네이션 + 정렬 조합

**주요 시나리오:**
1. 생성 → 목록 확인 → 상세 보기
2. 수정 → 변경사항 검증
3. 필터링 → 상세 → 뒤로가기
4. 다중 페이지 네비게이션
5. 상태 전환 (접수 → 진행중 → 완료)

### tps-permission.spec.ts (권한)
- Admin vs User 차이
- 역할별 접근 제어
- 권한 경계 테스트
- UI 렌더링 차이

**주요 테스트:**
- 👑 관리자: 삭제 가능, 모든 티켓 수정
- 👤 일반 사용자: 삭제 불가, 자신의 티켓만
- 🚫 권한 없는 페이지 접근
- 🎨 역할별 메뉴 표시

---

## 디렉토리 구조

```
07-tps-real-world/
├── README.md                    # 이 파일
├── INVESTIGATE.md               # 소크라테스식 탐구 질문
├── LEARN.md                     # 실전 패턴 학습
└── practice/
    ├── tps-login.spec.ts        # 인증 테스트
    ├── tps-ticket-list.spec.ts  # 목록 및 검색
    ├── tps-ticket-create.spec.ts # 티켓 생성
    ├── tps-workflow.spec.ts     # E2E 워크플로우
    ├── tps-permission.spec.ts   # 권한 테스트
    └── python/
        └── tps_ticket_screenshot.py  # Python 자동화
```

---

## 주요 개념

### storageState (인증 상태 저장)
```typescript
// 로그인 후 상태 저장
await context.storageState({ path: '.auth/user.json' });

// 다음 테스트에서 재사용
const context = await browser.newContext({
  storageState: '.auth/user.json'
});
```

### 동적 데이터 검증
```typescript
// ❌ 취약: 정확한 값 매칭
await expect(page.locator('.ticket-id')).toHaveText('TICKET-001');

// ✅ 유연: 정규식 패턴
await expect(page.locator('.ticket-id')).toHaveText(/^(CICD|PMS)-\d+$/);
```

### API 모킹
```typescript
// API 응답 모킹
await page.route('**/api/tickets', async (route) => {
  await route.fulfill({
    status: 200,
    body: JSON.stringify({ tickets: [], total: 0 }),
  });
});
```

### POM (Page Object Model)
```typescript
class TicketListPage {
  constructor(private page: Page) {}

  async searchTicket(query: string) {
    await this.page.fill('input[type="search"]', query);
    await this.page.click('button:has-text("검색")');
  }
}
```

---

## CI/CD 통합

### GitHub Actions 예시
```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 실무 적용 체크리스트

### Phase 1: Mock 서버 기반 테스트
- [ ] 모든 테스트 파일 실행 성공
- [ ] 핵심 시나리오 커버리지 확인
- [ ] 테스트 안정성 검증 (여러 번 실행)

### Phase 2: 실제 환경 설정
- [ ] `.env` 파일 설정
- [ ] global-setup.ts 작성
- [ ] storageState 저장 확인
- [ ] 실제 환경 테스트 실행

### Phase 3: CI/CD 통합
- [ ] GitHub Actions 워크플로우 작성
- [ ] 테스트 실패 시 artifacts 업로드
- [ ] 선택적 테스트 실행 (태그 활용)

### Phase 4: 유지보수
- [ ] 불안정한(flaky) 테스트 수정
- [ ] 테스트 데이터 정리 전략
- [ ] 팀 협업 가이드 작성

---

## 문제 해결

### 로그인 실패
```bash
# storageState 파일 확인
cat .auth/user.json

# 직접 로그인 테스트
npx playwright test tps-login.spec.ts --headed
```

### 요소를 찾을 수 없음
```bash
# 디버그 모드로 실행
npx playwright test --debug

# 스크린샷 확인
ls test-results/
```

### 느린 테스트
```bash
# 특정 테스트만 실행
npx playwright test --grep "로그인"

# 병렬 실행 worker 수 조정
npx playwright test --workers=4
```

---

## 다음 단계

1. **INVESTIGATE.md 읽기**: 질문 중심 탐구
2. **LEARN.md 학습**: 실전 패턴 이해
3. **practice/ 실습**: 테스트 실행 및 수정
4. **Python 스크립트**: 자동화 확장

**핵심**: Mock 서버로 빠른 학습 → 실제 환경 적용!
