import { test, expect } from '@playwright/test';

// 첫 번째 테스트: 페이지 탐색
test.describe('01-1. 첫 번째 테스트', () => {

  test('로그인 페이지에 접근할 수 있다', async ({ page }) => {
    await page.goto('/login');
    await expect(page).toHaveTitle(/TPS/);
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
  });

  test('로그인 폼 요소가 모두 존재한다', async ({ page }) => {
    await page.goto('/login');
    // 아이디 입력 필드
    await expect(page.getByLabel('아이디')).toBeVisible();
    // 비밀번호 입력 필드
    await expect(page.getByLabel('비밀번호')).toBeVisible();
    // 로그인 버튼
    await expect(page.getByRole('button', { name: '로그인' })).toBeEnabled();
  });

  test('잘못된 로그인 시 에러 메시지가 표시된다', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('아이디').fill('wrong');
    await page.getByLabel('비밀번호').fill('wrong');
    await page.getByRole('button', { name: '로그인' }).click();
    await expect(page.getByTestId('error-message')).toBeVisible();
    await expect(page.getByTestId('error-message')).toContainText('올바르지 않습니다');
  });

  test('올바른 로그인 시 티켓 목록으로 이동한다', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    // 로그인 후 /tickets로 리다이렉트
    await expect(page).toHaveURL(/.*tickets/);
  });
});

// Assertion 연습
test.describe('01-2. Assertion 패턴', () => {

  test('페이지 제목 검증', async ({ page }) => {
    await page.goto('/login');
    // 정확한 제목 매칭
    await expect(page).toHaveTitle(/TPS/);
  });

  test('URL 검증 패턴', async ({ page }) => {
    await page.goto('/login');
    await expect(page).toHaveURL(/.*login/);
    // 문자열 매칭도 가능
    await expect(page).toHaveURL(/localhost/);
  });

  test('요소 상태 검증', async ({ page }) => {
    await page.goto('/login');
    const loginBtn = page.getByRole('button', { name: '로그인' });

    // 가시성
    await expect(loginBtn).toBeVisible();
    // 활성화 상태
    await expect(loginBtn).toBeEnabled();
    // 텍스트 내용
    await expect(loginBtn).toHaveText('로그인');
  });

  test('입력 필드 값 검증', async ({ page }) => {
    await page.goto('/login');
    const usernameInput = page.getByLabel('아이디');

    // 초기 값은 비어있음
    await expect(usernameInput).toHaveValue('');

    // 값 입력 후 검증
    await usernameInput.fill('testuser');
    await expect(usernameInput).toHaveValue('testuser');
  });

  test('요소 개수 검증', async ({ page }) => {
    await page.goto('/login');
    // input 요소 개수 확인 (username + password)
    const inputs = page.locator('input[type="text"], input[type="password"]');
    await expect(inputs).toHaveCount(2);
  });
});
