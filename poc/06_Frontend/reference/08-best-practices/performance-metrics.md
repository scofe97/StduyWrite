# 성능 지표 (Core Web Vitals)

## 개요

**정의**: Core Web Vitals는 Google이 정의한 웹 성능 핵심 지표로, 사용자 경험의 로딩, 상호작용, 시각적 안정성을 측정한다.

**목적**: 사용자 경험 객관적 측정, SEO 순위 영향, 성능 병목 식별, 개선 효과 정량화를 달성한다.

---

## Core Web Vitals 3대 지표

```
┌─────────────────────────────────────────────────────────────────┐
│                    Core Web Vitals                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LCP (Largest Contentful Paint)                                │
│   ├─ 측정: 가장 큰 콘텐츠 요소 렌더링 시간                        │
│   ├─ 목표: ≤ 2.5초                                              │
│   └─ 개선: 이미지 최적화, 서버 응답 시간, CSS 차단 제거           │
│                                                                  │
│   INP (Interaction to Next Paint)                               │
│   ├─ 측정: 상호작용 후 다음 페인트까지 시간                       │
│   ├─ 목표: ≤ 200ms                                              │
│   └─ 개선: JavaScript 최적화, 긴 작업 분할, 메인 스레드 해제      │
│                                                                  │
│   CLS (Cumulative Layout Shift)                                 │
│   ├─ 측정: 예기치 않은 레이아웃 이동 누적 점수                    │
│   ├─ 목표: ≤ 0.1                                                │
│   └─ 개선: 이미지/광고 크기 지정, 폰트 로딩 최적화               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 지표 기준

| 지표 | Good | Needs Improvement | Poor |
|------|------|-------------------|------|
| **LCP** | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

---

## LCP (Largest Contentful Paint)

### 측정 대상
- `<img>` 요소
- `<video>` 포스터 이미지
- CSS background-image
- 텍스트 블록 (`<p>`, `<h1>` 등)

### 최적화 방법

```html
<!-- 1. 이미지 최적화 -->
<img
  src="hero.webp"
  srcset="hero-480.webp 480w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
  loading="eager"
  fetchpriority="high"
  alt="Hero image"
/>

<!-- 2. 중요 리소스 프리로드 -->
<link rel="preload" href="hero.webp" as="image" />
<link rel="preload" href="critical.css" as="style" />

<!-- 3. 서버 힌트 -->
<link rel="preconnect" href="https://cdn.example.com" />
<link rel="dns-prefetch" href="https://api.example.com" />
```

```javascript
// 서버 응답 시간 개선
// - CDN 사용
// - 캐싱 헤더 설정
// - 서버 사이드 렌더링 또는 정적 생성

// Next.js 예시
export const revalidate = 3600;  // ISR: 1시간 캐시
```

---

## INP (Interaction to Next Paint)

### 측정 대상
- 클릭, 탭, 키보드 입력
- 상호작용 후 시각적 피드백까지의 시간

### 최적화 방법

```javascript
// 1. 긴 작업 분할
// 나쁜 예: 메인 스레드 블로킹
function processLargeArray(items) {
  items.forEach(item => heavyComputation(item));
}

// 좋은 예: 청크로 분할
async function processLargeArray(items) {
  const CHUNK_SIZE = 100;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => heavyComputation(item));

    // 브라우저에 제어권 반환
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// 2. Web Worker 사용
const worker = new Worker('heavy-task.js');
worker.postMessage(data);
worker.onmessage = (e) => updateUI(e.data);

// 3. React: useTransition으로 우선순위 낮추기
function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  function handleChange(e) {
    setQuery(e.target.value);  // 높은 우선순위
    startTransition(() => {
      setResults(filterResults(e.target.value));  // 낮은 우선순위
    });
  }
}
```

---

## CLS (Cumulative Layout Shift)

### 발생 원인
- 크기 미지정 이미지/동영상
- 동적 삽입 콘텐츠
- 웹 폰트 로딩 (FOIT/FOUT)
- 비동기 광고/임베드

### 최적화 방법

```html
<!-- 1. 이미지 크기 지정 -->
<img src="photo.jpg" width="800" height="600" alt="Photo" />

<!-- 또는 aspect-ratio 사용 -->
<style>
  .image-container {
    aspect-ratio: 16 / 9;
    width: 100%;
  }
</style>

<!-- 2. 동적 콘텐츠 공간 예약 -->
<div class="ad-slot" style="min-height: 250px;">
  <!-- 광고 로드 -->
</div>

<!-- 3. 폰트 최적화 -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin />

<style>
  @font-face {
    font-family: 'CustomFont';
    src: url('font.woff2') format('woff2');
    font-display: swap;  /* 또는 optional */
  }
</style>
```

```javascript
// Next.js Image 컴포넌트
import Image from 'next/image';

function Hero() {
  return (
    <Image
      src="/hero.jpg"
      width={1200}
      height={600}
      priority
      alt="Hero"
    />
  );
}
```

---

## 측정 도구

### 필드 데이터 (실제 사용자)
- **Chrome UX Report (CrUX)**: 실제 Chrome 사용자 데이터
- **PageSpeed Insights**: CrUX + Lighthouse 결합
- **Search Console**: Core Web Vitals 리포트

### 랩 데이터 (테스트 환경)
- **Lighthouse**: Chrome DevTools 내장
- **WebPageTest**: 상세 워터폴 분석
- **Chrome DevTools Performance**: 런타임 분석

### JavaScript API

```javascript
// web-vitals 라이브러리
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(metric => {
  console.log('LCP:', metric.value);
  // 분석 서비스로 전송
  sendToAnalytics({ name: 'LCP', value: metric.value });
});

onINP(metric => {
  console.log('INP:', metric.value);
});

onCLS(metric => {
  console.log('CLS:', metric.value);
});

// Next.js 내장 지원
// pages/_app.js
export function reportWebVitals(metric) {
  console.log(metric);
}
```

---

## 최적화 체크리스트

```yaml
LCP_optimization:
  - 히어로 이미지 프리로드
  - 중요 CSS 인라인화
  - 서버 응답 시간 < 200ms
  - CDN 사용
  - 이미지 포맷 최적화 (WebP, AVIF)

INP_optimization:
  - 긴 JavaScript 작업 분할
  - 불필요한 JavaScript 지연 로딩
  - 이벤트 핸들러 최적화
  - Web Worker 활용
  - React: useDeferredValue, useTransition

CLS_optimization:
  - 모든 이미지에 width/height 또는 aspect-ratio
  - 폰트 font-display: swap
  - 동적 콘텐츠 공간 예약
  - 광고/임베드 크기 고정
  - transform 애니메이션 사용 (top/left 대신)
```

---

## 면접 포인트

**Q**: Core Web Vitals 3가지는?

**A**: LCP(Largest Contentful Paint)는 가장 큰 콘텐츠의 렌더링 시간으로 로딩 성능을 측정한다. INP(Interaction to Next Paint)는 상호작용 응답성을 측정한다. CLS(Cumulative Layout Shift)는 시각적 안정성을 측정한다. 각각 2.5초, 200ms, 0.1 이하가 좋은 점수이다.

**Q**: CLS가 발생하는 주요 원인은?

**A**: 크기가 지정되지 않은 이미지/동영상, 동적으로 삽입되는 콘텐츠, 웹 폰트 로딩으로 인한 텍스트 크기 변화, 비동기로 로드되는 광고가 주요 원인이다. 이미지에 width/height를 지정하고, 동적 콘텐츠 영역에 공간을 예약하여 방지한다.

**Q**: INP를 개선하는 방법은?

**A**: 긴 JavaScript 작업을 작은 청크로 분할하고, setTimeout이나 requestIdleCallback으로 메인 스레드에 제어권을 반환한다. 무거운 계산은 Web Worker로 오프로드하고, React에서는 useTransition으로 우선순위가 낮은 업데이트를 지연시킨다.

---

## 참고 자료

- [web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Chrome Developers - INP](https://developer.chrome.com/docs/lighthouse/performance/interaction-to-next-paint/)
- [web-vitals library](https://github.com/GoogleChrome/web-vitals)
- [PageSpeed Insights](https://pagespeed.web.dev/)
