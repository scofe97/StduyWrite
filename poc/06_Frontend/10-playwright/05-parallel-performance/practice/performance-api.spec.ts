import { test, expect } from '@playwright/test';

/**
 * 05-2. 성능 측정 API
 *
 * 브라우저의 Performance API를 활용하여 페이지 로딩 성능을 측정합니다.
 * - Navigation Timing API: 페이지 로딩 단계별 시간 측정
 * - Performance Marks & Measures: 커스텀 성능 마커
 * - Resource Timing API: 리소스별 로딩 시간
 *
 * 주요 메트릭:
 * - Time to First Byte (TTFB): 첫 바이트 수신 시간
 * - DOM Content Loaded: DOM 파싱 완료 시간
 * - Load Complete: 모든 리소스 로딩 완료 시간
 * - First Contentful Paint (FCP): 첫 콘텐츠 렌더링 시간
 */

interface PerformanceTiming {
  navigationStart: number;
  fetchStart: number;
  requestStart: number;
  responseStart: number;
  responseEnd: number;
  domLoading: number;
  domContentLoadedEventStart: number;
  domContentLoadedEventEnd: number;
  domComplete: number;
  loadEventStart: number;
  loadEventEnd: number;
}

interface PerformanceMetrics {
  ttfb: number;              // Time to First Byte
  domContentLoaded: number;  // DOM Content Loaded
  loadComplete: number;      // Page Load Complete
  domInteractive: number;    // DOM Interactive
  resourcesLoaded: number;   // All Resources Loaded
}

test.describe('05-2. 성능 측정 API', () => {

  /**
   * Navigation Timing API를 사용한 페이지 로딩 성능 측정
   */
  test('페이지 로딩 성능 측정 - Navigation Timing', async ({ page }) => {
    // 페이지 로드
    await page.goto('/login');

    // Performance Timing 데이터 수집
    const performanceTiming = await page.evaluate<PerformanceTiming>(() => {
      const timing = performance.timing;
      return {
        navigationStart: timing.navigationStart,
        fetchStart: timing.fetchStart,
        requestStart: timing.requestStart,
        responseStart: timing.responseStart,
        responseEnd: timing.responseEnd,
        domLoading: timing.domLoading,
        domContentLoadedEventStart: timing.domContentLoadedEventStart,
        domContentLoadedEventEnd: timing.domContentLoadedEventEnd,
        domComplete: timing.domComplete,
        loadEventStart: timing.loadEventStart,
        loadEventEnd: timing.loadEventEnd,
      };
    });

    // 성능 메트릭 계산
    const metrics: PerformanceMetrics = {
      // TTFB: Time to First Byte (서버 응답 시간)
      ttfb: performanceTiming.responseStart - performanceTiming.navigationStart,

      // DOM Content Loaded (DOM 파싱 완료)
      domContentLoaded: performanceTiming.domContentLoadedEventEnd - performanceTiming.navigationStart,

      // Load Complete (모든 리소스 로딩 완료)
      loadComplete: performanceTiming.loadEventEnd - performanceTiming.navigationStart,

      // DOM Interactive (DOM이 상호작용 가능한 시점)
      domInteractive: performanceTiming.domLoading - performanceTiming.navigationStart,

      // Resources Loaded (리소스 로딩 시간)
      resourcesLoaded: performanceTiming.domComplete - performanceTiming.navigationStart,
    };

    // 성능 메트릭 출력
    console.log('=== 페이지 로딩 성능 메트릭 ===');
    console.log(`TTFB (Time to First Byte): ${metrics.ttfb}ms`);
    console.log(`DOM Content Loaded: ${metrics.domContentLoaded}ms`);
    console.log(`Load Complete: ${metrics.loadComplete}ms`);
    console.log(`DOM Interactive: ${metrics.domInteractive}ms`);
    console.log(`Resources Loaded: ${metrics.resourcesLoaded}ms`);

    // 성능 임계값 검증
    expect(metrics.ttfb).toBeLessThan(1000); // TTFB는 1초 미만
    expect(metrics.domContentLoaded).toBeLessThan(3000); // DOM 파싱은 3초 미만
    expect(metrics.loadComplete).toBeLessThan(5000); // 전체 로딩은 5초 미만
  });

  /**
   * PerformanceNavigationTiming API (최신 버전)
   */
  test('페이지 로딩 성능 측정 - PerformanceNavigationTiming', async ({ page }) => {
    await page.goto('/login');

    const navigationTiming = await page.evaluate(() => {
      const [navigation] = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[];

      if (!navigation) return null;

      return {
        // DNS 조회 시간
        dnsTime: navigation.domainLookupEnd - navigation.domainLookupStart,

        // TCP 연결 시간
        tcpTime: navigation.connectEnd - navigation.connectStart,

        // 요청 시간
        requestTime: navigation.responseStart - navigation.requestStart,

        // 응답 시간
        responseTime: navigation.responseEnd - navigation.responseStart,

        // DOM 처리 시간
        domProcessingTime: navigation.domComplete - navigation.domInteractive,

        // 전체 로딩 시간
        totalTime: navigation.loadEventEnd - navigation.fetchStart,

        // 리다이렉트 시간
        redirectTime: navigation.redirectEnd - navigation.redirectStart,
      };
    });

    if (navigationTiming) {
      console.log('=== PerformanceNavigationTiming ===');
      console.log(`DNS 조회: ${navigationTiming.dnsTime}ms`);
      console.log(`TCP 연결: ${navigationTiming.tcpTime}ms`);
      console.log(`요청: ${navigationTiming.requestTime}ms`);
      console.log(`응답: ${navigationTiming.responseTime}ms`);
      console.log(`DOM 처리: ${navigationTiming.domProcessingTime}ms`);
      console.log(`전체: ${navigationTiming.totalTime}ms`);

      // 네트워크 시간이 합리적인지 검증
      expect(navigationTiming.dnsTime).toBeGreaterThanOrEqual(0);
      expect(navigationTiming.tcpTime).toBeGreaterThanOrEqual(0);
    }
  });

  /**
   * Performance Marks & Measures: 커스텀 성능 마커
   */
  test('커스텀 성능 마커 - Performance Marks', async ({ page }) => {
    await page.goto('/login');

    // 커스텀 마커 설정
    await page.evaluate(() => {
      // 로그인 시작 마커
      performance.mark('login-start');
    });

    // 로그인 수행
    await page.getByLabel('아이디').fill('admin');
    await page.getByLabel('비밀번호').fill('admin123');

    await page.evaluate(() => {
      // 입력 완료 마커
      performance.mark('input-complete');
    });

    await page.getByRole('button', { name: '로그인' }).click();

    await page.waitForURL(/.*tickets/);

    await page.evaluate(() => {
      // 로그인 완료 마커
      performance.mark('login-complete');

      // Measure 생성 (마커 간 시간 측정)
      performance.measure('login-input-time', 'login-start', 'input-complete');
      performance.measure('login-submit-time', 'input-complete', 'login-complete');
      performance.measure('total-login-time', 'login-start', 'login-complete');
    });

    // Measure 결과 가져오기
    const measures = await page.evaluate(() => {
      const loginInputTime = performance.getEntriesByName('login-input-time')[0] as PerformanceMeasure;
      const loginSubmitTime = performance.getEntriesByName('login-submit-time')[0] as PerformanceMeasure;
      const totalLoginTime = performance.getEntriesByName('total-login-time')[0] as PerformanceMeasure;

      return {
        inputTime: loginInputTime.duration,
        submitTime: loginSubmitTime.duration,
        totalTime: totalLoginTime.duration,
      };
    });

    console.log('=== 로그인 성능 측정 ===');
    console.log(`입력 시간: ${measures.inputTime.toFixed(2)}ms`);
    console.log(`제출 및 인증 시간: ${measures.submitTime.toFixed(2)}ms`);
    console.log(`전체 로그인 시간: ${measures.totalTime.toFixed(2)}ms`);

    // 로그인 시간이 합리적인지 검증
    expect(measures.totalTime).toBeLessThan(5000); // 5초 미만
  });

  /**
   * Resource Timing API: 리소스별 로딩 시간
   */
  test('리소스 로딩 성능 측정', async ({ page }) => {
    await page.goto('/login');

    const resourceTimings = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];

      return resources.map(resource => ({
        name: resource.name,
        type: resource.initiatorType,
        duration: resource.duration,
        size: resource.transferSize || 0,
        startTime: resource.startTime,
      }));
    });

    console.log('=== 리소스 로딩 성능 ===');
    console.log(`총 리소스 개수: ${resourceTimings.length}`);

    // 타입별 그룹화
    const byType = resourceTimings.reduce((acc, resource) => {
      acc[resource.type] = acc[resource.type] || [];
      acc[resource.type].push(resource);
      return acc;
    }, {} as Record<string, typeof resourceTimings>);

    Object.entries(byType).forEach(([type, resources]) => {
      const totalDuration = resources.reduce((sum, r) => sum + r.duration, 0);
      const totalSize = resources.reduce((sum, r) => sum + r.size, 0);
      const avgDuration = totalDuration / resources.length;

      console.log(`\n${type}:`);
      console.log(`  개수: ${resources.length}`);
      console.log(`  평균 로딩 시간: ${avgDuration.toFixed(2)}ms`);
      console.log(`  총 크기: ${(totalSize / 1024).toFixed(2)}KB`);
    });

    // 느린 리소스 찾기
    const slowResources = resourceTimings
      .filter(r => r.duration > 1000)
      .sort((a, b) => b.duration - a.duration);

    if (slowResources.length > 0) {
      console.log('\n⚠️  1초 이상 걸린 리소스:');
      slowResources.forEach(resource => {
        console.log(`  - ${resource.name}: ${resource.duration.toFixed(2)}ms`);
      });
    }
  });

  /**
   * 페이지 로딩 단계별 시간 비교
   */
  test('페이지 로딩 단계별 분석', async ({ page }) => {
    const startTime = Date.now();
    console.log('=== 페이지 로딩 단계 ===');

    // 1. 네비게이션 시작
    console.log(`1. 네비게이션 시작: ${Date.now() - startTime}ms`);

    await page.goto('/login', { waitUntil: 'commit' });
    console.log(`2. 서버 응답 받음 (commit): ${Date.now() - startTime}ms`);

    await page.goto('/login', { waitUntil: 'domcontentloaded' });
    console.log(`3. DOM 파싱 완료 (domcontentloaded): ${Date.now() - startTime}ms`);

    await page.goto('/login', { waitUntil: 'load' });
    console.log(`4. 모든 리소스 로딩 완료 (load): ${Date.now() - startTime}ms`);

    await page.goto('/login', { waitUntil: 'networkidle' });
    console.log(`5. 네트워크 유휴 상태 (networkidle): ${Date.now() - startTime}ms`);
  });

  /**
   * 성능 메트릭 비교: 여러 페이지
   */
  test('여러 페이지 성능 비교', async ({ page }) => {
    const pages = ['/login', '/tickets'];
    const results: Record<string, number> = {};

    for (const url of pages) {
      const startTime = Date.now();
      await page.goto(url);
      const loadTime = Date.now() - startTime;

      results[url] = loadTime;
      console.log(`${url}: ${loadTime}ms`);
    }

    // 가장 느린 페이지 찾기
    const slowestPage = Object.entries(results).reduce((a, b) =>
      a[1] > b[1] ? a : b
    );

    console.log(`\n⚠️  가장 느린 페이지: ${slowestPage[0]} (${slowestPage[1]}ms)`);
  });

  /**
   * Web Vitals 측정 (Core Web Vitals)
   * - LCP (Largest Contentful Paint): 주요 콘텐츠 렌더링 시간
   * - FID (First Input Delay): 첫 입력 지연 시간
   * - CLS (Cumulative Layout Shift): 누적 레이아웃 이동
   */
  test('Web Vitals 측정 (실험적)', async ({ page }) => {
    await page.goto('/login');

    // LCP 측정
    const lcp = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1] as any;
          resolve(lastEntry.renderTime || lastEntry.loadTime);
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // 타임아웃 설정
        setTimeout(() => resolve(0), 5000);
      });
    });

    if (lcp > 0) {
      console.log(`LCP (Largest Contentful Paint): ${lcp.toFixed(2)}ms`);

      // LCP는 2.5초 미만이 좋음
      if (lcp < 2500) {
        console.log('✅ LCP 성능 좋음');
      } else if (lcp < 4000) {
        console.log('⚠️  LCP 성능 개선 필요');
      } else {
        console.log('❌ LCP 성능 나쁨');
      }
    }
  });

  /**
   * 메모리 사용량 측정 (Chrome DevTools Protocol)
   */
  test('메모리 사용량 측정', async ({ page }) => {
    await page.goto('/login');

    // 메모리 정보 가져오기
    const memory = await page.evaluate(() => {
      if ('memory' in performance) {
        const mem = (performance as any).memory;
        return {
          usedJSHeapSize: mem.usedJSHeapSize,
          totalJSHeapSize: mem.totalJSHeapSize,
          jsHeapSizeLimit: mem.jsHeapSizeLimit,
        };
      }
      return null;
    });

    if (memory) {
      console.log('=== 메모리 사용량 ===');
      console.log(`사용 중: ${(memory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`);
      console.log(`할당됨: ${(memory.totalJSHeapSize / 1024 / 1024).toFixed(2)}MB`);
      console.log(`최대: ${(memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)}MB`);

      // 메모리 사용률
      const usagePercent = (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100;
      console.log(`사용률: ${usagePercent.toFixed(2)}%`);
    }
  });
});

/**
 * 성능 측정 베스트 프랙티스
 *
 * 1. 일관된 환경에서 측정
 *    - 같은 네트워크 환경
 *    - 같은 하드웨어
 *    - 같은 브라우저 버전
 *
 * 2. 여러 번 측정하여 평균값 사용
 *    - 캐시 영향 고려
 *    - 네트워크 변동성 고려
 *
 * 3. 임계값 설정
 *    - TTFB: < 200ms (이상적), < 600ms (허용)
 *    - DOM Content Loaded: < 1.5s
 *    - Load Complete: < 3s
 *    - LCP: < 2.5s (좋음), < 4s (개선 필요)
 *
 * 4. CI/CD 파이프라인에 통합
 *    - 성능 회귀 감지
 *    - 배포 전 성능 검증
 */
