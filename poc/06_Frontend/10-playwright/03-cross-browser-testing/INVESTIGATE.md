# 03. 크로스 브라우저 테스트 - 조사 (INVESTIGATE)

**작성일**: 2026-02-05
**목표**: Playwright의 크로스 브라우저 테스트 메커니즘 이해
**학습 패턴**: 소크라테스식 질문 → 탐구 → 이해

---

## 질문 1: Chromium, Firefox, WebKit 각 브라우저 엔진의 차이와 Playwright에서의 지원 방식

### 왜 이 질문이 중요한가?
웹 애플리케이션은 사용자가 다양한 브라우저에서 접근합니다. 각 브라우저 엔진은 웹 표준을 다르게 구현하므로, 같은 코드가 다르게 동작할 수 있습니다.

### 탐구 포인트
- **Chromium**: Google Chrome, Edge의 기반. V8 JavaScript 엔진 사용
- **Firefox**: Mozilla의 Gecko 엔진. SpiderMonkey JavaScript 엔진
- **WebKit**: Safari의 기반. JavaScriptCore 엔진

### 차이점
| 브라우저 엔진 | JavaScript 엔진 | 시장 점유율 | CSS 지원 차이 |
|---------------|-----------------|------------|---------------|
| Chromium | V8 | ~65% | 최신 CSS 빠른 지원 |
| Firefox | SpiderMonkey | ~3% | 독립적 표준 준수 |
| WebKit | JavaScriptCore | ~20% (iOS) | Safari 특유 버그 존재 |

### Playwright의 지원 방식
Playwright는 각 브라우저 벤더와 협력하여 **네이티브 자동화 프로토콜**을 사용합니다:

- **Chromium**: Chrome DevTools Protocol (CDP)
- **Firefox**: Firefox Remote Protocol
- **WebKit**: WebKit Automation Protocol

이는 Selenium과 다릅니다. Selenium은 WebDriver 표준을 사용하지만, Playwright는 더 깊은 수준의 제어가 가능합니다.

### 실무 예시
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

실행 시 Playwright는 각 브라우저를 독립적으로 실행하며, 같은 테스트를 3번 수행합니다.

### 핵심 이해
Playwright는 브라우저 벤더의 공식 자동화 API를 사용하므로, WebDriver보다 빠르고 안정적입니다. 각 브라우저 엔진의 차이를 이해하면, 왜 크로스 브라우저 테스트가 필요한지 명확해집니다.

---

## 질문 2: playwright.config.ts의 projects 배열로 멀티 브라우저 설정하는 방법

### 왜 이 질문이 중요한가?
하나의 설정 파일로 여러 브라우저에서 동시에 테스트를 실행할 수 있어야 효율적입니다.

### 탐구 포인트
`projects` 배열의 각 항목은 독립적인 테스트 실행 환경을 정의합니다.

### 설정 구조
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // 전역 설정
  testDir: './tests',
  timeout: 30000,
  retries: 2,

  // 브라우저별 프로젝트 정의
  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
        screenshot: 'only-on-failure',
      },
    },
    {
      name: 'firefox-desktop',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'webkit-desktop',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 7'],
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 14'],
      },
    },
  ],
});
```

### 선택적 실행
```bash
# 특정 프로젝트만 실행
npx playwright test --project=chromium-desktop

# 여러 프로젝트 실행
npx playwright test --project=chromium-desktop --project=firefox-desktop

# 모든 프로젝트 실행 (기본값)
npx playwright test
```

### 프로젝트별 다른 설정 적용
```typescript
projects: [
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] },
    testMatch: /.*\.spec\.ts/, // 모든 테스트 실행
  },
  {
    name: 'webkit',
    use: { ...devices['Desktop Safari'] },
    testMatch: /.*\.critical\.spec\.ts/, // 중요 테스트만
    retries: 3, // Safari는 재시도 더 많이
  },
],
```

### 핵심 이해
`projects`는 테스트 실행 환경의 매트릭스를 정의합니다. 각 프로젝트는 독립적으로 실행되며, 동일한 테스트 파일을 다른 환경에서 검증합니다.

---

## 질문 3: devices descriptor란? 모바일 에뮬레이션의 원리

### 왜 이 질문이 중요한가?
모바일 기기에서의 동작을 검증하려면, 실제 기기 없이도 환경을 재현할 수 있어야 합니다.

### devices descriptor란?
Playwright가 제공하는 **사전 정의된 기기 프로필**입니다. 실제 기기의 특성을 JavaScript 객체로 표현합니다.

### 구조
```typescript
// @playwright/test의 devices 객체
const devices = {
  'iPhone 14': {
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)...',
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    defaultBrowserType: 'webkit',
  },
  'Pixel 7': {
    userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7)...',
    viewport: { width: 412, height: 915 },
    deviceScaleFactor: 2.625,
    isMobile: true,
    hasTouch: true,
    defaultBrowserType: 'chromium',
  },
};
```

### 에뮬레이션 원리
모바일 에뮬레이션은 다음 요소들을 시뮬레이션합니다:

1. **Viewport 크기**: 화면 해상도
2. **Device Scale Factor**: Retina 디스플레이 등의 픽셀 밀도
3. **User Agent**: 서버가 기기를 식별하는 문자열
4. **Touch Events**: 터치 입력 활성화
5. **Geolocation**: GPS 위치 (선택)
6. **Orientation**: Portrait/Landscape

### 실무 예시
```typescript
import { test, devices } from '@playwright/test';

test('모바일에서 메뉴 버거 아이콘 표시', async ({ page }) => {
  // localhost:3002 Mock 서버
  await page.goto('http://localhost:3002');

  // 모바일 viewport에서는 햄버거 메뉴가 보임
  const burgerMenu = page.locator('[data-testid="burger-menu"]');
  await expect(burgerMenu).toBeVisible();

  // 데스크톱에서는 보이지 않음
  await page.setViewportSize({ width: 1920, height: 1080 });
  await expect(burgerMenu).toBeHidden();
});
```

### 커스텀 기기 정의
```typescript
const customDevice = {
  userAgent: 'MyCustomAgent/1.0',
  viewport: { width: 500, height: 800 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
};

test.use(customDevice);
```

### 핵심 이해
devices descriptor는 실제 기기의 특성을 코드로 표현한 것입니다. 브라우저에 "이 기기인 것처럼 동작해"라고 지시하는 메타데이터입니다. 실제 하드웨어는 아니지만, 웹 페이지 입장에서는 구분할 수 없습니다.

---

## 질문 4: 브라우저별로 다르게 동작하는 CSS/JS 기능은 무엇이 있는가?

### 왜 이 질문이 중요한가?
표준을 따르더라도, 각 브라우저는 구현 시점이 다르거나 버그가 있을 수 있습니다. 이를 알아야 크로스 브라우저 이슈를 예측하고 대응할 수 있습니다.

### CSS 차이점

#### 1. Flexbox Gap (과거 Safari 이슈)
```css
/* Safari 14 이전에는 gap 지원 안 됨 */
.container {
  display: flex;
  gap: 1rem; /* Safari 14.1+ */
}
```

#### 2. CSS Grid 자동 배치
```css
/* Firefox와 Chrome의 자동 배치 알고리즘 차이 */
.grid {
  display: grid;
  grid-auto-flow: dense; /* 브라우저마다 순서 다를 수 있음 */
}
```

#### 3. Scrollbar 스타일링
```css
/* WebKit 전용 */
::-webkit-scrollbar {
  width: 10px;
}

/* Firefox 전용 */
scrollbar-width: thin;
scrollbar-color: #888 #f1f1f1;
```

### JavaScript 차이점

#### 1. Date 파싱
```javascript
// Safari는 'YYYY-MM-DD' 형식만 지원 (ISO 8601)
new Date('2024-01-15'); // ✅ 모든 브라우저
new Date('01/15/2024'); // ❌ Safari에서 Invalid Date
```

#### 2. RegExp Lookbehind
```javascript
// Chrome 62+, Firefox 78+, Safari 16.4+
const regex = /(?<=@)\w+/; // Safari 16.4 이전 미지원
```

#### 3. Intl.Segmenter
```javascript
// Chrome 87+, Firefox 미지원, Safari 14.1+
const segmenter = new Intl.Segmenter('en', { granularity: 'word' });
```

### 테스트로 차이 감지
```typescript
import { test, expect } from '@playwright/test';

test('브라우저별 Date 파싱 동작', async ({ page, browserName }) => {
  await page.goto('http://localhost:3002/date-test');

  const result = await page.evaluate(() => {
    const date = new Date('01/15/2024');
    return date.toString();
  });

  if (browserName === 'webkit') {
    // Safari는 Invalid Date 반환할 수 있음
    expect(result).toContain('Invalid');
  } else {
    // Chrome, Firefox는 정상 파싱
    expect(result).toContain('2024');
  }
});
```

### 핵심 이해
브라우저 엔진은 웹 표준을 구현하는 속도와 방식이 다릅니다. 최신 기능을 사용할 때는 [caniuse.com](https://caniuse.com)으로 지원 여부를 확인하고, 크로스 브라우저 테스트로 검증해야 합니다.

---

## 질문 5: CI 환경에서 크로스 브라우저 테스트 전략 (비용 vs 커버리지)

### 왜 이 질문이 중요한가?
모든 브라우저에서 모든 테스트를 실행하면 시간과 비용이 많이 듭니다. 효율적인 전략이 필요합니다.

### 테스트 피라미드 (크로스 브라우저 관점)

```
           /\
          /  \       Chromium만
         / E2E \     (핵심 사용자 여정)
        /──────\
       /        \    Chromium + Safari
      / 통합     \   (주요 기능)
     /──────────\
    /            \   모든 브라우저
   / 단위 + 기능  \  (UI 컴포넌트)
  /──────────────\
```

### 전략 1: 계층별 브라우저 선택
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // 모든 테스트: Chromium (가장 빠름)
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      testMatch: /.*\.spec\.ts/,
    },

    // 중요 테스트만: Firefox, Safari
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      testMatch: /.*\.critical\.spec\.ts/,
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      testMatch: /.*\.critical\.spec\.ts/,
    },
  ],
});
```

### 전략 2: Sharding으로 병렬 실행
```yaml
# GitHub Actions 예시
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
        browser: [chromium, firefox, webkit]
    steps:
      - run: npx playwright test --project=${{ matrix.browser }} --shard=${{ matrix.shard }}/4
```

**효과**:
- 4개 샤드 × 3개 브라우저 = 12개 병렬 작업
- 총 시간: 전체 시간 ÷ 4

### 전략 3: 조건부 실행
```typescript
test.describe('결제 기능', () => {
  test('신용카드 결제', async ({ page }) => {
    // 모든 브라우저에서 실행
  });

  test('Apple Pay (Safari only)', async ({ page, browserName }) => {
    test.skip(browserName !== 'webkit', 'Safari만 테스트');
    // WebKit에서만 실행
  });
});
```

### 비용 vs 커버리지 계산

| 전략 | 실행 시간 | CI 비용 | 커버리지 | 추천 시점 |
|------|-----------|---------|----------|----------|
| Chromium만 | 10분 | $ | 60% | 개발 중 |
| Chromium + Safari | 20분 | $$ | 85% | PR 리뷰 |
| 모든 브라우저 | 30분 | $$$ | 95% | 메인 브랜치 머지 |
| 모든 브라우저 + Sharding | 10분 | $$$$ | 95% | 프로덕션 배포 |

### 실무 권장 전략
```typescript
// playwright.config.ts
const isCI = !!process.env.CI;
const isPR = !!process.env.GITHUB_EVENT_NAME && process.env.GITHUB_EVENT_NAME === 'pull_request';

export default defineConfig({
  projects: isCI && !isPR
    ? [
        // 메인 브랜치: 모든 브라우저
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
      ]
    : [
        // PR: Chromium만
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
      ],
});
```

### 핵심 이해
크로스 브라우저 테스트는 **선택적으로 실행**해야 합니다. 개발 중에는 빠른 피드백을 위해 Chromium만, 배포 전에는 모든 브라우저에서 검증하는 전략이 효율적입니다. Sharding을 활용하면 병렬 실행으로 시간을 단축할 수 있습니다.

---

## 다음 단계

이 조사를 바탕으로 `LEARN.md`에서 실제 구현 패턴을 학습합니다:

1. 브라우저 엔진별 특성 이해 → 설정 방법 학습
2. projects 배열 구조 이해 → 멀티 브라우저 설정 실습
3. devices descriptor 원리 이해 → 모바일 에뮬레이션 적용
4. 브라우저별 차이점 파악 → 조건부 테스트 작성
5. CI 전략 이해 → 실제 파이프라인 구축

**학습 포인트**: 크로스 브라우저 테스트는 "모든 브라우저에서 모든 테스트"가 아니라, "적절한 브라우저에서 적절한 테스트"를 실행하는 전략입니다.
