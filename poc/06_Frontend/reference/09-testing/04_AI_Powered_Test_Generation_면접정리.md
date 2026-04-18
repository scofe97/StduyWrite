# 04: AI-Powered Test Generation - 면접 정리

## 1. 핵심 개념 상세 설명

### Playwright Codegen

```
Codegen 구조:
┌─────────────────────────────────────────────────────────────────┐
│  npx playwright codegen https://example.com                     │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐             │
│  │   Browser Window    │    │  Playwright Inspector│             │
│  │  (상호작용 수행)    │ ◄──►│  (코드 자동 생성)    │             │
│  │                     │    │  - 언어 선택         │             │
│  │  클릭, 입력, 탐색   │    │  - Assertion 추가   │             │
│  │                     │    │  - 코드 복사/저장   │             │
│  └─────────────────────┘    └─────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘

지원 언어:
├── TypeScript (기본)
├── JavaScript
├── Python
├── C#
└── Java
```

**Codegen 명령어:**
```bash
# 기본 실행
npx playwright codegen https://example.com

# 특정 언어
npx playwright codegen --lang=python

# URL 없이 (수동 탐색)
npx playwright codegen
```

### Playwright MCP (Model Context Protocol)

```
MCP 아키텍처:
┌─────────────────────────────────────────────────────────────────┐
│  VS Code                                                        │
│  │                                                              │
│  └── GitHub Copilot (Agent 모드)                                │
│       │                                                         │
│       └── Playwright MCP Server                                 │
│            │                                                    │
│            └── 브라우저                                         │
│                 │                                               │
│                 └── 웹페이지 스냅샷 (Accessibility Tree)        │
│                      │                                          │
│                      ▼                                          │
│              AI가 페이지 구조 이해                              │
│                      │                                          │
│                      ▼                                          │
│              테스트 코드 생성                                   │
└─────────────────────────────────────────────────────────────────┘

설치:
code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'
```

### AI 생성 스크립트 개선

```
AI 생성 코드의 일반적인 문제:
┌─────────────────────────────────────────────────────────────────┐
│  문제                    │  해결 방법                          │
├──────────────────────────┼─────────────────────────────────────│
│  취약한 셀렉터           │  getByRole/getByText으로 변경       │
│  (div:nth-child(3))      │                                     │
├──────────────────────────┼─────────────────────────────────────│
│  대기 로직 누락          │  waitForSelector, expect 추가       │
├──────────────────────────┼─────────────────────────────────────│
│  에러 핸들링 없음        │  try-catch 블록 추가                │
├──────────────────────────┼─────────────────────────────────────│
│  결과 검증 없음          │  assertion 추가                     │
├──────────────────────────┼─────────────────────────────────────│
│  독립 스크립트 형식      │  test runner 형식으로 변환          │
└──────────────────────────┴─────────────────────────────────────┘
```

**Before/After 예시:**
```typescript
// AI 생성 (문제점 있음)
import { test } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://example.com/');
  await page.click('.btn');  // 취약한 셀렉터, 검증 없음
});

// 개선 후
import { test, expect } from '@playwright/test';

test('사용자가 버튼을 클릭하면 성공 메시지가 표시된다', async ({ page }) => {
  try {
    await page.goto('https://example.com/', { timeout: 30000 });
    await expect(page.getByText('Welcome')).toBeVisible();

    await page.getByRole('button', { name: 'Submit' }).click();
    await expect(page.getByText('Success')).toBeVisible();
  } catch (error) {
    console.error('테스트 실패:', error);
    throw error;
  }
});
```

### 폴백 로케이터 전략

```
폴백 로케이터 흐름:
┌─────────────────────────────────────────────────────────────────┐
│  요소 찾기 시도                                                 │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────┐                                            │
│  │ 1차: getByTestId│ ──성공──► 액션 수행                        │
│  └────────┬────────┘                                            │
│           │ 실패                                                │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │ 2차: getByRole  │ ──성공──► 액션 수행                        │
│  └────────┬────────┘                                            │
│           │ 실패                                                │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │ 3차: getByText  │ ──성공──► 액션 수행                        │
│  └────────┬────────┘                                            │
│           │ 실패                                                │
│           ▼                                                     │
│      에러 throw                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**구현 예시:**
```typescript
const locators = [
  page.getByTestId('submit-button'),
  page.getByRole('button', { name: 'Submit' }),
  page.getByText('Submit'),
];

for (const locator of locators) {
  try {
    await locator.click({ timeout: 5000 });
    return;  // 성공 시 종료
  } catch {
    console.warn(`Locator failed, trying next...`);
  }
}

throw new Error('All locators failed');
```

### Self-Healing 개념

```
Self-Healing 동작 원리:
┌─────────────────────────────────────────────────────────────────┐
│  1. 초기 학습                                                   │
│     요소의 여러 속성 수집: 텍스트, 위치, 크기, ID, 클래스 등    │
│                                                                 │
│  2. 테스트 실행                                                 │
│     기존 셀렉터로 요소 찾기 시도                                │
│          │                                                      │
│          ├── 성공 → 테스트 계속                                 │
│          │                                                      │
│          └── 실패 → AI 분석                                     │
│                    │                                            │
│                    ▼                                            │
│              수집된 속성으로 유사 요소 탐색                     │
│                    │                                            │
│                    ├── 발견 → 셀렉터 자동 업데이트 + 로그       │
│                    │                                            │
│                    └── 미발견 → 테스트 실패                     │
└─────────────────────────────────────────────────────────────────┘

Self-Healing 도구:
├── Testim: ML 기반 셀렉터 자동 수정
├── Mabl: 자동 복구 + 시각적 테스트
└── Healenium: 오픈소스 Self-Healing 라이브러리
```

---

## 2. 비교표

### Codegen vs MCP 비교

| 구분 | Codegen | MCP + Copilot |
|------|---------|---------------|
| **동작 방식** | 사용자 액션 녹화 | AI 자율 탐색 |
| **입력** | 마우스/키보드 조작 | 자연어 프롬프트 |
| **출력** | 기본 스크립트 | 완성도 높은 테스트 |
| **복잡도 처리** | 단순 플로우 | 복잡한 시나리오 가능 |
| **로직 포함** | 없음 | 조건문, 반복문 가능 |
| **권장 용도** | 빠른 프로토타입 | 복잡한 테스트 생성 |

### AI 생성 코드 문제점 및 해결

| 문제 | 증상 | 해결 방법 |
|------|------|----------|
| 취약한 셀렉터 | `div:nth-child(3)` | getBy* 로케이터로 변경 |
| 대기 로직 누락 | 요소 못 찾음 에러 | waitFor*, expect 추가 |
| 에러 핸들링 없음 | 스택 트레이스만 출력 | try-catch 블록 |
| 결과 검증 없음 | 클릭만 하고 끝 | assertion 추가 |
| 독립 스크립트 | chromium.launch() 사용 | test() 형식으로 변환 |

### 재시도 로직 비교

| 방법 | 코드 | 장점 | 단점 |
|------|------|------|------|
| `expect().toPass()` | `await expect(async () => {...}).toPass()` | 간결, 내장 | 유연성 제한 |
| 커스텀 함수 | `retryAction(fn, maxAttempts)` | 완전 제어 | 코드 증가 |

### Self-Healing 트레이드오프

| 장점 | 단점 |
|------|------|
| 테스트 유지보수 시간 감소 | 실행 속도 저하 |
| UI 변경에 강한 내성 | 대규모 리디자인에는 여전히 취약 |
| 신뢰할 수 있는 테스트 결과 | 너무 관대하면 실제 버그 놓침 |
| - | 구현 복잡성 증가 |

---

## 3. 면접 예상 질문 및 모범 답안

### Q1. Playwright Codegen의 용도와 한계는?

**모범 답안:**

**용도:**
- 테스트 스크립트 빠른 프로토타이핑
- 셀렉터 탐색 (Pick Locator 도구)
- 기본 플로우 녹화

**한계:**
```
Codegen 한계:
├── 단순 플로우만 캡처 (복잡한 시나리오 X)
├── 조건문, 반복문, 에러 핸들링 없음
├── 취약한 셀렉터 생성 가능
└── assertion이 부족할 수 있음
```

**권장 사용법:**
1. Codegen으로 기본 스크립트 생성
2. 셀렉터를 getBy* 로케이터로 개선
3. assertion 추가
4. 에러 핸들링 추가

---

### Q2. AI 생성 테스트 코드의 주요 개선 포인트는?

**모범 답안:**

**5가지 핵심 개선 포인트:**

```typescript
// 1. 취약한 셀렉터 → role 기반으로
// Bad:  await page.click('.btn');
// Good: await page.getByRole('button', { name: 'Submit' }).click();

// 2. 대기 로직 추가
await expect(page.getByText('Welcome')).toBeVisible();

// 3. 에러 핸들링
try {
  await page.goto('https://example.com');
} catch (error) {
  console.error('Navigation failed:', error);
  throw error;
}

// 4. 결과 검증 (assertion)
await page.getByRole('button').click();
await expect(page.getByText('Success')).toBeVisible();  // 필수!

// 5. test runner 형식으로 변환
// Bad:  const browser = await chromium.launch();
// Good: test('name', async ({ page }) => { ... });
```

**핵심 원칙:** "액션만 하지 말고, 결과를 검증하라"

---

### Q3. 폴백 로케이터 전략이란 무엇이고 왜 필요한가요?

**모범 답안:**

**정의:** 여러 로케이터를 우선순위대로 시도하여 UI 변경에도 테스트가 깨지지 않도록 하는 전략

**필요성:**
```
UI 변경 시나리오:
├── data-testid가 제거됨 → 2순위 로케이터로 시도
├── 버튼 텍스트가 변경됨 → 다른 속성으로 시도
└── 클래스명이 변경됨 → 의미 기반 로케이터로 시도
```

**구현:**
```typescript
const locators = [
  page.getByTestId('submit'),      // 1순위
  page.getByRole('button', { name: 'Submit' }),  // 2순위
  page.getByText('Submit'),        // 3순위
];

for (const locator of locators) {
  try {
    await locator.click({ timeout: 5000 });
    return;
  } catch {
    continue;
  }
}

throw new Error('All locators failed');
```

테스트 안정성을 높이고, 소소한 UI 변경에도 테스트가 깨지지 않습니다.

---

### Q4. `expect().toPass()`와 커스텀 재시도 로직의 차이는?

**모범 답안:**

**expect().toPass():**
```typescript
await expect(async () => {
  await page.getByText('Login').click();
}).toPass({
  timeout: 3000,   // 최대 3초
  interval: 1000,  // 1초 간격
});
```
- 장점: 간결, Playwright 내장
- 단점: 간단한 재시도만 가능

**커스텀 재시도:**
```typescript
async function retryAction(action, maxAttempts = 3) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await action();
      return;
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}
```
- 장점: 완전한 제어 (로깅, 조건부 재시도)
- 단점: 코드 증가

**선택 기준:**
- 단순 재시도 → `expect().toPass()`
- 복잡한 로직 필요 → 커스텀 함수

---

### Q5. Self-Healing 테스트의 장단점은?

**모범 답안:**

**장점:**
```
├── 테스트 유지보수 시간 감소
├── UI 변경에 강한 내성
└── 테스트 안정성 향상
```

**단점:**
```
├── 실행 속도 저하 (대체 셀렉터 탐색)
├── 대규모 리디자인에는 여전히 취약
├── 너무 관대하면 실제 버그를 놓칠 수 있음
└── 구현 복잡성 증가
```

**Playwright와의 관계:**
Playwright 자체에는 Self-Healing 기능이 없습니다. 상용 도구(Testim, Mabl)나 오픈소스(Healenium)로 구현 가능합니다.

**소규모 프로젝트에서는** 폴백 로케이터 전략으로 충분하고, Self-Healing 도입 비용이 이점보다 클 수 있습니다.

---

### Q6. MCP를 활용한 테스트 생성의 장점과 주의사항은?

**모범 답안:**

**장점:**
```
├── 자연어로 테스트 작성
├── 소스 코드 접근 없이 자동화 가능
├── AI가 페이지 구조를 분석하여 최적 셀렉터 선택
└── 80-90% 완성도의 테스트 생성
```

**주의사항:**
```
├── AI 생성 코드를 그대로 사용하지 말 것
├── 셀렉터, assertion 검토 필수
├── 민감 정보(비밀번호 등) 입력 금지
└── 나머지 10-20%는 수동 개선 필요
```

**워크플로우:**
1. 자연어로 테스트 요구사항 작성
2. MCP + Copilot이 테스트 생성
3. 생성된 코드 검토 및 개선
4. 테스트 실행 및 검증

---

## 4. 실무 체크리스트

### Codegen 사용

- [ ] 기본 스크립트 녹화 후 반드시 개선
- [ ] Pick Locator로 최적 셀렉터 확인
- [ ] assertion 아이콘으로 검증 추가
- [ ] 녹화된 셀렉터가 취약하지 않은지 확인

### AI 생성 코드 개선

- [ ] 취약한 셀렉터 → getBy* 로케이터로 변경
- [ ] 대기 로직 추가 (waitFor*, expect)
- [ ] try-catch로 에러 핸들링
- [ ] 결과 검증 assertion 추가
- [ ] test() 형식으로 변환

### 폴백 로케이터

- [ ] 우선순위대로 로케이터 배열 구성
- [ ] 적절한 timeout 설정
- [ ] 최대 시도 횟수 제한
- [ ] 실패 시 명확한 에러 메시지

### Self-Healing 검토

- [ ] 프로젝트 규모에 맞는지 평가
- [ ] 도입 비용 vs 이점 분석
- [ ] 너무 관대하지 않은지 확인

---

## 5. 참고 자료

- [Playwright Codegen 공식 문서](https://playwright.dev/docs/codegen)
- [Playwright Locators](https://playwright.dev/docs/locators)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Testim](https://www.testim.io/)
- [Mabl](https://www.mabl.com/)
- [Healenium](https://github.com/healenium/healenium)
