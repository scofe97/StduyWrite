import { test, expect } from '@playwright/test';

/**
 * Codegen으로 생성된 원본 코드 (수정 전)
 *
 * Playwright Codegen은 브라우저 작업을 녹화하여 테스트 코드를 자동 생성합니다.
 *
 * 실행 방법:
 * npx playwright codegen http://localhost:3002
 *
 * Codegen의 장점:
 * ✅ 빠른 프로토타이핑
 * ✅ 복잡한 사용자 플로우 캡처
 * ✅ 로케이터 아이디어 제공
 *
 * Codegen의 단점:
 * ❌ CSS 선택자 과다 사용 (깨지기 쉬움)
 * ❌ 불필요한 waitForTimeout 생성
 * ❌ 명확하지 않은 테스트 이름
 * ❌ 어설션 부족
 *
 * 이 파일은 Codegen의 출력물을 그대로 보여주며,
 * codegen-improved.spec.ts에서 개선된 버전을 확인할 수 있습니다.
 */

test('test', async ({ page }) => {
  // Codegen은 기본적으로 'test'라는 이름을 사용 (❌ 의미 없는 이름)

  // goto는 좋음 (✅)
  await page.goto('http://localhost:3002/login');

  // Codegen은 CSS 선택자를 자주 사용 (❌ 깨지기 쉬움)
  await page.locator('input[name="username"]').click();
  await page.locator('input[name="username"]').fill('admin');

  // 불필요한 클릭 액션 (이미 fill이 포커스를 줌)
  await page.locator('input[name="password"]').click();
  await page.locator('input[name="password"]').fill('admin123');

  // 버튼 클릭 - CSS 선택자 사용 (❌)
  await page.locator('button[type="submit"]').click();

  // Codegen은 때때로 불필요한 waitForTimeout 추가 (❌ 안티패턴)
  await page.waitForTimeout(1000);

  // URL 확인 - 어설션 있음 (✅)
  await expect(page).toHaveURL('http://localhost:3002/tickets');

  // 하지만 더 많은 어설션이 필요함 (❌ 부족한 검증)
});

test('recorded user flow', async ({ page }) => {
  // 또 다른 Codegen 예시: 티켓 생성 플로우

  await page.goto('http://localhost:3002/login');

  // 중복된 로그인 코드 (❌ 재사용 없음)
  await page.locator('#username').fill('admin');
  await page.locator('#password').fill('admin123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // 이건 괜찮음 - getByRole 사용 (✅)
  await page.getByRole('link', { name: 'New Ticket' }).click();

  // CSS 선택자로 복귀 (❌)
  await page.locator('#ticket-title').fill('Test Ticket');
  await page.locator('#ticket-description').fill('This is a test');

  // 드롭다운 선택 - 직접적인 선택자 (❌)
  await page.locator('select[name="priority"]').selectOption('high');

  // 제출
  await page.locator('button:has-text("Create")').click();

  // 너무 긴 대기 시간 (❌)
  await page.waitForTimeout(2000);

  // 텍스트 확인 - 하드코딩된 정확한 텍스트 (❌ 변경에 취약)
  await expect(page.locator('text=Ticket created successfully')).toBeVisible();
});

test('codegen navigation', async ({ page }) => {
  // Codegen은 여러 페이지 이동을 그대로 기록

  await page.goto('http://localhost:3002/');

  // 절대 URL 사용 (❌ 환경별 설정 불가)
  await page.goto('http://localhost:3002/login');

  await page.locator('[placeholder="Enter your username"]').fill('user123');
  await page.locator('[placeholder="Enter your password"]').fill('pass123');

  // 여러 방식의 선택자가 혼재 (❌ 일관성 없음)
  await page.click('button.submit-btn');

  await page.waitForURL('http://localhost:3002/dashboard');

  // 사이드바 메뉴 클릭
  await page.click('.sidebar >> text=Tickets');

  // 필터 적용
  await page.locator('#filter-status').selectOption('open');
  await page.locator('#filter-assignee').selectOption('me');

  // 검색
  await page.fill('[data-test="search-input"]', 'urgent');
  await page.press('[data-test="search-input"]', 'Enter');

  // 어설션 없음 (❌ 결과 검증 안 함)
});

test('codegen form interaction', async ({ page }) => {
  // 폼 입력 예시

  await page.goto('http://localhost:3002/tickets/new');

  // 여러 필드 입력 - 모두 CSS 선택자 (❌)
  await page.locator('#title').fill('Bug Report');
  await page.locator('#description').fill('Application crashes on startup');

  // 라디오 버튼
  await page.locator('input[name="type"][value="bug"]').check();

  // 체크박스
  await page.locator('input[name="notify-me"]').check();

  // 파일 업로드
  await page.setInputFiles('input[type="file"]', 'screenshot.png');

  // 날짜 선택
  await page.locator('input[type="date"]').fill('2024-12-31');

  // 제출 버튼
  await page.locator('button >> text=Submit').click();

  // 암묵적 대기 (❌)
  await page.waitForTimeout(500);

  // 성공 메시지 확인 - 취약한 선택자 (❌)
  await expect(page.locator('.alert.success')).toContainText('Success');
});

/**
 * Codegen 출력물의 주요 문제점 요약:
 *
 * 1. 선택자 품질
 *    - CSS 선택자 과다 사용 (#id, .class, [attr])
 *    - 구조 변경 시 쉽게 깨짐
 *    - getByRole, getByLabel 등 시맨틱 선택자 부족
 *
 * 2. 테스트 구조
 *    - 의미 없는 테스트 이름 ('test')
 *    - 재사용 가능한 헬퍼 함수 없음
 *    - beforeEach/afterEach 설정 없음
 *
 * 3. 대기/동기화
 *    - waitForTimeout() 과다 사용 (안티패턴)
 *    - 자동 대기 메커니즘 활용 부족
 *
 * 4. 어설션
 *    - 어설션 부족 (액션만 많고 검증은 적음)
 *    - 중간 상태 검증 없음
 *
 * 5. 유지보수성
 *    - 하드코딩된 값 (URL, 텍스트)
 *    - 환경 설정 분리 안 됨
 *    - Page Object Model 미적용
 *
 * 개선 방법은 codegen-improved.spec.ts 참조
 */
