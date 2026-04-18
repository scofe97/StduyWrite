import { test, expect } from '@playwright/test';

// Hook 실행 순서 데모
test.describe('01-3. Hook 실행 순서', () => {
  // describe 레벨 Hook - 모든 테스트 전/후 1번씩 실행
  test.beforeAll(async () => {
    console.log('  ⬇️ beforeAll: 전체 테스트 시작 전 1회 실행');
  });

  test.afterAll(async () => {
    console.log('  ⬆️ afterAll: 전체 테스트 완료 후 1회 실행');
  });

  // 테스트 레벨 Hook - 각 테스트 전/후 매번 실행
  test.beforeEach(async ({ page }) => {
    console.log('    → beforeEach: 각 테스트 시작 전 실행');
    // 공통 설정: 로그인 페이지로 이동
    await page.goto('/login');
  });

  test.afterEach(async ({ page }) => {
    console.log('    ← afterEach: 각 테스트 완료 후 실행');
  });

  test('테스트 A', async ({ page }) => {
    console.log('      ✅ 테스트 A 실행');
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
  });

  test('테스트 B', async ({ page }) => {
    console.log('      ✅ 테스트 B 실행');
    await expect(page.getByLabel('아이디')).toBeVisible();
  });

  test('테스트 C', async ({ page }) => {
    console.log('      ✅ 테스트 C 실행');
    await expect(page.getByLabel('비밀번호')).toBeVisible();
  });
});

// 중첩 describe의 Hook 순서
test.describe('01-4. 중첩 Hook 순서', () => {
  test.beforeEach(async ({ page }) => {
    console.log('  [외부] beforeEach');
    await page.goto('/login');
  });

  test.describe('내부 그룹', () => {
    test.beforeEach(async ({ page }) => {
      console.log('  [내부] beforeEach');
      // 외부 beforeEach 이후에 실행됨
    });

    test('중첩 테스트', async ({ page }) => {
      // 실행 순서: 외부 beforeEach → 내부 beforeEach → 테스트
      console.log('  [내부] 테스트 실행');
      await expect(page).toHaveURL(/.*login/);
    });
  });
});

// 로그인 상태 유지 패턴
test.describe('01-5. 로그인 후 테스트', () => {
  test.beforeEach(async ({ page }) => {
    // 매 테스트 전 로그인 수행
    await page.goto('/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await page.waitForURL(/.*tickets/);
  });

  test('로그인 후 티켓 목록이 표시된다', async ({ page }) => {
    await expect(page.getByTestId('ticket-table')).toBeVisible();
  });

  test('로그인 후 페이지 헤더가 보인다', async ({ page }) => {
    await expect(page.getByTestId('page-header')).toBeVisible();
  });
});
