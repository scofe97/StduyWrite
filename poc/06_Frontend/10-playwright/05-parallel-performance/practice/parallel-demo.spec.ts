import { test, expect } from '@playwright/test';

/**
 * 05-1. 병렬 실행 데모
 *
 * Playwright는 기본적으로 여러 워커(worker)를 사용하여 테스트를 병렬로 실행합니다.
 *
 * 병렬 실행 모드:
 * 1. 파일 레벨 병렬 (기본): 각 테스트 파일이 독립적인 워커에서 실행
 * 2. 테스트 레벨 병렬: describe.configure({ mode: 'parallel' })
 *
 * 설정 (playwright.config.ts):
 * - workers: 동시 실행 워커 수 (기본: CPU 코어 수의 50%)
 * - fullyParallel: true → 모든 테스트를 병렬 실행
 *
 * 실행 방법:
 * - 병렬 실행 (기본): npx playwright test parallel-demo.spec.ts
 * - 순차 실행: npx playwright test parallel-demo.spec.ts --workers=1
 * - 워커 수 지정: npx playwright test parallel-demo.spec.ts --workers=4
 */

/**
 * describe.configure()를 사용하여 병렬 모드 설정
 * 이 describe 블록 내의 모든 테스트가 병렬로 실행됩니다.
 */
test.describe('05-1. 병렬 실행 데모', () => {
  // 병렬 모드 활성화
  test.describe.configure({ mode: 'parallel' });

  /**
   * 각 테스트는 독립적인 브라우저 컨텍스트에서 실행됩니다.
   * 워커 정보는 test.info()를 통해 확인할 수 있습니다.
   */
  test('테스트 1: 로그인 페이지 로드', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 1 시작`);
    const startTime = Date.now();

    await page.goto('/login');
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();

    const duration = Date.now() - startTime;
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 1 완료 (${duration}ms)`);
  });

  test('테스트 2: 로그인 성공', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 2 시작`);
    const startTime = Date.now();

    await page.goto('/login');
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');
    await page.getByRole('button', { name: '로그인' }).click();
    await expect(page).toHaveURL(/.*tickets/);

    const duration = Date.now() - startTime;
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 2 완료 (${duration}ms)`);
  });

  test('테스트 3: 로그인 실패', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 3 시작`);
    const startTime = Date.now();

    await page.goto('/login');
    await page.getByLabel('아이디').fill('invalid');
    await page.getByLabel('비밀번호').fill('wrong');
    await page.getByRole('button', { name: '로그인' }).click();
    await expect(page.getByRole('alert')).toBeVisible();

    const duration = Date.now() - startTime;
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 3 완료 (${duration}ms)`);
  });

  test('테스트 4: 빈 필드 검증', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 4 시작`);
    const startTime = Date.now();

    await page.goto('/login');
    await page.getByRole('button', { name: '로그인' }).click();

    const usernameInput = page.getByLabel('아이디');
    const isInvalid = await usernameInput.evaluate((el: HTMLInputElement) =>
      !el.validity.valid
    );
    expect(isInvalid).toBe(true);

    const duration = Date.now() - startTime;
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 4 완료 (${duration}ms)`);
  });

  test('테스트 5: 페이지 제목 확인', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 5 시작`);
    const startTime = Date.now();

    await page.goto('/login');
    await expect(page).toHaveTitle(/로그인|Login/i);

    const duration = Date.now() - startTime;
    console.log(`[워커 ${testInfo.parallelIndex}] 테스트 5 완료 (${duration}ms)`);
  });
});

/**
 * 순차 실행 모드 (기본값)
 * describe.configure()를 사용하지 않으면 순차적으로 실행됩니다.
 */
test.describe('순차 실행 데모 (비교용)', () => {
  // mode를 'serial'로 설정하면 명시적으로 순차 실행
  test.describe.configure({ mode: 'serial' });

  test('순차 테스트 1', async ({ page }, testInfo) => {
    console.log(`[순차] 테스트 1 시작`);
    await page.goto('/login');
    await expect(page).toHaveTitle(/로그인|Login/i);
    console.log(`[순차] 테스트 1 완료`);
  });

  test('순차 테스트 2', async ({ page }, testInfo) => {
    console.log(`[순차] 테스트 2 시작`);
    await page.goto('/login');
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    console.log(`[순차] 테스트 2 완료`);
  });

  test('순차 테스트 3', async ({ page }, testInfo) => {
    console.log(`[순차] 테스트 3 시작`);
    await page.goto('/login');
    await expect(page.getByLabel('아이디')).toBeVisible();
    console.log(`[순차] 테스트 3 완료`);
  });
});

/**
 * 테스트 격리 (Test Isolation) 데모
 * 각 테스트는 독립적인 브라우저 컨텍스트를 가지므로 서로 영향을 주지 않습니다.
 */
test.describe('테스트 격리 데모', () => {
  test.describe.configure({ mode: 'parallel' });

  test('격리 테스트 1: 로컬 스토리지 설정', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 로컬 스토리지에 데이터 저장`);

    await page.goto('/login');
    await page.evaluate(() => {
      localStorage.setItem('test-key', 'value-from-test-1');
    });

    const value = await page.evaluate(() => localStorage.getItem('test-key'));
    expect(value).toBe('value-from-test-1');
  });

  test('격리 테스트 2: 로컬 스토리지 확인', async ({ page }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 로컬 스토리지 확인`);

    await page.goto('/login');

    // 다른 테스트의 로컬 스토리지는 보이지 않음 (격리됨)
    const value = await page.evaluate(() => localStorage.getItem('test-key'));
    expect(value).toBeNull();
  });

  test('격리 테스트 3: 쿠키 설정', async ({ page, context }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 쿠키 설정`);

    await page.goto('/login');
    await context.addCookies([
      { name: 'test-cookie', value: 'cookie-from-test-3', url: 'http://localhost:3002' }
    ]);

    const cookies = await context.cookies();
    expect(cookies.some(c => c.name === 'test-cookie')).toBe(true);
  });

  test('격리 테스트 4: 쿠키 확인', async ({ page, context }, testInfo) => {
    console.log(`[워커 ${testInfo.parallelIndex}] 쿠키 확인`);

    await page.goto('/login');

    // 다른 테스트의 쿠키는 보이지 않음 (격리됨)
    const cookies = await context.cookies();
    expect(cookies.some(c => c.name === 'test-cookie')).toBe(false);
  });
});

/**
 * 워커 정보 및 메타데이터
 */
test.describe('워커 정보 확인', () => {
  test.describe.configure({ mode: 'parallel' });

  test('워커 메타데이터', async ({ page }, testInfo) => {
    console.log('=== 워커 정보 ===');
    console.log('워커 인덱스:', testInfo.parallelIndex);
    console.log('테스트 제목:', testInfo.title);
    console.log('프로젝트 이름:', testInfo.project.name);
    console.log('타임아웃:', testInfo.timeout);
    console.log('재시도 횟수:', testInfo.retry);

    await page.goto('/login');
    await expect(page).toHaveTitle(/로그인|Login/i);
  });

  test('테스트 메타데이터 추가', async ({ page }, testInfo) => {
    // 커스텀 어노테이션 추가
    testInfo.annotations.push({ type: 'category', description: 'smoke' });
    testInfo.annotations.push({ type: 'priority', description: 'high' });

    console.log('어노테이션:', testInfo.annotations);

    await page.goto('/login');
    await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
  });
});

/**
 * 성능 비교: 병렬 vs 순차
 *
 * 병렬 실행 (4개 워커):
 * - 총 실행 시간: ~5초 (동시 실행으로 단축)
 * - 각 워커가 독립적으로 실행
 *
 * 순차 실행 (1개 워커):
 * - 총 실행 시간: ~15초 (각 테스트가 순차적으로 실행)
 * - 모든 테스트가 하나의 워커에서 실행
 *
 * 실행 방법:
 * # 병렬 실행 (빠름)
 * npx playwright test parallel-demo.spec.ts --workers=4
 *
 * # 순차 실행 (느림)
 * npx playwright test parallel-demo.spec.ts --workers=1
 *
 * # CI 환경에서 권장 (안정성 우선)
 * npx playwright test parallel-demo.spec.ts --workers=2
 */

/**
 * 병렬 실행 주의사항
 *
 * ✅ 병렬 실행에 적합한 테스트:
 * - 상태를 공유하지 않는 독립적인 테스트
 * - 읽기 전용 작업 (조회, 검색 등)
 * - UI 렌더링 테스트
 *
 * ❌ 병렬 실행에 부적합한 테스트:
 * - 공유 데이터베이스를 수정하는 테스트
 * - 파일 시스템 조작 (같은 파일을 여러 워커가 수정)
 * - 순서가 중요한 시나리오 (예: 회원가입 → 로그인 → 프로필 수정)
 *
 * 해결 방법:
 * - test.describe.configure({ mode: 'serial' }) 사용
 * - 테스트별 격리된 데이터 사용 (UUID, 타임스탬프 등)
 * - 테스트 픽스처로 데이터 초기화/정리
 */
