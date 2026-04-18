# 03: Browser Agnostic Testing - 면접 정리

## 1. 핵심 개념 상세 설명

### Projects를 통한 멀티 브라우저 테스트

```
Projects 구조:
┌─────────────────────────────────────────────────────────────────┐
│  playwright.config.ts                                           │
│  │                                                              │
│  └── projects: [                                                │
│       ├── { name: 'chromium', use: { ...devices['Desktop Chrome'] } }
│       ├── { name: 'firefox', use: { ...devices['Desktop Firefox'] } }
│       ├── { name: 'webkit', use: { ...devices['Desktop Safari'] } }
│       └── { name: 'mobile', use: { ...devices['iPhone 16'] } }  │
│      ]                                                          │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     테스트 실행                                  │
│  ├── Chromium에서 실행 ────┐                                    │
│  ├── Firefox에서 실행  ────┼──► 통합 리포트                     │
│  ├── WebKit에서 실행   ────┤                                    │
│  └── Mobile에서 실행   ────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 브라우저 실행 옵션

```
주요 use 옵션:
┌──────────────────────┬─────────────────────────────────────────┐
│  카테고리            │  옵션                                   │
├──────────────────────┼─────────────────────────────────────────┤
│  뷰포트/디스플레이   │  viewport, deviceScaleFactor           │
│  모바일 에뮬레이션   │  isMobile, hasTouch                    │
│  로케일/타임존       │  locale, timezoneId                    │
│  위치 정보           │  geolocation, permissions              │
│  다크/라이트 모드    │  colorScheme                           │
│  User-Agent          │  userAgent                             │
│  세션 재사용         │  storageState                          │
│  HTTPS 오류 무시     │  ignoreHTTPSErrors                     │
│  프록시              │  proxy                                 │
└──────────────────────┴─────────────────────────────────────────┘
```

### storageState로 세션 재사용

```
storageState 워크플로우:
┌─────────────────────────────────────────────────────────────────┐
│  1. Setup 스크립트                                              │
│     ├── 로그인 수행                                             │
│     └── context.storageState({ path: 'auth.json' })             │
│                          │                                      │
│                          ▼                                      │
│  2. auth.json 파일 (쿠키, 로컬스토리지 저장)                    │
│                          │                                      │
│                          ▼                                      │
│  3. 테스트 설정                                                 │
│     use: { storageState: 'auth.json' }                          │
│                          │                                      │
│                          ▼                                      │
│  4. 테스트 실행 (이미 로그인된 상태)                            │
└─────────────────────────────────────────────────────────────────┘

장점:
├── 매 테스트마다 로그인 불필요
├── 테스트 실행 시간 단축
└── 인증 로직과 테스트 로직 분리
```

### 브랜드 브라우저 채널

```
Playwright 번들 vs 브랜드 브라우저:
┌─────────────────────────────────────────────────────────────────┐
│  Playwright 번들 브라우저                                       │
│  ├── chromium: Playwright가 빌드한 Chromium                    │
│  ├── firefox: Playwright가 빌드한 Firefox                      │
│  └── webkit: Playwright가 빌드한 WebKit                        │
├─────────────────────────────────────────────────────────────────│
│  브랜드 브라우저 (channel 옵션)                                 │
│  ├── chrome: Google Chrome Stable                              │
│  ├── chrome-beta: Chrome Beta                                  │
│  ├── chrome-canary: Chrome Canary                              │
│  ├── msedge: Microsoft Edge Stable                             │
│  ├── msedge-beta: Edge Beta                                    │
│  └── msedge-canary: Edge Canary                                │
└─────────────────────────────────────────────────────────────────┘

주의: 브랜드 브라우저는 시스템에 설치되어 있어야 함
```

### browserName과 isMobile Fixture

```
조건부 로직 작성:
┌─────────────────────────────────────────────────────────────────┐
│  test('responsive test', async ({ page, browserName, isMobile }) => {
│    console.log(`Browser: ${browserName}, Mobile: ${isMobile}`);
│
│    if (isMobile) {
│      // 모바일: 햄버거 메뉴 클릭
│      await page.getByRole('button', { name: 'Menu' }).click();
│    }
│
│    // 공통 로직
│    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
│  });                                                            │
└─────────────────────────────────────────────────────────────────┘

테스트 스킵:
test('WebKit 전용 테스트', async ({ browserName }) => {
  test.skip(browserName !== 'webkit', 'WebKit 전용');
  // WebKit에서만 실행
});
```

### 디바이스 에뮬레이션

```
내장 디바이스 프로필:
┌─────────────────────────────────────────────────────────────────┐
│  Desktop                                                        │
│  ├── Desktop Chrome, Desktop Firefox, Desktop Safari            │
│                                                                 │
│  iPhone                                                         │
│  ├── iPhone 12, iPhone 14, iPhone 16, iPhone 16 Pro            │
│                                                                 │
│  Android                                                        │
│  ├── Pixel 5, Pixel 7, Pixel 8                                 │
│                                                                 │
│  Tablet                                                         │
│  └── iPad Pro 11, iPad Mini, Galaxy Tab S4                     │
└─────────────────────────────────────────────────────────────────┘

프로필 오버라이드:
{
  name: 'Pixel 8 Dark Mode',
  use: {
    ...devices['Pixel 8'],     // 기본 설정 상속
    colorScheme: 'dark',       // 다크 모드로 변경
    locale: 'ko-KR',           // 한국어로 변경
  },
}
```

### 디버깅 전략

```
브라우저별 테스트 실패 디버깅:
┌─────────────────────────────────────────────────────────────────┐
│  1. 특정 브라우저만 실행                                        │
│     npx playwright test --project=webkit                        │
│                                                                 │
│  2. headed 모드로 확인                                          │
│     npx playwright test --project=webkit --headed               │
│                                                                 │
│  3. slowMo로 느리게 실행                                        │
│     launchOptions: { slowMo: 1000 }                             │
│                                                                 │
│  4. page.pause()로 중단점                                       │
│     await page.pause();  // Inspector 열림                      │
│                                                                 │
│  5. DevTools로 검사                                             │
│     Playwright Inspector에서 단계별 실행                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 비교표

### Playwright 지원 브라우저

| 브라우저 | 엔진 | Playwright 이름 | 브랜드 채널 |
|----------|------|----------------|------------|
| Chrome | Chromium | `chromium` | `chrome`, `chrome-beta` |
| Edge | Chromium | `chromium` | `msedge`, `msedge-beta` |
| Firefox | Gecko | `firefox` | - |
| Safari | WebKit | `webkit` | - |

### 실행 옵션 비교

| 옵션 | 타입 | 용도 | 예시 |
|------|------|------|------|
| `viewport` | object | 뷰포트 크기 | `{ width: 1920, height: 1080 }` |
| `deviceScaleFactor` | number | DPI 배율 | `2` (Retina) |
| `isMobile` | boolean | 모바일 에뮬레이션 | `true` |
| `hasTouch` | boolean | 터치 이벤트 | `true` |
| `locale` | string | 브라우저 로케일 | `'ko-KR'` |
| `timezoneId` | string | 타임존 | `'Asia/Seoul'` |
| `colorScheme` | string | 다크/라이트 모드 | `'dark'` |
| `storageState` | string | 저장된 세션 | `'auth.json'` |

### CLI 명령어 비교

| 명령어 | 설명 |
|--------|------|
| `npx playwright test` | 모든 프로젝트에서 실행 |
| `--project chromium` | Chromium만 실행 |
| `--project chromium --project firefox` | 복수 지정 |
| `--project mobile-chrome --grep "login"` | 필터 조합 |
| `--headed` | 브라우저 UI 표시 |
| `--debug` | Inspector 디버깅 |

### 디바이스 에뮬레이션 vs 실제 디바이스

| 구분 | 에뮬레이션 | 실제 디바이스 |
|------|----------|--------------|
| **속도** | 빠름 | 느림 |
| **비용** | 무료 | 디바이스 구매/클라우드 비용 |
| **정확도** | 90%+ | 100% |
| **터치 동작** | 에뮬레이션 | 실제 |
| **하드웨어 기능** | 제한적 | 완전 지원 |
| **CI/CD 통합** | 쉬움 | 복잡 |

---

## 3. 면접 예상 질문 및 모범 답안

### Q1. Playwright에서 멀티 브라우저 테스트를 설정하는 방법은?

**모범 답안:**

`playwright.config.ts`의 **projects** 배열을 사용합니다:

```typescript
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
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
});
```

**실행:**
```bash
# 모든 브라우저
npx playwright test

# 특정 브라우저만
npx playwright test --project chromium
```

한 번의 테스트 코드 작성으로 여러 브라우저에서 동일한 테스트를 실행할 수 있습니다.

---

### Q2. 특정 브라우저에서만 테스트를 실행하려면 어떻게 하나요?

**모범 답안:**

**방법 1: CLI에서 --project 플래그**
```bash
# Chromium만
npx playwright test --project chromium

# 복수 지정
npx playwright test --project chromium --project firefox
```

**방법 2: 테스트 코드에서 조건부 스킵**
```typescript
test('WebKit 전용 테스트', async ({ browserName }) => {
  test.skip(browserName !== 'webkit', 'WebKit 전용 테스트입니다');
  // WebKit에서만 실행
});
```

**주의:** 프로젝트 이름은 **대소문자를 구분**합니다. `chromium` ≠ `Chromium`

---

### Q3. storageState의 용도와 이점은 무엇인가요?

**모범 답안:**

**용도:** 로그인 세션(쿠키, 로컬스토리지)을 파일로 저장하여 테스트 간 재사용

**워크플로우:**
```typescript
// 1. Setup 스크립트에서 로그인 후 저장
await context.storageState({ path: 'auth.json' });

// 2. 설정에서 로드
use: { storageState: 'auth.json' }
```

**이점:**
| 항목 | 설명 |
|------|------|
| 속도 향상 | 매 테스트마다 로그인 불필요 |
| 관심사 분리 | 인증 로직과 테스트 로직 분리 |
| 안정성 | 로그인 과정의 flaky 요소 제거 |

실제 CI/CD에서는 Setup Project로 로그인을 처리하고, 나머지 테스트는 저장된 세션을 사용합니다.

---

### Q4. 브라우저별로 다른 동작을 처리하는 방법은?

**모범 답안:**

**browserName과 isMobile fixture 활용:**
```typescript
test('반응형 테스트', async ({ page, browserName, isMobile }) => {
  if (isMobile) {
    // 모바일: 햄버거 메뉴 클릭
    await page.getByRole('button', { name: 'Menu' }).click();
  }

  if (browserName === 'webkit') {
    // WebKit 특수 처리
    test.skip(true, 'WebKit에서 미지원 기능');
  }

  // 공통 검증
  await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
});
```

**권장 접근법:**
1. 설정(config)에서 차이 처리 (우선)
2. 조건부 로직은 최소화하고 문서화 필수
3. 브라우저별 별도 테스트 파일은 최후의 수단

---

### Q5. 디바이스 에뮬레이션과 실제 디바이스 테스트의 차이점은?

**모범 답안:**

| 구분 | 에뮬레이션 | 실제 디바이스 |
|------|----------|--------------|
| **정확도** | 90%+ (화면 크기, UA 등) | 100% |
| **터치** | 에뮬레이션 (마우스 이벤트 변환) | 실제 터치 |
| **하드웨어** | 제한적 (카메라, GPS 등) | 완전 지원 |
| **속도** | 빠름 | 느림 |
| **비용** | 무료 | 디바이스/클라우드 비용 |

**에뮬레이션 사용:**
```typescript
{
  name: 'mobile',
  use: {
    ...devices['iPhone 16'],
    // viewport, userAgent, deviceScaleFactor 등 자동 설정
  },
}
```

**권장:** 대부분의 반응형 테스트는 에뮬레이션으로 충분. 핵심 기능은 실제 디바이스로 검증.

---

### Q6. 크로스 브라우저 테스트 시 주의할 점은?

**모범 답안:**

**DO:**
```
권장 사항:
├── 사용자 관점의 assertion (toBeVisible, toHaveText)
├── 설정(config)에서 브라우저 차이 처리
├── 기능 지원 여부 사전 확인 (caniuse.com)
├── 초기부터 크로스 브라우저 테스트
└── expect().toBeVisible() 등 auto-retry assertion
```

**DON'T:**
```
피해야 할 것:
├── 픽셀 단위 비교 (브라우저별 렌더링 차이)
├── 고정 대기 시간 (waitForTimeout)
├── 테스트 코드에 조건문 남발
├── 최신 CSS/JS 기능 무분별 사용
└── 개발 완료 후 테스트 (초기부터 해야 함)
```

**브라우저별 기능 확인:**
```typescript
test('backdrop-filter 테스트', async ({ browserName }) => {
  // Firefox는 backdrop-filter 지원이 제한적
  if (browserName === 'firefox') {
    test.skip(true, 'backdrop-filter not fully supported');
  }
  // ...
});
```

---

## 4. 실무 체크리스트

### 프로젝트 설정

- [ ] 처음부터 3개 브라우저(Chromium, Firefox, WebKit) projects 설정
- [ ] 모바일 프로젝트 추가 (반응형 테스트 필요 시)
- [ ] devices 프로필 활용 (직접 설정보다 권장)

### 세션 관리

- [ ] storageState로 로그인 세션 재사용
- [ ] Setup Project로 인증 로직 분리
- [ ] auth.json을 .gitignore에 추가

### 조건부 로직

- [ ] browserName, isMobile fixture 활용
- [ ] 조건부 로직은 최소화
- [ ] 스킵 사유 명시 (test.skip의 두 번째 인자)

### 디버깅

- [ ] --project 플래그로 특정 브라우저만 실행
- [ ] --headed 모드로 시각적 확인
- [ ] slowMo, page.pause() 활용

### 주의사항

- [ ] 프로젝트 이름 대소문자 구분
- [ ] spread 연산자 후에 오버라이드 배치
- [ ] channel 사용 시 브라우저 설치 확인

---

## 5. 참고 자료

- [Playwright Test Projects](https://playwright.dev/docs/test-projects)
- [Playwright Browser Contexts](https://playwright.dev/docs/browser-contexts)
- [Playwright Emulation](https://playwright.dev/docs/emulation)
- [Playwright Debugging](https://playwright.dev/docs/debug)
- [Can I Use](https://caniuse.com/) - 브라우저 기능 호환성
- [Playwright Device Descriptors](https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json)
