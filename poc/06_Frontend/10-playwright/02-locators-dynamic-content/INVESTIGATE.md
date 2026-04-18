# 02. 로케이터와 동적 콘텐츠 - 조사 (INVESTIGATE)

**작성일**: 2026-02-05
**목표**: Playwright의 다양한 로케이터 전략과 동적 콘텐츠 처리 방법 이해
**학습 유형**: 조사 및 탐구

---

## 핵심 질문 (5개)

### 1. getByRole, getByLabel, getByText, getByTestId - 각각 언제 사용하는가? 우선순위는?

**탐구 목표**: 각 로케이터의 적용 상황과 우선순위 기준을 파악합니다.

**질문 세부사항**:
- getByRole은 접근성 역할(button, textbox 등)을 사용합니다. 어떤 상황에서 최우선으로 선택해야 하나요?
- getByLabel은 폼 요소(input, select 등)와 연결된 label을 찾습니다. 언제 getByRole 대신 사용하나요?
- getByText는 화면에 보이는 텍스트를 찾습니다. 왜 getByRole보다 낮은 우선순위인가요?
- getByTestId는 data-testid 속성을 사용합니다. "최후의 수단"이라고 하는 이유는?

**탐구 활동**:
```typescript
// 활동 1: TPS 티켓 상세 페이지에서 버튼 찾기
// localhost:3002/ticket/123 페이지에서 다음 방법들을 시도해보세요

// 방법 A: getByRole (권장)
await page.getByRole('button', { name: '등록(CI/CD)' }).click();

// 방법 B: getByText
await page.getByText('등록(CI/CD)').click();

// 방법 C: getByTestId
await page.getByTestId('submit-ticket-btn').click();

// 질문: 위 3가지 방법 중 어떤 것이 가장 견고한가요? 왜 그런가요?
```

**TPS 기반 실제 예시**:
```typescript
// TPS 티켓 목록에서 특정 상태의 티켓 찾기
// 시나리오: "진행 중" 상태의 첫 번째 티켓의 제목을 클릭

// 방법 1: Role + 필터 (추천)
await page
  .getByRole('row')
  .filter({ hasText: '진행 중' })
  .first()
  .getByRole('link')
  .click();

// 방법 2: TestId (유지보수성 낮음)
await page.getByTestId('ticket-row-진행중').getByTestId('ticket-title-link').click();

// 비교: 방법 1은 UI가 변경되어도 작동하지만, 방법 2는 testid 변경 시 깨집니다.
```

---

### 2. CSS 셀렉터와 XPath를 "최후의 수단"이라고 하는 이유는?

**탐구 목표**: CSS/XPath의 단점과 대안을 이해합니다.

**질문 세부사항**:
- CSS 셀렉터는 DOM 구조에 의존합니다. 이것이 왜 문제인가요?
- XPath는 더 강력하지만 더 취약합니다. 어떤 점에서 그런가요?
- "구현 세부사항에 결합"된다는 것은 무엇을 의미하나요?
- 리팩토링이나 디자인 변경 시 어떤 영향을 받나요?

**탐구 활동**:
```typescript
// 활동 2: 취약한 셀렉터 vs 견고한 셀렉터 비교
// localhost:3002/ticket-list 페이지에서 검색 버튼 찾기

// ❌ 취약: CSS 셀렉터 (DOM 구조 의존)
await page.locator('div.header > div.search-bar > button.search-btn').click();
// 문제점: div 구조가 변경되면 즉시 깨집니다.

// ❌ 취약: XPath (경로 의존)
await page.locator('//div[@class="header"]/div[@class="search-bar"]/button[1]').click();
// 문제점: 클래스명이나 순서가 변경되면 깨집니다.

// ✅ 견고: getByRole
await page.getByRole('button', { name: '검색' }).click();
// 장점: 버튼 텍스트만 유지되면 DOM 구조와 무관하게 작동합니다.

// 실험: mock-server의 HTML을 수정하여 div 구조를 변경해보세요.
// 어떤 셀렉터가 계속 작동하나요?
```

**실험 과제**:
1. `mock-server/pages/ticket-list.html`에서 버튼의 부모 div를 제거
2. 위 3가지 셀렉터를 다시 실행
3. 어떤 것이 계속 작동하는지 확인

---

### 3. Playwright의 다이얼로그(alert, confirm, prompt) 처리 방식은? (page.on('dialog'))

**탐구 목표**: 브라우저 네이티브 다이얼로그를 자동화하는 방법을 이해합니다.

**질문 세부사항**:
- JavaScript의 `alert()`, `confirm()`, `prompt()`는 테스트를 어떻게 차단하나요?
- `page.on('dialog')` 이벤트는 언제 발생하나요?
- `dialog.accept()` vs `dialog.dismiss()`의 차이는?
- 다이얼로그 메시지를 검증하는 방법은?

**탐구 활동**:
```typescript
// 활동 3: TPS 티켓 삭제 확인 다이얼로그 처리
// localhost:3002/ticket/123 페이지에서 삭제 버튼 테스트

test('티켓 삭제 시 confirm 다이얼로그 처리', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket/123');

  // 다이얼로그 이벤트 리스너 등록 (버튼 클릭 전에 설정!)
  page.on('dialog', async (dialog) => {
    console.log('다이얼로그 타입:', dialog.type()); // 'alert', 'confirm', 'prompt'
    console.log('다이얼로그 메시지:', dialog.message());

    // 실험 1: 승인
    await dialog.accept();

    // 실험 2: 거부 (주석 해제)
    // await dialog.dismiss();
  });

  // 삭제 버튼 클릭 → confirm("정말 삭제하시겠습니까?") 발생
  await page.getByRole('button', { name: '삭제' }).click();

  // 질문: accept()와 dismiss()일 때 페이지 상태가 어떻게 다른가요?
});
```

**실험 과제**:
1. `dialog.accept()` → 티켓이 삭제됩니까?
2. `dialog.dismiss()` → 티켓이 유지됩니까?
3. `dialog.message()`로 메시지를 검증해보세요.

---

### 4. iframe 내부 요소에 접근하는 방법은? (frameLocator)

**탐구 목표**: 중첩된 프레임 컨텍스트를 다루는 방법을 이해합니다.

**질문 세부사항**:
- iframe은 별도의 DOM 트리를 가집니다. 왜 일반 locator로는 접근할 수 없나요?
- `frameLocator()`와 `locator()`의 차이는?
- 중첩된 iframe(iframe 안의 iframe)은 어떻게 접근하나요?
- iframe이 로드될 때까지 기다리는 방법은?

**탐구 활동**:
```typescript
// 활동 4: iframe 내부의 임베디드 컨텐츠 접근
// localhost:3002/embedded-content 페이지 테스트

test('iframe 내부 버튼 클릭', async ({ page }) => {
  await page.goto('http://localhost:3002/embedded-content');

  // ❌ 작동하지 않음: 일반 locator
  // await page.getByRole('button', { name: 'Submit' }).click();
  // 이유: iframe 내부는 별도 컨텍스트

  // ✅ 작동: frameLocator 사용
  const frame = page.frameLocator('#embedded-form-iframe');
  await frame.getByRole('button', { name: 'Submit' }).click();

  // 중첩된 iframe 예시
  const outerFrame = page.frameLocator('#outer-iframe');
  const innerFrame = outerFrame.frameLocator('#inner-iframe');
  await innerFrame.getByText('Click me').click();
});
```

**실험 과제**:
1. DevTools에서 iframe의 DOM을 확인
2. iframe 없이 접근 시도 → 실패 확인
3. frameLocator로 접근 → 성공 확인

---

### 5. Shadow DOM 요소를 어떻게 선택하는가?

**탐구 목표**: Web Components의 Shadow DOM을 다루는 방법을 이해합니다.

**질문 세부사항**:
- Shadow DOM은 왜 일반 셀렉터로 접근할 수 없나요?
- Playwright는 Shadow DOM을 자동으로 뚫고 들어가나요?
- `locator()` vs `locator().locator()`의 차이는?
- Shadow Host와 Shadow Root의 관계는?

**탐구 활동**:
```typescript
// 활동 5: Shadow DOM 내부 요소 접근
// localhost:3002/web-components 페이지 테스트

test('Shadow DOM 요소 접근', async ({ page }) => {
  await page.goto('http://localhost:3002/web-components');

  // Playwright는 자동으로 Shadow DOM을 관통합니다!
  // 특별한 처리 없이 일반 locator 사용 가능
  await page.getByRole('button', { name: 'Click Me' }).click();

  // 만약 수동으로 접근해야 한다면 (레거시)
  const shadowHost = page.locator('my-custom-element');
  const shadowButton = shadowHost.locator('button');
  await shadowButton.click();

  // 질문: Playwright의 자동 Shadow DOM 관통은 어떤 이점이 있나요?
});
```

**실험 과제**:
1. DevTools에서 #shadow-root (open) 확인
2. 일반 document.querySelector()로 접근 시도 → 실패
3. Playwright locator로 접근 → 성공

---

## 실전 시나리오: TPS 티켓 목록 필터링

**시나리오**: TPS 티켓 목록에서 특정 상태의 티켓을 찾고 클릭하는 테스트 작성

```typescript
test('TPS 티켓 목록에서 "완료" 상태 티켓 찾기', async ({ page }) => {
  await page.goto('http://localhost:3002/ticket-list');

  // 질문 1: 어떤 로케이터가 가장 적절한가?
  // Option A: getByRole + filter
  // Option B: CSS 셀렉터
  // Option C: XPath

  // 추천 답안: Option A
  const completedTickets = page
    .getByRole('row')
    .filter({ hasText: '완료' });

  // 첫 번째 완료 티켓의 제목 클릭
  await completedTickets.first().getByRole('link').click();

  // 검증: 상세 페이지로 이동했는가?
  await expect(page).toHaveURL(/\/ticket\/\d+/);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
```

**탐구 질문**:
1. `filter({ hasText: '완료' })` 대신 `filter({ has: page.getByText('완료') })`를 사용하면 어떻게 다른가요?
2. `first()` 대신 `nth(0)`을 사용해도 되나요?
3. 티켓이 없을 때 어떤 에러가 발생하나요?

---

## 다음 단계

### 학습 문서로 이동
→ `LEARN.md`에서 체계적인 개념 정리와 패턴 학습

### 실습 과제
→ `practice/` 폴더에서 실제 코드 작성

### 확인 사항
- [ ] 5가지 핵심 질문에 대한 답을 찾았나요?
- [ ] 모든 탐구 활동을 실행해보았나요?
- [ ] TPS 기반 예시를 이해했나요?
- [ ] 실험 과제를 완료했나요?

---

**다음 학습**: `LEARN.md`에서 로케이터 전략 피라미드와 실전 패턴 학습
