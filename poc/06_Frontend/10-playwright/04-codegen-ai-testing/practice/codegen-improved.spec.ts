import { test, expect } from '@playwright/test';

/**
 * Codegen 결과를 개선한 코드
 *
 * codegen-output.spec.ts의 문제점을 개선한 버전입니다.
 *
 * 개선 사항:
 * ✅ CSS 선택자 → getByRole/getByLabel 등 시맨틱 선택자
 * ✅ 명확한 테스트 이름
 * ✅ 적절한 어설션 추가
 * ✅ 재사용 가능한 헬퍼 함수
 * ✅ waitForTimeout 제거 → 자동 대기
 * ✅ 환경 변수 분리
 */

/**
 * 재사용 가능한 헬퍼 함수
 */
const loginAsAdmin = async (page) => {
  await page.goto('/login');
  await page.getByLabel('아이디').fill('admin');
  await page.getByLabel('비밀번호').fill('admin123');
  await page.getByRole('button', { name: '로그인' }).click();

  // 자동 대기: Playwright가 URL 변경을 기다림
  await expect(page).toHaveURL(/.*tickets/);
};

test.describe('로그인 플로우', () => {
  /**
   * 개선 전: test('test', async ({ page }) => { ... })
   * 개선 후: 명확한 테스트 이름
   */
  test('관리자 계정으로 로그인 성공', async ({ page }) => {
    // 개선 전: await page.goto('http://localhost:3002/login');
    // 개선 후: baseURL 사용 (playwright.config.ts 설정)
    await page.goto('/login');

    // 개선 전: await page.locator('input[name="username"]').fill('admin');
    // 개선 후: getByLabel 사용 (접근성 좋음, 안정적)
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');

    // 개선 전: await page.locator('button[type="submit"]').click();
    // 개선 후: getByRole 사용
    await page.getByRole('button', { name: '로그인' }).click();

    // 개선 전: await page.waitForTimeout(1000); (❌ 안티패턴)
    // 개선 후: 자동 대기 (Playwright가 네비게이션 완료를 기다림)

    // URL 검증 (정규식 사용으로 유연성 확보)
    await expect(page).toHaveURL(/.*tickets/);

    // 개선: 추가 어설션으로 페이지 로드 확인
    await expect(page.getByTestId('ticket-table')).toBeVisible();
    await expect(page.getByRole('heading', { name: '티켓 목록' })).toBeVisible();
  });

  test('잘못된 비밀번호로 로그인 실패', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('wrongpassword');
    await page.getByRole('button', { name: '로그인' }).click();

    // 에러 메시지 확인
    await expect(page.getByRole('alert')).toContainText(/로그인 실패|Invalid/i);

    // 여전히 로그인 페이지에 있는지 확인
    await expect(page).toHaveURL(/.*login/);
  });

  test('빈 필드로 로그인 시도', async ({ page }) => {
    await page.goto('/login');

    // 아무것도 입력하지 않고 제출
    await page.getByRole('button', { name: '로그인' }).click();

    // HTML5 validation 또는 커스텀 validation 확인
    const usernameInput = page.getByLabel('아이디');
    const isInvalid = await usernameInput.evaluate((el: HTMLInputElement) =>
      !el.validity.valid
    );
    expect(isInvalid).toBe(true);
  });
});

test.describe('티켓 생성 플로우', () => {
  // beforeEach로 반복 코드 제거
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('새 티켓 생성 성공', async ({ page }) => {
    // 개선 전: await page.getByRole('link', { name: 'New Ticket' }).click();
    // 개선 후: 한국어 로케일 고려
    await page.getByRole('link', { name: /새 티켓|New Ticket/i }).click();

    // 개선 전: await page.locator('#ticket-title').fill('Test Ticket');
    // 개선 후: getByLabel 사용
    await page.getByLabel('제목').fill('버그 리포트: 로그인 오류');
    await page.getByLabel('내용').fill('로그인 시 간헐적으로 오류 발생');

    // 개선 전: await page.locator('select[name="priority"]').selectOption('high');
    // 개선 후: getByLabel 사용
    await page.getByLabel('우선순위').selectOption('높음');

    // 개선 전: await page.locator('button:has-text("Create")').click();
    // 개선 후: getByRole 사용
    await page.getByRole('button', { name: /생성|Create/i }).click();

    // 개선 전: await page.waitForTimeout(2000); (❌)
    // 개선 후: 자동 대기

    // 개선 전: 단순 텍스트 확인
    // 개선 후: role="alert" 사용 + 정규식
    await expect(page.getByRole('alert')).toContainText(/성공|success/i);

    // 추가 검증: 생성된 티켓이 목록에 보이는지
    await expect(page.getByText('버그 리포트: 로그인 오류')).toBeVisible();
  });

  test('필수 필드 없이 티켓 생성 시도', async ({ page }) => {
    await page.getByRole('link', { name: /새 티켓/i }).click();

    // 제목만 입력하고 제출
    await page.getByLabel('제목').fill('제목만 입력');
    await page.getByRole('button', { name: /생성/i }).click();

    // Validation 메시지 확인
    await expect(page.getByText(/내용을 입력|required/i)).toBeVisible();
  });
});

test.describe('검색 및 필터링', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('상태별 티켓 필터링', async ({ page }) => {
    // 개선 전: await page.locator('#filter-status').selectOption('open');
    // 개선 후: getByLabel 또는 getByRole 사용
    await page.getByLabel('상태 필터').selectOption('진행중');

    // 자동 대기: Playwright가 필터 결과 로딩을 기다림

    // 개선: 필터링 결과 검증
    const tickets = page.getByTestId('ticket-row');
    const count = await tickets.count();
    expect(count).toBeGreaterThan(0);

    // 모든 티켓이 '진행중' 상태인지 확인
    const statuses = await tickets.allTextContents();
    statuses.forEach(status => {
      expect(status).toContain('진행중');
    });
  });

  test('키워드로 티켓 검색', async ({ page }) => {
    // 개선 전: await page.fill('[data-test="search-input"]', 'urgent');
    // 개선 후: getByPlaceholder 또는 getByLabel 사용
    const searchInput = page.getByPlaceholder('티켓 검색...');
    await searchInput.fill('긴급');

    // 개선 전: await page.press('[data-test="search-input"]', 'Enter');
    // 개선 후: 동일하지만 더 명확한 선택자
    await searchInput.press('Enter');

    // 개선: 검색 결과 검증
    await expect(page.getByTestId('ticket-table')).toBeVisible();

    // 검색어가 결과에 포함되는지 확인
    const results = await page.getByTestId('ticket-row').allTextContents();
    expect(results.some(text => text.includes('긴급'))).toBe(true);
  });
});

test.describe('폼 인터랙션 (개선)', () => {
  test('티켓 생성 폼의 모든 필드 타입', async ({ page }) => {
    await loginAsAdmin(page);
    await page.getByRole('link', { name: /새 티켓/i }).click();

    // 텍스트 입력
    await page.getByLabel('제목').fill('복합 폼 테스트');
    await page.getByLabel('내용').fill('모든 필드 타입 테스트');

    // 셀렉트 박스
    await page.getByLabel('우선순위').selectOption('높음');

    // 라디오 버튼
    // 개선 전: await page.locator('input[name="type"][value="bug"]').check();
    // 개선 후: getByLabel 사용
    await page.getByLabel('버그').check();
    expect(await page.getByLabel('버그').isChecked()).toBe(true);

    // 체크박스
    // 개선 전: await page.locator('input[name="notify-me"]').check();
    // 개선 후: getByLabel 사용
    await page.getByLabel('알림 받기').check();

    // 날짜 선택
    // 개선 전: await page.locator('input[type="date"]').fill('2024-12-31');
    // 개선 후: getByLabel 사용
    await page.getByLabel('마감일').fill('2024-12-31');

    // 파일 업로드 (실제 파일 없이 테스트하려면 mock 필요)
    // await page.getByLabel('첨부파일').setInputFiles('test.png');

    // 제출
    await page.getByRole('button', { name: /생성/i }).click();

    // 성공 검증
    await expect(page.getByRole('alert')).toContainText(/성공/i);
  });
});

/**
 * 에러 처리 개선
 */
test.describe('에러 핸들링', () => {
  test('네트워크 오류 처리', async ({ page }) => {
    // API 요청을 가로채서 에러 응답 시뮬레이션
    await page.route('**/api/login', route => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    await page.goto('/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();

    // 에러 메시지 확인
    await expect(page.getByRole('alert')).toContainText(/오류가 발생|error/i);
  });

  test('타임아웃 처리', async ({ page }) => {
    // 느린 응답 시뮬레이션
    await page.route('**/api/tickets', async route => {
      await new Promise(resolve => setTimeout(resolve, 5000));
      await route.continue();
    });

    await loginAsAdmin(page);

    // 로딩 인디케이터 확인
    await expect(page.getByTestId('loading-spinner')).toBeVisible();
  });
});

/**
 * 개선 요약:
 *
 * 1. 선택자 품질
 *    ✅ getByRole, getByLabel, getByPlaceholder 우선 사용
 *    ✅ CSS 선택자는 최후의 수단
 *    ✅ data-testid는 특별한 경우에만 사용
 *
 * 2. 테스트 구조
 *    ✅ describe로 그룹화
 *    ✅ beforeEach로 반복 코드 제거
 *    ✅ 명확한 테스트 이름
 *    ✅ 헬퍼 함수 활용
 *
 * 3. 대기/동기화
 *    ✅ waitForTimeout 완전 제거
 *    ✅ Playwright 자동 대기 활용
 *    ✅ 명시적 대기는 expect로 처리
 *
 * 4. 어설션
 *    ✅ 각 액션 후 상태 검증
 *    ✅ 중간 상태 확인
 *    ✅ 다양한 어설션 메서드 활용
 *
 * 5. 유지보수성
 *    ✅ baseURL 환경 변수 사용
 *    ✅ 정규식으로 유연성 확보
 *    ✅ 에러 케이스 고려
 *    ✅ 접근성 고려 (screen reader 친화적)
 */
