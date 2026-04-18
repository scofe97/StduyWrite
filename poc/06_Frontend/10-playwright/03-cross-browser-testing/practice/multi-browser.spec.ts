import { test, expect, type BrowserName } from '@playwright/test';

/**
 * 03-1. 멀티 브라우저 테스트
 *
 * Playwright는 Chromium, Firefox, WebKit(Safari) 세 가지 브라우저를 지원합니다.
 * playwright.config.ts에서 projects 설정으로 브라우저별 실행을 정의합니다.
 *
 * 실행 방법:
 * - 모든 브라우저: npx playwright test multi-browser.spec.ts
 * - 특정 브라우저: npx playwright test multi-browser.spec.ts --project=chromium
 */
test.describe('03-1. 멀티 브라우저 테스트', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  /**
   * 브라우저별 기본 렌더링 테스트
   * browserName fixture를 통해 현재 실행 중인 브라우저 확인 가능
   */
  test('모든 브라우저에서 로그인 페이지가 렌더링된다', async ({ page, browserName }) => {
    console.log(`Running on: ${browserName}`);

    // 로그인 페이지 핵심 요소 확인
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    await expect(page.getByLabel('아이디')).toBeVisible();
    await expect(page.getByLabel('비밀번호')).toBeVisible();
  });

  /**
   * 브라우저별 기능 동작 테스트
   * 실제 로그인 플로우가 모든 브라우저에서 동일하게 작동하는지 검증
   */
  test('모든 브라우저에서 로그인이 작동한다', async ({ page, browserName }) => {
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();

    // URL 변경 대기 및 검증
    await expect(page).toHaveURL(/.*tickets/);
    console.log(`✅ Login successful on ${browserName}`);
  });

  /**
   * 브라우저별 조건부 테스트
   * test.skip()을 사용하여 특정 브라우저에서만 실행하거나 건너뛸 수 있습니다.
   */
  test('WebKit에서만 실행되는 테스트', async ({ page, browserName }) => {
    // WebKit이 아닌 경우 건너뛰기
    test.skip(browserName !== 'webkit', 'WebKit 전용 테스트');

    await expect(page).toHaveURL(/.*login/);
    // WebKit 특화 동작 테스트
  });

  test('Firefox에서 건너뛰는 테스트', async ({ page, browserName }) => {
    // Firefox에서 알려진 이슈가 있는 경우 건너뛰기
    test.skip(browserName === 'firefox', 'Firefox에서 알려진 이슈');

    await page.getByLabel('아이디').fill('test');
    await expect(page.getByLabel('아이디')).toHaveValue('test');
  });

  /**
   * 시각적 회귀 테스트 (Visual Regression Testing)
   *
   * 브라우저별로 스크린샷을 캡처하고 비교합니다.
   * - 첫 실행: 기준 스크린샷 생성 (tests/multi-browser.spec.ts-snapshots/)
   * - 이후 실행: 기준 이미지와 비교
   * - 차이 발견: 테스트 실패 및 diff 이미지 생성
   *
   * 주의: 브라우저마다 렌더링이 다르므로 브라우저별 기준 이미지가 생성됩니다.
   * 예: login-page-chromium-darwin.png, login-page-firefox-darwin.png
   */
  test('로그인 페이지 시각적 스냅샷', async ({ page }) => {
    await expect(page).toHaveScreenshot('login-page.png', {
      // 최대 픽셀 차이 비율 (0.1 = 10%)
      maxDiffPixelRatio: 0.1,
    });
  });

  /**
   * 브라우저별 User-Agent 확인
   * 각 브라우저가 올바른 User-Agent를 전송하는지 검증
   */
  test('브라우저별 User-Agent 확인', async ({ page, browserName }) => {
    const userAgent = await page.evaluate(() => navigator.userAgent);
    console.log(`${browserName} User-Agent:`, userAgent);

    // 브라우저별 User-Agent 검증
    switch (browserName) {
      case 'chromium':
        expect(userAgent).toContain('Chrome');
        break;
      case 'firefox':
        expect(userAgent).toContain('Firefox');
        break;
      case 'webkit':
        expect(userAgent).toContain('Safari');
        break;
    }
  });

  /**
   * 브라우저별 CSS 속성 차이 테스트
   * 브라우저마다 CSS 렌더링이 다를 수 있으므로 검증
   */
  test('로그인 버튼 스타일 확인', async ({ page }) => {
    const button = page.getByRole('button', { name: '로그인' });

    // CSS 속성 확인
    const backgroundColor = await button.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );

    // 색상 값은 브라우저마다 다를 수 있으므로 존재 여부만 확인
    expect(backgroundColor).toBeTruthy();
  });
});
