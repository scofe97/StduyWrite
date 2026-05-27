import { test, expect, type Locator } from '@playwright/test';

/**
 * 04-3. 로케이터 폴백 전략
 *
 * 로케이터 선택 우선순위:
 * 1순위: getByRole, getByLabel (접근성 기반 - 가장 안정적)
 * 2순위: getByPlaceholder, getByText
 * 3순위: data-testid (테스트 전용 속성)
 * 4순위: CSS 선택자 (.class, #id)
 * 5순위: XPath (최후의 수단)
 *
 * 폴백 전략: 우선순위가 높은 로케이터부터 시도하고, 실패 시 다음 순위로 이동
 */

/**
 * 다중 로케이터 폴백 헬퍼 함수
 * 여러 전략을 순차적으로 시도하여 첫 번째로 발견된 요소 반환
 */
async function findElementWithFallback(
  page: any,
  strategies: (() => Locator)[]
): Promise<Locator> {
  for (const strategy of strategies) {
    const locator = strategy();
    try {
      // 요소가 존재하는지 확인 (타임아웃 짧게 설정)
      await locator.waitFor({ timeout: 2000 });
      console.log('✅ 로케이터 성공:', locator.toString());
      return locator;
    } catch (error) {
      console.log('❌ 로케이터 실패, 다음 전략 시도...');
      continue;
    }
  }
  throw new Error('모든 로케이터 전략 실패');
}

test.describe('04-3. 로케이터 폴백 전략', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  /**
   * 우선순위 1: getByRole (가장 권장)
   * - 접근성(a11y) 기반
   * - screen reader와 동일한 방식
   * - 구조 변경에 강함
   */
  test('1순위: getByRole - 로그인 버튼', async ({ page }) => {
    const button = page.getByRole('button', { name: '로그인' });

    await expect(button).toBeVisible();
    console.log('✅ getByRole로 버튼 찾기 성공');

    // Role 종류: button, link, textbox, heading, checkbox, radio 등
    const usernameInput = page.getByRole('textbox', { name: '아이디' });
    await expect(usernameInput).toBeVisible();
  });

  /**
   * 우선순위 1-2: getByLabel (폼 요소에 적합)
   * - <label> 태그와 연결된 입력 필드
   * - 접근성 좋음
   * - 라벨 텍스트 변경 시만 영향받음
   */
  test('1순위: getByLabel - 입력 필드', async ({ page }) => {
    const usernameInput = page.getByLabel('아이디');
    const passwordInput = page.getByLabel('비밀번호');

    await usernameInput.fill('testuser');
    await passwordInput.fill('testpass');

    await expect(usernameInput).toHaveValue('testuser');
    await expect(passwordInput).toHaveValue('testpass');

    console.log('✅ getByLabel로 입력 필드 찾기 성공');
  });

  /**
   * 우선순위 2: getByPlaceholder
   * - placeholder 속성 기반
   * - 입력 필드에 적합
   */
  test('2순위: getByPlaceholder - 검색창', async ({ page }) => {
    // 로그인 후 검색창 테스트를 위해 먼저 로그인
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);

    // placeholder로 검색창 찾기
    const searchInput = page.getByPlaceholder('티켓 검색...');
    await expect(searchInput).toBeVisible();

    console.log('✅ getByPlaceholder로 검색창 찾기 성공');
  });

  /**
   * 우선순위 2-2: getByText
   * - 텍스트 콘텐츠 기반
   * - 링크, 버튼, 헤딩에 적합
   */
  test('2순위: getByText - 링크/제목', async ({ page }) => {
    // 정확한 텍스트 매칭
    const exactText = page.getByText('로그인', { exact: true });

    // 부분 매칭 (기본)
    const partialText = page.getByText('로그');

    // 정규식
    const regexText = page.getByText(/로그인|Login/i);

    await expect(regexText).toBeVisible();
    console.log('✅ getByText로 텍스트 찾기 성공');
  });

  /**
   * 우선순위 3: getByTestId
   * - data-testid 속성 기반
   * - 테스트 전용으로 추가한 속성
   * - 비즈니스 로직과 분리됨
   */
  test('3순위: getByTestId - 테스트 전용 속성', async ({ page }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);

    // data-testid 사용
    const ticketTable = page.getByTestId('ticket-table');
    await expect(ticketTable).toBeVisible();

    console.log('✅ getByTestId로 요소 찾기 성공');

    // 팁: data-testid는 일관된 네이밍 규칙 사용
    // 예: {component}-{element}-{descriptor}
    // ticket-list-table, user-profile-avatar, etc.
  });

  /**
   * 우선순위 4: CSS 선택자
   * - 클래스, ID, 속성 선택자
   * - 구조 변경에 취약
   * - 다른 방법이 없을 때만 사용
   */
  test('4순위: CSS 선택자 - 최후의 수단', async ({ page }) => {
    // ID 선택자
    const byId = page.locator('#username');

    // 클래스 선택자
    const byClass = page.locator('.login-form');

    // 속성 선택자
    const byAttribute = page.locator('[name="username"]');

    // 복합 선택자
    const complex = page.locator('form.login-form input[type="text"]');

    console.log('⚠️  CSS 선택자 사용 - 다른 방법이 없는 경우에만 권장');
  });

  /**
   * 우선순위 5: XPath
   * - XML Path Language
   * - 매우 강력하지만 읽기 어려움
   * - 정말 마지막 수단
   */
  test('5순위: XPath - 정말 최후의 수단', async ({ page }) => {
    // XPath 예시
    const byXPath = page.locator('xpath=//button[contains(text(), "로그인")]');

    // 복잡한 XPath
    const complexXPath = page.locator(
      'xpath=//form[@class="login-form"]//input[@type="password"]'
    );

    console.log('⚠️  XPath 사용 - 정말 다른 방법이 없을 때만');
  });

  /**
   * 실전: 폴백 전략 적용
   * 여러 로케이터를 순차적으로 시도
   */
  test('폴백 전략 실전 적용 - 로그인 버튼 찾기', async ({ page }) => {
    const loginButton = await findElementWithFallback(page, [
      // 1순위: getByRole (가장 안정적)
      () => page.getByRole('button', { name: '로그인' }),

      // 2순위: getByText
      () => page.getByText('로그인', { exact: true }),

      // 3순위: data-testid
      () => page.getByTestId('login-button'),

      // 4순위: CSS 선택자
      () => page.locator('button[type="submit"]'),

      // 5순위: XPath
      () => page.locator('xpath=//button[contains(text(), "로그인")]'),
    ]);

    await expect(loginButton).toBeVisible();
    console.log('✅ 폴백 전략으로 로그인 버튼 찾기 성공');
  });

  /**
   * 동적 컨텐츠: 여러 전략 동시 시도
   */
  test('동적 컨텐츠 - 로딩 후 나타나는 요소', async ({ page }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();

    // 티켓 테이블이 로딩될 때까지 대기 (여러 전략 시도)
    const ticketTable = await findElementWithFallback(page, [
      () => page.getByRole('table', { name: '티켓 목록' }),
      () => page.getByTestId('ticket-table'),
      () => page.locator('table.tickets'),
    ]);

    await expect(ticketTable).toBeVisible();
  });

  /**
   * 체이닝: 여러 로케이터 조합
   */
  test('로케이터 체이닝 - 중첩된 요소', async ({ page }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);

    // 테이블 안의 첫 번째 행의 제목 셀 찾기
    const table = page.getByTestId('ticket-table');
    const firstRow = table.locator('tbody tr').first();
    const titleCell = firstRow.locator('td').nth(1);

    await expect(titleCell).toBeVisible();

    console.log('✅ 로케이터 체이닝 성공');
  });

  /**
   * 필터링: 여러 요소 중 특정 조건 만족하는 요소 찾기
   */
  test('로케이터 필터링 - 특정 조건 만족하는 요소', async ({ page }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);

    // 모든 티켓 행 중에서 '긴급' 상태인 행만 필터링
    const urgentTickets = page
      .getByTestId('ticket-row')
      .filter({ hasText: '긴급' });

    const count = await urgentTickets.count();
    console.log(`긴급 티켓 개수: ${count}`);

    if (count > 0) {
      await expect(urgentTickets.first()).toBeVisible();
    }
  });

  /**
   * 로케이터 조합: AND/OR 조건
   */
  test('로케이터 조합 - 복잡한 조건', async ({ page }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);

    // '긴급' 텍스트를 포함하면서 특정 클래스를 가진 요소
    const urgentHighPriority = page.locator('.priority-high').filter({
      hasText: '긴급'
    });

    // 또는 여러 조건 동시에
    const specificTicket = page
      .getByTestId('ticket-row')
      .filter({ hasText: '버그' })
      .filter({ hasText: '진행중' });

    const count = await specificTicket.count();
    console.log(`진행중인 버그 티켓 개수: ${count}`);
  });
});

/**
 * 로케이터 선택 가이드 요약
 *
 * ✅ 항상 우선 시도할 것:
 * 1. getByRole - 접근성 기반, 가장 안정적
 * 2. getByLabel - 폼 요소에 최적
 * 3. getByPlaceholder - 입력 필드
 * 4. getByText - 콘텐츠 기반
 *
 * ⚠️  주의해서 사용:
 * 5. getByTestId - 테스트 전용, 프로덕션 코드에 영향
 * 6. CSS 선택자 - 구조 변경에 취약
 *
 * ❌ 피할 것:
 * 7. XPath - 읽기 어렵고 유지보수 힘듦
 *
 * 💡 팁:
 * - 폴백 전략: 여러 방법을 순차적으로 시도
 * - 체이닝: 복잡한 DOM 구조 탐색
 * - 필터링: 여러 요소 중 특정 조건 만족하는 요소 찾기
 * - 항상 접근성(a11y)을 고려한 로케이터 우선 사용
 */
