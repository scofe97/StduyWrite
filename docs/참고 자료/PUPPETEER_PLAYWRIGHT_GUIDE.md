# Puppeteer & Playwright 가이드

웹 브라우저 자동화 및 스크린샷 캡처를 위한 도구 비교 및 사용법입니다.

---

## Puppeteer vs Playwright 비교

| 항목 | Puppeteer | Playwright |
|------|-----------|------------|
| 개발사 | Google | Microsoft (전 Puppeteer 팀) |
| 브라우저 | Chrome/Chromium 중심 | Chrome, Firefox, Safari 모두 지원 |
| 언어 | JavaScript/TypeScript | JS/TS, Python, Java, .NET |
| 설치 | `npm install puppeteer` | `npm install playwright` |
| 권장 | 레거시 프로젝트 | **신규 프로젝트 권장** |

**결론**: **Playwright 권장** - 더 많은 브라우저, 더 안정적, 활발한 개발

---

## Claude Code에서 사용하기

### MCP 서버 (이미 설정됨)

Claude Code에 Playwright MCP 서버가 등록되어 있다면:

```bash
# MCP 서버 확인
claude mcp list
```

### 직접 스크립트 사용

```bash
# Playwright 설치
npm install playwright
npx playwright install  # 브라우저 다운로드
```

---

## 주요 기능

### 1. 스크린샷 캡처

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('https://example.com');

  // 전체 페이지 스크린샷
  await page.screenshot({ path: 'screenshot.png', fullPage: true });

  // 특정 요소만
  await page.locator('#header').screenshot({ path: 'header.png' });

  await browser.close();
})();
```

### 2. PDF 생성

```javascript
await page.pdf({
  path: 'page.pdf',
  format: 'A4',
  printBackground: true
});
```

### 3. 웹 요소 제어

```javascript
// 클릭
await page.click('button#submit');

// 텍스트 입력
await page.fill('input[name="email"]', 'test@example.com');

// 선택
await page.selectOption('select#country', 'KR');

// 대기
await page.waitForSelector('.loaded');
```

### 4. 네트워크 가로채기

```javascript
await page.route('**/*.png', route => route.abort());  // 이미지 차단

await page.route('**/api/*', route => {
  console.log('API 요청:', route.request().url());
  route.continue();
});
```

---

## Python 버전 (Playwright)

```bash
pip install playwright
playwright install
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto('https://example.com')
    page.screenshot(path='screenshot.png', full_page=True)

    browser.close()
```

---

## 실용 예제

### 웹페이지 모니터링

```javascript
const { chromium } = require('playwright');

async function monitor(url, selector) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(url);
  const text = await page.locator(selector).textContent();

  console.log(`현재 값: ${text}`);

  await page.screenshot({
    path: `monitor_${Date.now()}.png`,
    fullPage: false
  });

  await browser.close();
  return text;
}

// 사용
monitor('https://example.com/status', '.status-text');
```

### 로그인 후 데이터 추출

```javascript
const { chromium } = require('playwright');

async function scrapeAfterLogin(url, credentials) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // 로그인
  await page.goto(url + '/login');
  await page.fill('#username', credentials.username);
  await page.fill('#password', credentials.password);
  await page.click('button[type="submit"]');

  // 로그인 완료 대기
  await page.waitForURL(url + '/dashboard');

  // 데이터 추출
  const data = await page.locator('.data-table').innerHTML();

  // 스크린샷
  await page.screenshot({ path: 'dashboard.png' });

  await browser.close();
  return data;
}
```

### 여러 페이지 순회

```javascript
const urls = [
  'https://example.com/page1',
  'https://example.com/page2',
  'https://example.com/page3'
];

async function crawlPages(urls) {
  const browser = await chromium.launch();
  const results = [];

  for (const url of urls) {
    const page = await browser.newPage();
    await page.goto(url);

    results.push({
      url,
      title: await page.title(),
      screenshot: `screenshot_${urls.indexOf(url)}.png`
    });

    await page.screenshot({ path: results[results.length - 1].screenshot });
    await page.close();
  }

  await browser.close();
  return results;
}
```

---

## CLI 사용법

### Playwright CLI

```bash
# 코드 생성기 (녹화 모드)
npx playwright codegen https://example.com

# 스크린샷
npx playwright screenshot https://example.com screenshot.png

# PDF
npx playwright pdf https://example.com page.pdf
```

### 헤드리스 vs 헤드풀

```javascript
// 헤드리스 (UI 없음, 서버용)
const browser = await chromium.launch({ headless: true });

// 헤드풀 (UI 표시, 디버깅용)
const browser = await chromium.launch({ headless: false });

// 슬로우 모션 (디버깅)
const browser = await chromium.launch({
  headless: false,
  slowMo: 500  // 500ms 딜레이
});
```

---

## 트러블슈팅

### 브라우저 설치 오류

```bash
# 브라우저 재설치
npx playwright install --force

# 특정 브라우저만
npx playwright install chromium
```

### 타임아웃 오류

```javascript
// 타임아웃 증가
await page.goto(url, { timeout: 60000 });  // 60초

// 전역 타임아웃
const browser = await chromium.launch();
const context = await browser.newContext();
context.setDefaultTimeout(30000);  // 30초
```

### 셀렉터 찾기 어려움

```javascript
// 텍스트로 찾기
await page.getByText('로그인').click();

// 역할로 찾기
await page.getByRole('button', { name: '제출' }).click();

// 라벨로 찾기
await page.getByLabel('이메일').fill('test@test.com');
```

---

## Claude Code 스킬 연동

`.claude/skills/browser-automation/SKILL.md` 생성하여 활용 가능:

```markdown
# Browser Automation Skill

## 트리거
- "스크린샷", "웹 캡처", "페이지 저장" 요청 시

## 워크플로우
1. Playwright 스크립트 생성
2. 실행 및 결과 저장
3. 스크린샷/PDF 확인
```

---

## 참조

- [Playwright 공식 문서](https://playwright.dev/)
- [Puppeteer 공식 문서](https://pptr.dev/)
- [Playwright Python](https://playwright.dev/python/)
