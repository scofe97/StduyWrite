# 02: Advanced Selectors & Dynamic Content - 면접 정리

## 1. 핵심 개념 상세 설명

### getBy* 로케이터 우선순위

```
셀렉터 선택 우선순위:
┌─────────────────────────────────────────────────────────────────┐
│  1순위: getBy* 로케이터 (접근성 기반, 권장)                     │
│  ├── getByRole      : ARIA 역할 기반                           │
│  ├── getByLabel     : <label> 연결 요소                        │
│  ├── getByPlaceholder: placeholder 텍스트                      │
│  ├── getByText      : 보이는 텍스트                            │
│  ├── getByAltText   : 이미지 alt 속성                          │
│  ├── getByTitle     : title 속성                               │
│  └── getByTestId    : data-testid 속성                         │
├─────────────────────────────────────────────────────────────────│
│  2순위: getByTestId (접근성 속성 없을 때)                       │
├─────────────────────────────────────────────────────────────────│
│  3순위: CSS 셀렉터 (주의 필요)                                  │
├─────────────────────────────────────────────────────────────────│
│  4순위: XPath (최후의 수단)                                     │
└─────────────────────────────────────────────────────────────────┘

비유:
├── getBy* : "제출 버튼을 찾아줘" (의미 기반)
└── CSS    : "3번째 div 안의 2번째 button을 찾아줘" (구조 기반)
```

### getBy* 로케이터 종류

```
getBy* 로케이터 상세:
┌──────────────────┬──────────────────────────────────────────────┐
│  로케이터        │  사용 예시                                   │
├──────────────────┼──────────────────────────────────────────────┤
│  getByRole       │  getByRole('button', { name: 'Submit' })     │
│  getByLabel      │  getByLabel('Email')                         │
│  getByPlaceholder│  getByPlaceholder('Enter email')             │
│  getByText       │  getByText('Welcome')                        │
│  getByAltText    │  getByAltText('Logo')                        │
│  getByTitle      │  getByTitle('Close')                         │
│  getByTestId     │  getByTestId('submit-btn')                   │
└──────────────────┴──────────────────────────────────────────────┘

ARIA (Accessible Rich Internet Applications):
├── 웹 콘텐츠를 스크린 리더가 이해할 수 있도록 하는 표준
├── role, aria-label, aria-hidden 등의 속성
└── getByRole은 이 ARIA 속성을 활용
```

### Auto-Wait 메커니즘

```
Playwright Auto-Wait 흐름:
┌─────────────────────────────────────────────────────────────────┐
│  액션 요청 (예: click)                                          │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐    No     ┌──────────┐                         │
│  │  Visible?   │──────────►│   대기   │                         │
│  └──────┬──────┘           └────┬─────┘                         │
│         │ Yes                   │                               │
│         ▼                       │                               │
│  ┌─────────────┐    No          │                               │
│  │   Stable?   │──────────►─────┘                               │
│  └──────┬──────┘                                                │
│         │ Yes                                                   │
│         ▼                                                       │
│  ┌─────────────┐    No                                          │
│  │  Enabled?   │──────────►─────┘                               │
│  └──────┬──────┘                                                │
│         │ Yes                                                   │
│         ▼                                                       │
│  ┌─────────────┐    No                                          │
│  │ Receivable? │──────────►─────┘                               │
│  └──────┬──────┘                                                │
│         │ Yes                                                   │
│         ▼                                                       │
│    액션 실행                                                    │
└─────────────────────────────────────────────────────────────────┘

상태 정의:
├── Visible    : DOM에 렌더링되고 화면에 보임
├── Stable     : 애니메이션/리사이징 완료
├── Enabled    : disabled 상태가 아님
└── Receivable : 다른 요소에 가려지지 않음
```

### Custom Wait 메서드

```
Custom Wait 종류:
┌──────────────────────┬──────────────────────────────────────────┐
│  메서드              │  용도                                    │
├──────────────────────┼──────────────────────────────────────────┤
│  waitForRequest      │  특정 요청 발생 대기                     │
│  waitForResponse     │  특정 응답 대기                          │
│  waitForLoadState    │  페이지 로드 상태                        │
│  waitForFunction     │  JS 함수 반환값 대기                     │
│  waitForEvent        │  이벤트 발생 대기                        │
│  waitForURL          │  URL 변경 대기                           │
│  waitForSelector     │  셀렉터 매칭 대기                        │
│  waitForTimeout      │  고정 시간 대기 (Anti-pattern!)          │
└──────────────────────┴──────────────────────────────────────────┘

waitForRequest vs waitForResponse:
┌───────────────────────────────────────────────────────────────┐
│  Browser ──► Server                                          │
│         │                                                     │
│         └──► waitForRequest 감지                              │
│                                                               │
│  Server ──► Browser                                          │
│         │                                                     │
│         └──► waitForResponse 감지                             │
└───────────────────────────────────────────────────────────────┘
```

### 다이얼로그 핸들링

```
다이얼로그 처리 흐름:
┌─────────────────────────────────────────────────────────────────┐
│  page.on('dialog') 또는 page.once('dialog')                     │
│       │                                                         │
│       ▼                                                         │
│  dialog 이벤트 발생                                             │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  dialog.type() 확인                                         ││
│  │  ├── 'alert'   → dialog.accept() 또는 dialog.dismiss()     ││
│  │  ├── 'confirm' → dialog.accept() 또는 dialog.dismiss()     ││
│  │  └── 'prompt'  → dialog.accept('입력값')                    ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

dialog 객체 메서드:
├── type()         : 다이얼로그 유형
├── message()      : 표시된 메시지
├── defaultValue() : prompt의 기본값
├── accept([value]): OK 클릭 (prompt는 값 전달)
└── dismiss()      : Cancel 클릭
```

### iframe 및 Shadow DOM

```
iframe 접근:
┌─────────────────────────────────────────────────────────────────┐
│  메인 페이지 (page)                                             │
│  │                                                              │
│  └── page.frameLocator('#iframe-id')                            │
│       │                                                         │
│       └── frameLocator.getByRole('button')                      │
└─────────────────────────────────────────────────────────────────┘

중첩 iframe:
page.frameLocator('#parent')
    .frameLocator('#child')
    .locator('input')

Shadow DOM 접근:
┌─────────────────────────────────────────────────────────────────┐
│  방법 1: 호스트 요소 통해 접근                                  │
│  page.locator('my-widget').locator('.internal-button')          │
│                                                                 │
│  방법 2: >>> 피어싱 셀렉터                                      │
│  page.locator('my-widget >>> .internal-button')                 │
└─────────────────────────────────────────────────────────────────┘

Shadow DOM 유형:
├── Open (mode: 'open')   : 접근 가능
└── Closed (mode: 'closed'): 접근 불가능 (웹 표준)
```

---

## 2. 비교표

### getBy* vs CSS/XPath 비교

| 특성 | getBy* 로케이터 | CSS/XPath |
|------|----------------|-----------|
| **안정성** | 높음 (의미 기반) | 낮음 (구조 기반) |
| **접근성** | ARIA 속성 활용 | 무관 |
| **유지보수** | 쉬움 | 어려움 (구조 변경에 취약) |
| **가독성** | 높음 | 복잡해지면 낮음 |
| **권장도** | 최우선 | 폴백 용도 |

### getBy* 로케이터 종류 비교

| 로케이터 | 용도 | 예시 HTML | 사용법 |
|----------|------|----------|--------|
| `getByRole` | ARIA 역할 | `<button>Submit</button>` | `getByRole('button', { name: 'Submit' })` |
| `getByLabel` | label 연결 | `<label for="email">Email</label>` | `getByLabel('Email')` |
| `getByPlaceholder` | placeholder | `<input placeholder="Enter email">` | `getByPlaceholder('Enter email')` |
| `getByText` | 텍스트 | `<span>Welcome</span>` | `getByText('Welcome')` |
| `getByTestId` | data-testid | `<div data-testid="card">` | `getByTestId('card')` |

### Wait 메서드 비교

| 메서드 | 감지 시점 | 주요 용도 |
|--------|----------|----------|
| `waitForRequest` | 요청 발송 시 | API 호출 트리거 확인 |
| `waitForResponse` | 응답 수신 시 | 응답 상태/내용 검증 |
| `waitForURL` | URL 변경 시 | SPA 페이지 전환 |
| `waitForLoadState` | 로드 상태 변경 시 | 페이지 로드 완료 |
| `waitForTimeout` | 고정 시간 후 | **사용 지양 (flaky 테스트 원인)** |

### 다이얼로그 유형 비교

| 유형 | 특징 | 처리 방법 |
|------|------|----------|
| `alert` | 알림만, OK 버튼 | `dialog.accept()` |
| `confirm` | 확인/취소 선택 | `dialog.accept()` 또는 `dialog.dismiss()` |
| `prompt` | 텍스트 입력 | `dialog.accept('입력값')` |

---

## 3. 면접 예상 질문 및 모범 답안

### Q1. getBy* 로케이터를 CSS/XPath보다 선호하는 이유는 무엇인가요?

**모범 답안:**

**핵심 이유: 안정성과 유지보수성**

```
getBy* 로케이터 장점:
├── 의미 기반 선택: UI 구조 변경에 강함
├── 접근성 표준 준수: ARIA 속성 활용
├── 사용자 관점: 실제 사용자가 보는 것으로 테스트
└── 가독성: 테스트 의도가 명확히 드러남
```

**비교 예시:**
```typescript
// 취약한 CSS 셀렉터 (구조 변경에 취약)
await page.locator('#form > div:nth-child(2) > button').click();

// 안정적인 getByRole (의미 기반)
await page.getByRole('button', { name: 'Submit' }).click();
```

CSS/XPath는 레거시 코드, 서드파티 컴포넌트, 접근성 속성이 없는 경우에만 폴백으로 사용합니다.

---

### Q2. Playwright의 Auto-wait 메커니즘이 어떻게 동작하나요?

**모범 답안:**

Playwright는 액션 수행 전 자동으로 **4가지 상태**를 확인합니다:

```
Auto-Wait 검사 순서:
1. Visible  : DOM에 렌더링되고 화면에 보이는가?
2. Stable   : 애니메이션/리사이징이 완료되었는가?
3. Enabled  : disabled 상태가 아닌가?
4. Receivable: 다른 요소에 가려지지 않는가?
```

**장점:**
- 대부분의 경우 명시적 대기 불필요
- Flaky 테스트 감소
- 코드 간결화

**Custom Wait가 필요한 경우:**
```typescript
// API 응답 대기
await page.waitForResponse(r => r.status() === 200);

// URL 변경 대기 (SPA)
await page.waitForURL('**/dashboard');

// 네트워크 유휴 상태 대기
await page.waitForLoadState('networkidle');
```

---

### Q3. `waitForRequest`와 `waitForResponse`의 차이점은?

**모범 답안:**

```
타임라인:
Browser ─── 요청 전송 ───► Server
         │
         └─► waitForRequest 감지 (요청 발송 시점)

Server ─── 응답 반환 ───► Browser
         │
         └─► waitForResponse 감지 (응답 수신 시점)
```

| 구분 | waitForRequest | waitForResponse |
|------|----------------|-----------------|
| 감지 시점 | 요청 발송 시 | 응답 수신 시 |
| 용도 | 요청이 전송되었는지 확인 | 응답 상태/내용 검증 |
| 예시 | API 호출 트리거 확인 | 200 OK 응답 확인 |

**사용 예시:**
```typescript
// 요청 전송 확인
await page.waitForRequest('**/api/users');

// 응답 상태 검증
const response = await page.waitForResponse(
  r => r.url().includes('/api/users') && r.status() === 200
);
```

---

### Q4. Shadow DOM 내부 요소에 어떻게 접근하나요?

**모범 답안:**

**두 가지 방법:**

```typescript
// 방법 1: 호스트 요소 통해 접근
const widget = page.locator('my-widget');
const button = widget.locator('.internal-button');
await button.click();

// 방법 2: >>> 피어싱 셀렉터
await page.locator('my-widget >>> .internal-button').click();

// 중첩된 Shadow DOM
await page.click('parent-component >>> child-component >>> button');
```

**주의사항:**
- **Open Shadow DOM**: 접근 가능
- **Closed Shadow DOM**: Playwright로도 접근 불가능 (웹 표준 제약)

Closed Shadow DOM이 있는 경우 컴포넌트 설계 변경이 필요합니다.

---

### Q5. iframe 내부 요소를 테스트하려면 어떻게 해야 하나요?

**모범 답안:**

```typescript
// 단일 iframe 접근
const frame = page.frameLocator('#myIframe');
await frame.getByRole('button', { name: 'Submit' }).click();

// 중첩 iframe 접근 (체이닝)
const parentFrame = page.frameLocator('#parentIframe');
const childFrame = parentFrame.frameLocator('#childIframe');
await childFrame.locator('input').fill('value');
```

**frameLocator vs contentFrame:**
```typescript
// 방법 1: frameLocator (권장)
const frame = page.frameLocator('#iframe');

// 방법 2: locator + contentFrame
const frame = page.locator('#iframe').contentFrame();
```

**주의:** Cross-origin iframe은 브라우저 보안 정책으로 접근 제한될 수 있습니다.

---

### Q6. 다이얼로그(alert, confirm, prompt) 핸들링 방법을 설명해주세요.

**모범 답안:**

```typescript
// 핸들러 등록 (액션 전에!)
page.on('dialog', async dialog => {
  console.log(`Type: ${dialog.type()}`);
  console.log(`Message: ${dialog.message()}`);

  if (dialog.type() === 'prompt') {
    await dialog.accept('입력값');  // 값 입력 후 OK
  } else if (dialog.type() === 'confirm') {
    await dialog.accept();          // OK 클릭
  } else {
    await dialog.dismiss();         // Cancel 클릭
  }
});

// 다이얼로그 트리거
await page.getByRole('button', { name: 'Show alert' }).click();
```

**핵심 포인트:**
- 핸들러는 **액션 전에** 등록
- 단일 다이얼로그: `page.once('dialog', ...)`
- 여러 다이얼로그: `page.on('dialog', ...)`

---

## 4. 실무 체크리스트

### 셀렉터 선택

- [ ] getBy* 로케이터를 최우선으로 사용
- [ ] 접근성 속성 없으면 getByTestId 사용
- [ ] CSS 셀렉터는 폴백으로만 사용
- [ ] `div:nth-child(3)` 같은 취약한 셀렉터 피하기

### 대기 전략

- [ ] Auto-wait로 충분한지 먼저 확인
- [ ] waitForTimeout 사용 피하기 (flaky 테스트 원인)
- [ ] API 호출 후 UI 변경은 waitForResponse 활용
- [ ] SPA 페이지 전환은 waitForURL 사용

### 다이얼로그 처리

- [ ] 핸들러는 액션 전에 등록
- [ ] dialog.type()으로 유형 확인 후 처리
- [ ] 단일/복수 다이얼로그에 따라 once/on 선택

### 특수 요소 처리

- [ ] iframe: frameLocator 사용
- [ ] Shadow DOM: >>> 피어싱 셀렉터 또는 호스트 요소 경유
- [ ] Cross-origin iframe 제약 사항 확인

---

## 5. 참고 자료

- [Playwright Locators 공식 문서](https://playwright.dev/docs/locators)
- [Playwright Auto-waiting](https://playwright.dev/docs/actionability)
- [Playwright Dialogs](https://playwright.dev/docs/dialogs)
- [Playwright Frames](https://playwright.dev/docs/frames)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Testing Library - Guiding Principles](https://testing-library.com/docs/guiding-principles)
