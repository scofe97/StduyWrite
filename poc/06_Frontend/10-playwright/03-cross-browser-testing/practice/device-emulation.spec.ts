import { test, expect, devices } from '@playwright/test';

/**
 * 03-2. 디바이스 에뮬레이션
 *
 * Playwright는 다양한 디바이스(모바일, 태블릿)를 에뮬레이션할 수 있습니다.
 * - 뷰포트 크기
 * - User-Agent
 * - 터치 이벤트
 * - 지리적 위치
 * - 색상 스킴 (다크모드)
 *
 * 사용 가능한 디바이스 목록: https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json
 */
test.describe('03-2. 디바이스 에뮬레이션', () => {

  /**
   * 모바일 뷰포트 테스트
   * test.use()를 사용하여 디바이스 설정 적용
   */
  test.describe('모바일 뷰포트', () => {
    // iPhone 14 디바이스 설정 적용
    test.use({ ...devices['iPhone 14'] });

    test('모바일에서 로그인 페이지 레이아웃', async ({ page }) => {
      await page.goto('/login');

      // 뷰포트 크기 확인
      const viewport = page.viewportSize();
      console.log('Mobile viewport:', viewport);
      expect(viewport?.width).toBeLessThan(500);

      // 모바일에서도 로그인 버튼이 보이는지 확인
      await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    });

    test('모바일에서 입력 필드 포커스', async ({ page }) => {
      await page.goto('/login');

      const idInput = page.getByLabel('아이디');
      await idInput.click();

      // 모바일에서 입력 필드에 포커스가 잘 되는지 확인
      await expect(idInput).toBeFocused();
    });

    test('모바일 User-Agent 확인', async ({ page }) => {
      await page.goto('/login');

      const userAgent = await page.evaluate(() => navigator.userAgent);
      console.log('Mobile User-Agent:', userAgent);

      // iPhone User-Agent 포함 확인
      expect(userAgent).toContain('iPhone');
    });
  });

  /**
   * 태블릿 뷰포트 테스트
   * 중간 크기 디바이스에서의 레이아웃 검증
   */
  test.describe('태블릿 뷰포트', () => {
    test.use({ ...devices['iPad Pro 11'] });

    test('태블릿에서 티켓 목록 테이블', async ({ page }) => {
      // 로그인
      await page.goto('/login');
      await page.getByLabel('아이디').fill('admin');
      await page.getByLabel('비밀번호').fill('admin123');
      await page.getByRole('button', { name: '로그인' }).click();

      // 티켓 목록 페이지로 이동 대기
      await page.waitForURL(/.*tickets/);

      // 태블릿에서 테이블이 잘 보이는지 확인
      await expect(page.getByTestId('ticket-table')).toBeVisible();

      const viewport = page.viewportSize();
      console.log('Tablet viewport:', viewport);
      expect(viewport?.width).toBeGreaterThan(768);
    });

    test('태블릿 가로/세로 모드', async ({ page }) => {
      await page.goto('/login');

      // 가로 모드 (기본)
      let viewport = page.viewportSize();
      console.log('Landscape mode:', viewport);

      // 세로 모드로 변경
      await page.setViewportSize({
        width: viewport!.height,
        height: viewport!.width
      });

      viewport = page.viewportSize();
      console.log('Portrait mode:', viewport);

      // 레이아웃이 여전히 정상인지 확인
      await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    });
  });

  /**
   * 커스텀 뷰포트 설정
   * 프리셋 외에 직접 뷰포트와 User-Agent를 설정할 수 있습니다.
   */
  test.describe('커스텀 뷰포트', () => {
    test.use({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Custom-Test-Agent/1.0',
    });

    test('Full HD 뷰포트에서 테스트', async ({ page }) => {
      await page.goto('/login');

      const viewport = page.viewportSize();
      expect(viewport?.width).toBe(1920);
      expect(viewport?.height).toBe(1080);

      console.log('Custom viewport:', viewport);
    });

    test('커스텀 User-Agent 확인', async ({ page }) => {
      await page.goto('/login');

      const userAgent = await page.evaluate(() => navigator.userAgent);
      expect(userAgent).toBe('Custom-Test-Agent/1.0');
    });
  });

  /**
   * 색상 스킴 에뮬레이션
   * 다크모드/라이트모드 테스트
   */
  test.describe('색상 스킴', () => {
    test.use({ colorScheme: 'dark' });

    test('다크모드 에뮬레이션', async ({ page }) => {
      await page.goto('/login');

      // 다크모드 감지
      const isDarkMode = await page.evaluate(() =>
        window.matchMedia('(prefers-color-scheme: dark)').matches
      );
      expect(isDarkMode).toBe(true);

      console.log('다크모드 활성화됨');
    });

    test('라이트모드로 변경', async ({ page, context }) => {
      // 컨텍스트 수준에서 색상 스킴 변경
      await context.close();

      // 새 컨텍스트를 라이트모드로 생성
      const newContext = await page.context().browser()!.newContext({
        colorScheme: 'light',
      });

      const newPage = await newContext.newPage();
      await newPage.goto('/login');

      const isLightMode = await newPage.evaluate(() =>
        !window.matchMedia('(prefers-color-scheme: dark)').matches
      );
      expect(isLightMode).toBe(true);

      await newContext.close();
    });
  });

  /**
   * 지역/언어 에뮬레이션
   * 로케일과 타임존 설정
   */
  test.describe('로케일 설정', () => {
    test.use({
      locale: 'ko-KR',
      timezoneId: 'Asia/Seoul'
    });

    test('한국어 로케일 에뮬레이션', async ({ page }) => {
      await page.goto('/login');

      const locale = await page.evaluate(() => navigator.language);
      expect(locale).toBe('ko-KR');

      console.log('현재 로케일:', locale);
    });

    test('타임존 확인', async ({ page }) => {
      await page.goto('/login');

      const timezone = await page.evaluate(() => {
        const offset = new Date().getTimezoneOffset();
        return offset;
      });

      // 한국 시간대 (UTC+9, 즉 -540분)
      expect(timezone).toBe(-540);

      console.log('타임존 오프셋 (분):', timezone);
    });

    test('날짜 포맷 확인', async ({ page }) => {
      await page.goto('/login');

      const dateString = await page.evaluate(() => {
        return new Date('2024-01-01').toLocaleDateString('ko-KR');
      });

      // 한국어 날짜 형식 확인
      expect(dateString).toContain('2024');
      console.log('날짜 포맷:', dateString);
    });
  });

  /**
   * 지리적 위치 에뮬레이션
   * GPS 좌표 설정 및 권한 부여
   */
  test.describe('지리적 위치', () => {
    test.use({
      geolocation: { longitude: 126.9780, latitude: 37.5665 }, // 서울
      permissions: ['geolocation'],
    });

    test('위치 정보 접근', async ({ page }) => {
      await page.goto('/login');

      // 위치 정보 조회
      const position = await page.evaluate(() => {
        return new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(
            (pos) => resolve({
              latitude: pos.coords.latitude,
              longitude: pos.coords.longitude,
            }),
            (err) => reject(err)
          );
        });
      });

      expect(position).toMatchObject({
        latitude: 37.5665,
        longitude: 126.9780,
      });

      console.log('현재 위치:', position);
    });
  });

  /**
   * 네트워크 속도 에뮬레이션
   * 느린 네트워크 환경 시뮬레이션
   */
  test.describe('네트워크 속도', () => {
    test('느린 3G 네트워크 시뮬레이션', async ({ page, context }) => {
      // 네트워크 조건 설정 (Slow 3G)
      await context.route('**/*', async (route) => {
        // 500ms 지연 추가
        await new Promise(resolve => setTimeout(resolve, 500));
        await route.continue();
      });

      const startTime = Date.now();
      await page.goto('/login');
      const loadTime = Date.now() - startTime;

      console.log('페이지 로딩 시간 (느린 네트워크):', loadTime, 'ms');

      // 느린 네트워크에서도 페이지가 로드되는지 확인
      await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    });
  });

  /**
   * 터치 이벤트 에뮬레이션
   * 모바일 디바이스의 터치 동작 시뮬레이션
   */
  test.describe('터치 이벤트', () => {
    test.use({
      ...devices['iPhone 14'],
      hasTouch: true,
    });

    test('터치 이벤트 처리', async ({ page }) => {
      await page.goto('/login');

      // 터치 지원 확인
      const hasTouchSupport = await page.evaluate(() =>
        'ontouchstart' in window
      );
      expect(hasTouchSupport).toBe(true);

      console.log('터치 이벤트 지원:', hasTouchSupport);
    });

    test('스와이프 제스처 시뮬레이션', async ({ page }) => {
      await page.goto('/login');

      // 터치 시작 지점
      await page.touchscreen.tap(100, 100);

      // 페이지가 여전히 정상인지 확인
      await expect(page.getByRole('button', { name: '로그인' })).toBeVisible();
    });
  });
});
