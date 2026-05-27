import { test, expect, chromium } from '@playwright/test';

/**
 * Playwright Tracing & Trace Viewer 데모
 *
 * Tracing 기능:
 * - 테스트 실행 과정을 상세히 기록
 * - 스크린샷, 스냅샷, 네트워크 요청, 소스 코드 포함
 * - 실패 원인 디버깅에 유용
 *
 * Trace Viewer:
 * - npx playwright show-trace test-results/traces/[file].zip
 * - 타임라인, DOM 스냅샷, 네트워크 요청을 시각적으로 확인
 */

test.describe('05-3. Tracing & Trace Viewer', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/login');
  });

  /**
   * 기본 Tracing 사용법
   * - context.tracing.start()로 추적 시작
   * - context.tracing.stop()으로 추적 종료 및 저장
   */
  test('기본 Trace 기록', async ({ browser }) => {
    const context = await browser.newContext();

    // Tracing 시작
    await context.tracing.start({
      screenshots: true,    // 각 액션마다 스크린샷 촬영
      snapshots: true,      // DOM 스냅샷 저장 (Before/After)
      sources: true         // 소스 코드 위치 기록
    });

    const page = await context.newPage();
    await page.goto('http://localhost:3002/login');

    // 로그인 과정
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');

    // 티켓 목록으로 이동
    await page.waitForURL('**/tickets');
    await expect(page.locator('h1')).toHaveText('티켓 목록');

    // Tracing 종료 및 저장
    await context.tracing.stop({
      path: 'test-results/traces/basic-trace.zip'
    });

    await context.close();
  });

  /**
   * 스크린샷과 스냅샷 옵션 비교
   *
   * screenshots: true
   * - 각 액션마다 실제 화면 캡처
   * - 시각적 변화 확인 가능
   *
   * snapshots: true
   * - DOM 구조 저장 (Before/After)
   * - 요소 검사 가능
   */
  test('스크린샷과 스냅샷 비교', async ({ browser }) => {
    const context = await browser.newContext();

    await context.tracing.start({
      screenshots: true,   // 스크린샷 활성화
      snapshots: true      // 스냅샷 활성화
    });

    const page = await context.newPage();
    await page.goto('http://localhost:3002/login');

    // 여러 단계의 상호작용
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');

    // 검색 필터 사용
    await page.waitForURL('**/tickets');
    await page.fill('input[placeholder*="검색"]', 'CICD');
    await page.click('button:has-text("검색")');

    await context.tracing.stop({
      path: 'test-results/traces/screenshots-snapshots.zip'
    });

    await context.close();
  });

  /**
   * 실패 시에만 Trace 저장
   * - 정상 케이스는 저장하지 않아 스토리지 절약
   * - 실패 케이스만 디버깅용으로 저장
   */
  test('실패 시에만 Trace 저장', async ({ browser }) => {
    const context = await browser.newContext();
    let testFailed = false;

    try {
      await context.tracing.start({
        screenshots: true,
        snapshots: true,
        sources: true
      });

      const page = await context.newPage();
      await page.goto('http://localhost:3002/login');

      // 의도적으로 실패하는 로그인
      await page.fill('input[name="username"]', 'wronguser');
      await page.fill('input[name="password"]', 'wrongpass');
      await page.click('button[type="submit"]');

      // 이 부분에서 실패할 것임
      await expect(page.locator('.alert-error')).toContainText('로그인 실패');

      testFailed = false; // 예상대로 실패 메시지 출력됨
    } catch (error) {
      testFailed = true;
      throw error; // 테스트 실패로 전파
    } finally {
      // 실패한 경우에만 저장
      if (testFailed) {
        await context.tracing.stop({
          path: 'test-results/traces/failure-trace.zip'
        });
      } else {
        await context.tracing.stop();
      }
      await context.close();
    }
  });

  /**
   * API 요청 추적
   * - 네트워크 요청이 trace에 자동으로 기록됨
   * - Request/Response 헤더 및 바디 확인 가능
   */
  test('네트워크 요청 Trace', async ({ browser }) => {
    const context = await browser.newContext();

    await context.tracing.start({
      screenshots: true,
      snapshots: true,
      sources: true
    });

    const page = await context.newPage();

    // API 요청이 발생하는 시나리오
    await page.goto('http://localhost:3002/login');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');

    // 로그인 API 호출 발생
    await page.click('button[type="submit"]');

    // 티켓 목록 API 호출 대기
    await page.waitForResponse(response =>
      response.url().includes('/api/tickets') && response.status() === 200
    );

    // 티켓 생성 페이지로 이동 (추가 API 호출)
    await page.click('a[href="/tickets/create/cicd"]');
    await page.waitForURL('**/tickets/create/cicd');

    // Trace에 모든 네트워크 요청이 기록됨:
    // - POST /api/login
    // - GET /api/tickets
    // - GET /api/cicd/data

    await context.tracing.stop({
      path: 'test-results/traces/network-trace.zip'
    });

    await context.close();
  });

  /**
   * Trace 옵션 상세 설명
   */
  test('Trace 옵션 비교', async ({ browser }) => {
    const context = await browser.newContext();

    await context.tracing.start({
      // screenshots: true
      // - 각 액션마다 스크린샷 캡처
      // - 파일 크기 증가
      // - 시각적 변화 확인 가능
      screenshots: true,

      // snapshots: true
      // - DOM 구조 저장 (Before/After)
      // - 요소 검사 가능
      // - 파일 크기 증가
      snapshots: true,

      // sources: true
      // - 테스트 코드 위치 기록
      // - 어느 줄에서 액션이 발생했는지 확인
      // - 파일 크기에 영향 적음
      sources: true
    });

    const page = await context.newPage();
    await page.goto('http://localhost:3002/tickets');

    // 여러 액션 수행
    await page.click('.ticket-row:first-child');
    await page.click('button:has-text("상세보기")');

    await context.tracing.stop({
      path: 'test-results/traces/options-comparison.zip'
    });

    await context.close();
  });

  /**
   * 프로덕션 권장 설정
   * - CI 환경에서는 실패 시에만 저장
   * - playwright.config.ts에서 설정 가능
   */
  test('프로덕션 권장 Trace 설정', async ({ browser }) => {
    const context = await browser.newContext();

    // CI 환경에서는 on-first-retry 모드 권장
    // playwright.config.ts에서 설정:
    // trace: 'on-first-retry'

    await context.tracing.start({
      screenshots: true,   // 필수: 실패 원인 파악에 중요
      snapshots: true,     // 필수: DOM 구조 확인
      sources: false       // 선택: 소스 코드는 CI에서 불필요할 수 있음
    });

    const page = await context.newPage();
    await page.goto('http://localhost:3002/tickets');

    // 일반적인 테스트 시나리오
    await page.fill('input[placeholder*="검색"]', 'CICD');
    await page.click('button:has-text("검색")');
    await expect(page.locator('.ticket-row')).toHaveCount(3);

    await context.tracing.stop({
      path: 'test-results/traces/production-recommended.zip'
    });

    await context.close();
  });
});

/**
 * Trace Viewer 사용법
 *
 * 1. Trace 파일 열기:
 *    npx playwright show-trace test-results/traces/basic-trace.zip
 *
 * 2. Trace Viewer 기능:
 *    - Timeline: 액션 순서 및 시간 확인
 *    - Screenshots: 각 단계의 스크린샷
 *    - Before/After: DOM 스냅샷 비교
 *    - Network: API 요청/응답 확인
 *    - Console: 콘솔 로그
 *    - Source: 테스트 코드 위치
 *
 * 3. CI 통합:
 *    - trace.playwright.dev에 업로드 가능
 *    - 팀원과 공유하여 실패 원인 분석
 */
