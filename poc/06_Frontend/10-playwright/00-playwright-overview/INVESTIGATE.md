# 00. Playwright 개론 - 조사 (INVESTIGATE)

> Playwright를 깊이 이해하기 위한 사전 질문들입니다.

---

## 핵심 질문

### 1. E2E 테스트 도구 비교
- Selenium, Cypress, Playwright 각각의 아키텍처 차이는?
- Playwright가 후발주자인데도 선택되는 이유는?
- "브라우저 컨텍스트" 개념이 왜 Playwright에서 중요한가?

### 2. Playwright Test vs Playwright Library
- `@playwright/test`와 `playwright` 패키지의 차이는?
- 왜 두 가지를 분리했을까?
- 기존 Jest 환경에서 Playwright Library를 선택하는 것이 더 나은 경우는?

### 3. Playwright 아키텍처
- Playwright는 브라우저와 어떻게 통신하는가?
- CDP(Chrome DevTools Protocol)와의 관계는?
- "하나의 API, 세 개의 브라우저"가 가능한 이유는?

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Test Script │────▶│  Playwright  │────▶│   Browser    │
│  (Node.js)   │     │   Server     │     │  (실제 브라우저) │
└──────────────┘     └──────────────┘     └──────────────┘
                          ▲
                          │
                     어떤 프로토콜?
```

### 4. Auto-Wait 메커니즘
- Playwright의 auto-wait이란 무엇인가?
- Cypress의 자동 재시도와 어떻게 다른가?
- `waitForSelector`를 직접 쓸 필요가 없는 이유는?

### 5. 테스트 격리 (Test Isolation)
- 각 테스트가 독립적으로 실행된다는 것은 무슨 의미인가?
- Browser Context가 테스트 격리에 어떤 역할을 하는가?
- storageState를 활용한 인증 상태 재사용은 어떻게 작동하는가?

---

## 탐색 활동

### 활동 1: E2E 도구 비교표 완성

| 항목 | Selenium | Cypress | Playwright |
|------|----------|---------|------------|
| 출시년도 | 2004 | 2017 | ? |
| 아키텍처 | WebDriver | ? | ? |
| 지원 브라우저 | 모든 브라우저 | Chromium, Firefox | ? |
| 언어 지원 | 다수 | JS/TS만 | ? |
| 병렬 실행 | Grid 필요 | ? | ? |
| Auto-wait | ❌ | ✅ | ? |
| 네트워크 가로채기 | ❌ | ✅ | ? |

### 활동 2: Playwright 공식 문서 탐색
- https://playwright.dev/docs/intro 를 읽고 핵심 기능 3가지를 적어보세요

---

## 생각해볼 점

1. 왜 Microsoft가 E2E 테스트 도구를 만들었을까?
2. Playwright가 Puppeteer에서 fork되었다는데, 어떤 부분이 달라졌을까?
3. 모바일 브라우저 테스트가 Playwright에서 가능한가? 어떤 방식으로?

---

## 참고 키워드
- Browser Context
- CDP (Chrome DevTools Protocol)
- Auto-waiting
- Test Isolation
- Playwright vs Cypress vs Selenium

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
