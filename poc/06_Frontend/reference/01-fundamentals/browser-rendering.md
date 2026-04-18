# 브라우저 렌더링

## 개요

**정의**: 브라우저 렌더링은 HTML, CSS, JavaScript를 파싱하여 화면에 픽셀을 그리는 과정으로, Critical Rendering Path를 통해 수행된다.

**목적**: 렌더링 과정 이해를 통해 성능 병목을 식별하고, Reflow/Repaint를 최소화하여 사용자 경험을 최적화한다.

---

## 핵심 개념

### Critical Rendering Path

```
┌─────────────────────────────────────────────────────────────────┐
│                   Critical Rendering Path                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   HTML                     CSS                                   │
│    │                        │                                    │
│    ▼                        ▼                                    │
│  ┌─────────┐           ┌─────────┐                              │
│  │  DOM    │           │ CSSOM   │                              │
│  │  Tree   │           │  Tree   │                              │
│  └────┬────┘           └────┬────┘                              │
│       │                     │                                    │
│       └──────────┬──────────┘                                   │
│                  │                                               │
│                  ▼                                               │
│            ┌──────────┐                                         │
│            │  Render  │                                         │
│            │   Tree   │                                         │
│            └────┬─────┘                                         │
│                 │                                                │
│                 ▼                                                │
│            ┌──────────┐                                         │
│            │  Layout  │  ← 위치, 크기 계산 (Reflow)              │
│            └────┬─────┘                                         │
│                 │                                                │
│                 ▼                                                │
│            ┌──────────┐                                         │
│            │  Paint   │  ← 픽셀 채우기 (Repaint)                 │
│            └────┬─────┘                                         │
│                 │                                                │
│                 ▼                                                │
│            ┌──────────┐                                         │
│            │Composite │  ← 레이어 합성 (GPU)                     │
│            └──────────┘                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 렌더링 단계 상세

| 단계 | 설명 | 입력 | 출력 |
|------|------|------|------|
| **DOM 구축** | HTML 파싱 | HTML 바이트 | DOM Tree |
| **CSSOM 구축** | CSS 파싱 | CSS 바이트 | CSSOM Tree |
| **Render Tree** | DOM + CSSOM 결합 | DOM, CSSOM | Render Tree |
| **Layout** | 위치/크기 계산 | Render Tree | Box Model |
| **Paint** | 픽셀 그리기 | Layout | 레이어 비트맵 |
| **Composite** | 레이어 합성 | Paint 레이어 | 최종 화면 |

---

### DOM 구축

```
HTML 바이트 → 문자열 → 토큰 → 노드 → DOM Tree

<html>
  <head>
    <title>Page</title>
  </head>
  <body>
    <div class="container">
      <p>Hello</p>
    </div>
  </body>
</html>

           ┌──────────┐
           │   html   │
           └────┬─────┘
        ┌───────┴───────┐
        ▼               ▼
   ┌────────┐      ┌────────┐
   │  head  │      │  body  │
   └────┬───┘      └────┬───┘
        ▼               ▼
   ┌────────┐      ┌────────────┐
   │ title  │      │    div     │
   │ "Page" │      │ .container │
   └────────┘      └─────┬──────┘
                         ▼
                    ┌─────────┐
                    │    p    │
                    │ "Hello" │
                    └─────────┘
```

---

### CSSOM 구축

```
CSS 바이트 → 문자열 → 토큰 → 노드 → CSSOM Tree

body { font-size: 16px; }
.container { width: 100%; }
p { color: blue; }

           ┌──────────────────┐
           │      body        │
           │ font-size: 16px  │
           └────────┬─────────┘
                    │
                    ▼
           ┌────────────────────┐
           │    .container      │
           │    width: 100%     │
           │ (font-size: 16px)  │  ← 상속
           └────────┬───────────┘
                    │
                    ▼
           ┌──────────────────┐
           │        p         │
           │   color: blue    │
           │ (font-size: 16px)│  ← 상속
           └──────────────────┘
```

**CSSOM 특성**:
- CSS는 렌더링 차단 리소스 (render-blocking)
- 전체 CSS가 파싱되어야 CSSOM 완성
- 미디어 쿼리로 조건부 로딩 가능

---

### Render Tree 구축

```
DOM + CSSOM = Render Tree

특징:
- display: none 요소는 제외
- visibility: hidden 요소는 포함 (공간 차지)
- ::before, ::after 가상 요소 포함

   Render Tree
   ┌─────────────────────────────┐
   │ body                        │
   │ font-size: 16px             │
   └─────────────┬───────────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │ div.container               │
   │ width: 100%                 │
   └─────────────┬───────────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │ p                           │
   │ color: blue                 │
   │ content: "Hello"            │
   └─────────────────────────────┘
```

---

### Layout (Reflow)

**정의**: 각 요소의 정확한 위치와 크기를 계산하는 과정

```javascript
// Layout 발생 원인
element.offsetWidth;      // 강제 동기 레이아웃
element.clientHeight;     // 강제 동기 레이아웃
element.getBoundingClientRect();

// 레이아웃 트리거 속성
width, height, padding, margin, border
position, top, left, right, bottom
display, float, overflow
font-size, font-family, font-weight
```

**Reflow 범위**:

| 범위 | 설명 | 성능 영향 |
|------|------|----------|
| **Global** | 전체 문서 재계산 | 매우 큼 |
| **Incremental** | 변경된 부분만 | 중간 |
| **Isolated** | 독립 레이어만 | 작음 |

---

### Paint (Repaint)

**정의**: 레이아웃 계산 결과를 바탕으로 픽셀을 채우는 과정

```
Paint 순서 (Stacking Context):
1. 배경색
2. 배경 이미지
3. 테두리
4. 자식 요소
5. 아웃라인

Paint 트리거 속성 (Layout 없이 Paint만):
- color, background, visibility
- box-shadow, border-radius
- outline
```

---

### Composite

**정의**: 여러 레이어를 최종 화면으로 합성하는 GPU 작업

```
┌─────────────────────────────────────────────┐
│              Compositing Layers              │
├─────────────────────────────────────────────┤
│                                              │
│   Layer 3 (z-index: 3)  ─┐                  │
│   ┌──────────────────┐   │                  │
│   │     Modal        │   │                  │
│   └──────────────────┘   │                  │
│                          │  GPU 합성        │
│   Layer 2 (z-index: 2)  ─┤  ───────────►   │
│   ┌──────────────────┐   │                  │
│   │   Navigation     │   │                  │
│   └──────────────────┘   │                  │
│                          │                  │
│   Layer 1 (z-index: 1)  ─┘                  │
│   ┌──────────────────┐                      │
│   │     Content      │                      │
│   └──────────────────┘                      │
│                                              │
└─────────────────────────────────────────────┘
```

**레이어 생성 조건**:
- `transform: translateZ(0)` 또는 `translate3d()`
- `will-change: transform` 또는 `opacity`
- `position: fixed`
- `<video>`, `<canvas>`, `<iframe>`
- CSS filters, blend modes

---

## 구현 패턴

### 1. Reflow 최소화

```javascript
// 나쁜 예: 강제 동기 레이아웃 (Layout Thrashing)
for (let i = 0; i < elements.length; i++) {
  elements[i].style.width = box.offsetWidth + 'px';  // 읽기 → 쓰기 반복
}

// 좋은 예: 읽기/쓰기 분리
const width = box.offsetWidth;  // 한 번만 읽기
for (let i = 0; i < elements.length; i++) {
  elements[i].style.width = width + 'px';  // 쓰기만
}
```

### 2. CSS 변경 일괄 처리

```javascript
// 나쁜 예: 개별 스타일 변경
element.style.width = '100px';
element.style.height = '200px';
element.style.margin = '10px';

// 좋은 예: 클래스 토글
element.classList.add('new-styles');

// 좋은 예: cssText 사용
element.style.cssText = 'width: 100px; height: 200px; margin: 10px;';
```

### 3. DOM 조작 최적화

```javascript
// 나쁜 예: 반복적 DOM 삽입
for (let i = 0; i < 1000; i++) {
  container.innerHTML += `<div>${i}</div>`;  // 매번 리플로우
}

// 좋은 예: DocumentFragment 사용
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = i;
  fragment.appendChild(div);
}
container.appendChild(fragment);  // 한 번만 리플로우
```

### 4. GPU 가속 활용

```css
/* Layout/Paint를 건너뛰고 Composite만 */
.animate-transform {
  transform: translateX(100px);  /* GPU 가속 */
}

.animate-opacity {
  opacity: 0.5;  /* GPU 가속 */
}

/* will-change로 레이어 힌트 */
.will-animate {
  will-change: transform;  /* 미리 레이어 생성 */
}

/* 사용 후 제거 */
.animation-done {
  will-change: auto;  /* 메모리 해제 */
}
```

### 5. 레이아웃 트리거 속성 회피

```css
/* 나쁜 예: width/height 애니메이션 */
.bad-animation {
  transition: width 0.3s;  /* Layout 발생 */
}

/* 좋은 예: transform 사용 */
.good-animation {
  transition: transform 0.3s;  /* Composite만 */
}

/* 스케일 대신 transform */
.bad { width: 200%; }           /* Layout */
.good { transform: scale(2); }  /* Composite */
```

---

## 렌더링 차단 리소스

### CSS 최적화

```html
<!-- 모든 CSS는 기본적으로 렌더링 차단 -->
<link rel="stylesheet" href="style.css">

<!-- 미디어 쿼리로 조건부 로딩 -->
<link rel="stylesheet" href="print.css" media="print">
<link rel="stylesheet" href="mobile.css" media="(max-width: 768px)">

<!-- 비동기 로딩 (비필수 CSS) -->
<link rel="preload" href="non-critical.css" as="style" onload="this.rel='stylesheet'">
```

### JavaScript 최적화

```html
<!-- 기본: 파싱 차단 -->
<script src="app.js"></script>

<!-- async: 다운로드 병렬, 완료 시 즉시 실행 -->
<script async src="analytics.js"></script>

<!-- defer: 다운로드 병렬, DOM 완성 후 순서대로 실행 -->
<script defer src="app.js"></script>
```

**async vs defer**:

```
HTML 파싱:  ████████████████████████████████████

async:      다운로드 ███   실행 ██
            (파싱 중 완료되면 즉시 실행, 순서 보장 없음)

defer:      다운로드 █████████████
                                  실행 ██
            (파싱 완료 후 순서대로 실행)
```

---

## 성능 측정

### Chrome DevTools 활용

```
Performance 패널:
├── Loading (파란색): HTML 파싱, 리소스 로딩
├── Scripting (노란색): JavaScript 실행
├── Rendering (보라색): Layout, Style 계산
├── Painting (녹색): Paint, Composite
└── System (회색): 기타 브라우저 작업

주요 지표:
- FP (First Paint): 첫 픽셀 렌더링
- FCP (First Contentful Paint): 첫 콘텐츠 렌더링
- LCP (Largest Contentful Paint): 최대 콘텐츠 렌더링
- CLS (Cumulative Layout Shift): 레이아웃 이동 누적
```

### Layout Thrashing 감지

```javascript
// Performance API로 레이아웃 측정
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'layout-shift') {
      console.log('Layout Shift:', entry.value);
    }
  }
});
observer.observe({ entryTypes: ['layout-shift'] });
```

---

## 트레이드오프

### 렌더링 최적화 전략

| 전략 | 장점 | 단점 | 적용 시점 |
|------|------|------|----------|
| **레이어 분리** | GPU 가속, 독립 렌더링 | 메모리 증가 | 애니메이션 요소 |
| **will-change** | 사전 최적화 | 리소스 낭비 가능 | 확실한 애니메이션 |
| **requestAnimationFrame** | 프레임 동기화 | 복잡도 증가 | JS 애니메이션 |
| **가상화** | 대량 요소 최적화 | 구현 복잡도 | 긴 리스트 |

### CSS vs JavaScript 애니메이션

| 특성 | CSS | JavaScript |
|------|-----|------------|
| 성능 | 일반적으로 우수 | 제어 가능 |
| 제어 | 제한적 | 완전한 제어 |
| 복잡도 | 단순 | 복잡 |
| GPU 가속 | 자동 (transform, opacity) | 수동 설정 |
| 사용 | 단순 애니메이션 | 복잡한 시퀀스 |

---

## 실무 적용

### 체크리스트

```yaml
critical_rendering_path:
  - CSS를 <head>에 배치
  - 비필수 CSS는 비동기 로딩
  - JavaScript는 defer 또는 async 사용
  - 폰트는 font-display: swap 적용

layout_optimization:
  - 읽기/쓰기 분리
  - DocumentFragment 사용
  - 클래스 토글로 일괄 변경
  - 고정 크기 지정 (CLS 방지)

paint_optimization:
  - transform, opacity 사용
  - will-change 적절히 사용
  - 불필요한 레이어 생성 방지
  - requestAnimationFrame 활용
```

---

## 면접 포인트

**Q**: Critical Rendering Path란?

**A**: HTML과 CSS를 파싱하여 화면에 픽셀을 그리는 과정이다. DOM 구축 → CSSOM 구축 → Render Tree 생성 → Layout → Paint → Composite 순서로 진행된다. CSS는 렌더링 차단 리소스이므로 CSSOM이 완성되어야 Render Tree를 구축할 수 있다.

**Q**: Reflow와 Repaint의 차이는?

**A**: Reflow(Layout)는 요소의 위치와 크기를 다시 계산하는 과정이고, Repaint는 계산된 레이아웃에 픽셀을 채우는 과정이다. Reflow는 항상 Repaint를 발생시키지만 Repaint는 Reflow 없이 발생할 수 있다. transform, opacity는 Composite만 발생시켜 가장 효율적이다.

**Q**: Layout Thrashing이란?

**A**: JavaScript에서 레이아웃 속성을 읽고 쓰기를 반복하면 브라우저가 매번 강제로 레이아웃을 다시 계산하는 현상이다. offsetWidth를 읽은 후 style을 변경하면 동기적으로 레이아웃이 발생한다. 읽기 작업을 먼저 일괄 수행하고 쓰기를 나중에 하여 방지한다.

**Q**: will-change 사용 시 주의점은?

**A**: will-change는 브라우저에 최적화 힌트를 주어 미리 레이어를 생성한다. 그러나 과도하게 사용하면 메모리를 낭비한다. 애니메이션 시작 전에 적용하고 완료 후 제거해야 한다. 정적 요소에는 사용하지 않는다.

---

## 참고 자료

- [Google - Critical Rendering Path](https://developers.google.com/web/fundamentals/performance/critical-rendering-path)
- [MDN - CSS and JavaScript animation performance](https://developer.mozilla.org/en-US/docs/Web/Performance/CSS_JavaScript_animation_performance)
- [web.dev - Rendering Performance](https://web.dev/rendering-performance/)
- [CSS Triggers](https://csstriggers.com/)
