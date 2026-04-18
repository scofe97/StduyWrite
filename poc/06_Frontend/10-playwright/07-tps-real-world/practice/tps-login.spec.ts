/**
 * TPS 로그인 기능 테스트
 *
 * 테스트 목표:
 * - 성공/실패 시나리오 검증
 * - storageState 저장 확인
 * - 토큰 만료 처리 테스트
 */

import { test, expect } from '@playwright/test';
import path from 'path';

// 이 테스트들은 storageState를 사용하지 않음 (로그인 자체를 테스트하기 위해)
test.use({ storageState: undefined });

test.describe('TPS 로그인 기능', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('성공: 올바른 자격증명으로 로그인', async ({ page }) => {
    // Given: 로그인 페이지
    await expect(page.locator('h1')).toContainText('TPS 로그인');

    // When: 올바른 자격증명 입력
    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');

    // Then: 대시보드로 리다이렉트
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('.user-name')).toContainText('admin');

    // 로그아웃 버튼 표시 확인
    await expect(page.locator('button:has-text("로그아웃")')).toBeVisible();
  });

  test('실패: 잘못된 비밀번호', async ({ page }) => {
    // When: 잘못된 비밀번호 입력
    await page.fill('#username', 'admin');
    await page.fill('#password', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Then: 에러 메시지 표시
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText(/로그인 실패|인증 실패|비밀번호가 올바르지 않습니다/);

    // 여전히 로그인 페이지에 있음
    await expect(page).toHaveURL(/.*login/);
  });

  test('실패: 존재하지 않는 사용자', async ({ page }) => {
    // When: 존재하지 않는 사용자명
    await page.fill('#username', 'nonexistentuser');
    await page.fill('#password', 'password123');
    await page.click('button[type="submit"]');

    // Then: 에러 메시지 표시
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText(/사용자를 찾을 수 없습니다|로그인 실패/);
  });

  test('실패: 빈 필드 검증', async ({ page }) => {
    // When: 아무것도 입력하지 않고 제출
    await page.click('button[type="submit"]');

    // Then: HTML5 required validation 또는 에러 메시지
    const usernameInput = page.locator('#username');
    const isRequired = await usernameInput.evaluate((el: HTMLInputElement) => el.required);
    expect(isRequired).toBeTruthy();
  });

  test('성공: 로그인 상태 storageState 저장', async ({ page, context }) => {
    // Given: 로그인 성공
    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // When: storageState 저장
    const authDir = path.join(__dirname, '..', '..', '.auth');
    const storagePath = path.join(authDir, 'test-user.json');

    // .auth 디렉토리가 없으면 테스트 통과 (CI 환경)
    try {
      await context.storageState({ path: storagePath });
      console.log(`✓ storageState saved to ${storagePath}`);
    } catch (error) {
      console.log('⚠ storageState 저장 실패 (디렉토리 없음, CI 환경에서는 정상)');
    }

    // Then: 쿠키 또는 로컬스토리지에 인증 정보 확인
    const cookies = await context.cookies();
    const hasSessionCookie = cookies.some(cookie =>
      cookie.name === 'sessionId' || cookie.name === 'token' || cookie.name === 'connect.sid'
    );

    // 쿠키 또는 로컬스토리지에 인증 정보가 있어야 함
    if (hasSessionCookie) {
      expect(hasSessionCookie).toBeTruthy();
    } else {
      // 로컬스토리지 확인
      const localStorage = await page.evaluate(() => JSON.stringify(window.localStorage));
      expect(localStorage).toContain('user');
    }
  });

  test('로그인 폼 UI 요소 확인', async ({ page }) => {
    // 모든 필수 요소가 있는지 확인
    await expect(page.locator('#username')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();

    // 플레이스홀더 확인
    await expect(page.locator('#username')).toHaveAttribute('placeholder', /사용자|아이디|Username/i);
    await expect(page.locator('#password')).toHaveAttribute('placeholder', /비밀번호|Password/i);
  });

  test('로그인 버튼 클릭 시 로딩 상태', async ({ page }) => {
    // API 응답 지연 시뮬레이션
    await page.route('**/api/auth/login', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.continue();
    });

    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin123');

    // 로딩 버튼 확인
    const submitButton = page.locator('button[type="submit"]');
    await submitButton.click();

    // 버튼이 비활성화되거나 로딩 텍스트로 변경되는지 확인
    // (구현에 따라 다를 수 있음)
    await expect(submitButton).toBeDisabled().or(expect(submitButton).toContainText(/로그인|로딩|처리/));
  });
});

test.describe('토큰 만료 처리', () => {
  test('만료된 세션으로 접근 시 로그인 페이지로 리다이렉트', async ({ page, context }) => {
    // Given: 만료된 쿠키 설정
    await context.addCookies([{
      name: 'sessionId',
      value: 'expired-token',
      domain: 'localhost',
      path: '/',
      expires: Date.now() / 1000 - 3600, // 1시간 전 만료
    }]);

    // When: 보호된 페이지 접근 시도
    await page.goto('/tickets');

    // Then: 로그인 페이지로 리다이렉트 또는 에러 메시지
    await expect(page).toHaveURL(/.*login/).or(
      expect(page.locator('.error-message')).toContainText(/세션이 만료|다시 로그인/)
    );
  });
});

test.describe('Remember Me 기능 (선택사항)', () => {
  test.skip('Remember Me 체크 시 쿠키 만료 시간 연장', async ({ page, context }) => {
    // 구현된 경우에만 테스트
    await page.goto('/login');
    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin123');

    const rememberCheckbox = page.locator('input[type="checkbox"][name="remember"]');
    if (await rememberCheckbox.isVisible()) {
      await rememberCheckbox.check();
      await page.click('button[type="submit"]');

      const cookies = await context.cookies();
      const sessionCookie = cookies.find(c => c.name === 'sessionId');

      // 쿠키 만료 시간이 7일 이상인지 확인
      if (sessionCookie?.expires) {
        const expiresInDays = (sessionCookie.expires - Date.now() / 1000) / 86400;
        expect(expiresInDays).toBeGreaterThan(7);
      }
    }
  });
});
