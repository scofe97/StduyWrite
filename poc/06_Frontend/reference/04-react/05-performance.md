# React 성능 최적화 및 렌더링 패턴

## 개요

**정의**: 렌더링 패턴은 웹 콘텐츠를 어디서, 언제, 어떻게 렌더링할지 결정하는 아키텍처 전략이다.

**목적**: 초기 로딩 시간을 줄이고, 번들 크기를 최적화하며, Core Web Vitals를 개선하여 최적의 사용자 경험을 제공한다.

---

## 핵심 개념

### Core Web Vitals

| 지표 | 설명 | 최적화 대상 |
|------|------|------------|
| **TTFB** | Time to First Byte | 서버 응답 시간 |
| **FCP** | First Contentful Paint | 첫 콘텐츠 렌더링 |
| **LCP** | Largest Contentful Paint | 주요 콘텐츠 로딩 |
| **TTI** | Time to Interactive | 상호작용 가능 시점 |
| **CLS** | Cumulative Layout Shift | 레이아웃 안정성 |
| **FID** | First Input Delay | 첫 입력 반응 시간 |

### 렌더링 패턴 비교

| 패턴 | TTFB | FCP | TTI | JS 크기 | SEO | 서버 비용 |
|------|------|-----|-----|--------|-----|----------|
| CSR | 빠름 | 느림 | 느림 | 큼 | 나쁨 | 낮음 |
| SSR | 보통 | 보통 | 보통 | 큼 | 좋음 | 높음 |
| Static | 빠름 | 빠름 | 빠름 | 중간 | 좋음 | 낮음 |
| ISR | 빠름 | 빠름 | 빠름 | 중간 | 좋음 | 낮음 |
| Streaming | 빠름 | 빠름 | 보통 | 중간 | 좋음 | 중간 |
| Islands | 빠름 | 빠름 | 빠름 | 작음 | 좋음 | 낮음 |
| RSC | 빠름 | 빠름 | 빠름 | 작음 | 좋음 | 중간 |

---

## 기본 렌더링 패턴

### 1. Client-Side Rendering (CSR)

클라이언트에서 JavaScript로 전체 렌더링을 수행한다.

```javascript
function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <Loading />;

  return (
    <div>
      {data.map(product => (
        <ProductCard key={product.id} {...product} />
      ))}
    </div>
  );
}
```

**적합한 사용 사례**:
- 대시보드, 어드민 패널
- 내부 도구
- 실시간 앱
- SEO가 중요하지 않은 애플리케이션

---

### 2. Server-Side Rendering (SSR)

모든 요청에 대해 서버에서 HTML을 생성한다.

```javascript
// pages/dashboard.js (Next.js)
export async function getServerSideProps(context) {
  const user = await getUserFromCookie(context.req.cookies);
  const dashboardData = await fetchUserDashboard(user.id);

  return {
    props: { user, dashboardData }
  };
}

export default function Dashboard({ user, dashboardData }) {
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <DashboardContent data={dashboardData} />
    </div>
  );
}
```

**적합한 사용 사례**:
- 개인화된 대시보드
- 인증 기반 페이지
- 실시간 데이터
- SEO 중요한 동적 콘텐츠

---

### 3. Static Rendering

빌드 시점에 HTML을 생성하고 CDN에 캐싱한다.

```javascript
// pages/blog.js
export async function getStaticProps() {
  const posts = await fetchBlogPosts();
  return { props: { posts } };
}

export default function Blog({ posts }) {
  return (
    <div>
      {posts.map(post => <PostCard key={post.id} {...post} />)}
    </div>
  );
}
```

**동적 경로 생성 (getStaticPaths)**:

```javascript
// pages/posts/[id].js
export async function getStaticPaths() {
  const posts = await fetchAllPosts();

  return {
    paths: posts.map(post => ({
      params: { id: post.id.toString() }
    })),
    fallback: false  // 없는 경로는 404
  };
}
```

---

### 4. Incremental Static Regeneration (ISR)

빌드 후에도 정적 페이지를 갱신할 수 있는 하이브리드 접근이다.

```javascript
// pages/products/[id].js
export async function getStaticProps({ params }) {
  const product = await fetchProduct(params.id);

  return {
    props: { product },
    revalidate: 60  // 60초마다 재검증
  };
}

export async function getStaticPaths() {
  const popularProducts = await fetchPopularProducts();

  return {
    paths: popularProducts.map(p => ({
      params: { id: p.id.toString() }
    })),
    fallback: 'blocking'  // 나머지는 요청 시 생성
  };
}
```

**On-Demand ISR**:

```javascript
// pages/api/revalidate.js
export default async function handler(req, res) {
  if (req.query.secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  await res.revalidate('/products/' + req.query.id);
  return res.json({ revalidated: true });
}
```

---

## 고급 렌더링 패턴

### 5. Streaming SSR

HTML을 청크 단위로 점진적으로 전송한다.

```javascript
// React 18 - renderToPipeableStream
import { renderToPipeableStream } from 'react-dom/server';

app.get('/', (req, res) => {
  const { pipe, abort } = renderToPipeableStream(
    <App />,
    {
      bootstrapScripts: ['/main.js'],
      onShellReady() {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'text/html');
        pipe(res);
      },
      onShellError(error) {
        res.statusCode = 500;
        res.send('<h1>Something went wrong</h1>');
      }
    }
  );

  setTimeout(abort, 10000);
});
```

**Suspense와 조합**:

```javascript
function App() {
  return (
    <html>
      <body>
        <Header />  {/* 즉시 스트리밍 */}

        <Suspense fallback={<Spinner />}>
          <MainContent />  {/* 준비되면 스트리밍 */}
        </Suspense>

        <Suspense fallback={<CommentsSkeleton />}>
          <Comments />  {/* 나중에 스트리밍 */}
        </Suspense>

        <Footer />
      </body>
    </html>
  );
}
```

---

### 6. Edge SSR

CDN의 엣지 노드에서 서버 렌더링을 수행한다.

```javascript
// pages/listings.js (Next.js Edge)
export const config = {
  runtime: 'edge',
};

export default function Listings({ listings, region }) {
  return (
    <div>
      <Header region={region} />
      <ListingGrid items={listings} />
    </div>
  );
}

export async function getServerSideProps({ req }) {
  const region = req.geo?.region || 'global';
  const listings = await fetchListingsByRegion(region);

  return { props: { listings, region } };
}
```

**장단점**:

| 장점 | 단점 |
|------|------|
| 글로벌 저지연 | 런타임 제한 (V8 기반) |
| 콜드 스타트 거의 없음 | Node.js API 일부 미지원 |
| 자동 스케일링 | 복잡한 로직에 부적합 |
| 비용 효율적 | DB 연결 제한 |

---

### 7. Islands Architecture

정적 HTML 위에 독립적인 상호작용 "섬(Island)"을 배치한다.

```
┌─────────────────────────────────────────────┐
│  Header (정적 HTML - JS 없음)               │
├─────────────────────────────────────────────┤
│  Navigation (Island)  │  Hero Image (정적)  │
│    dropdown.js        │                     │
├─────────────────────────────────────────────┤
│  Main Content (정적 HTML)                   │
├─────────────────────────────────────────────┤
│  Newsletter Form     │  Related Products    │
│    (Island)          │      (Island)        │
│  newsletter.js       │    carousel.js       │
├─────────────────────────────────────────────┤
│  Footer (정적 HTML - JS 없음)               │
└─────────────────────────────────────────────┘
```

**Astro 구현 예시**:

```astro
---
import Header from '../components/Header.astro';
import SearchBar from '../components/SearchBar.jsx';
import Newsletter from '../components/Newsletter.jsx';
---

<html>
  <body>
    <!-- 정적 컴포넌트 -->
    <Header />

    <!-- Island - 즉시 로드 -->
    <SearchBar client:load />

    <!-- Island - 뷰포트 진입 시 로드 -->
    <Newsletter client:visible />
  </body>
</html>
```

**Astro 클라이언트 지시어**:

| 지시어 | Hydration 시점 |
|--------|---------------|
| `client:load` | 즉시 |
| `client:idle` | 브라우저 유휴 시 |
| `client:visible` | 뷰포트 진입 시 |
| `client:media="(min-width: 768px)"` | 미디어 쿼리 매칭 시 |

---

### 8. Progressive Hydration

컴포넌트를 우선순위에 따라 점진적으로 Hydration한다.

```javascript
function LazyHydrate({ children, whenVisible }) {
  const [hydrated, setHydrated] = useState(false);
  const ref = useRef();

  useEffect(() => {
    if (!whenVisible) {
      setHydrated(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setHydrated(true);
          observer.disconnect();
        }
      },
      { rootMargin: '200px' }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [whenVisible]);

  return (
    <div ref={ref}>
      {hydrated ? children : null}
    </div>
  );
}

// 사용
<LazyHydrate whenVisible>
  <HeavyComponent />
</LazyHydrate>
```

---

## 성능 최적화 기법

### 1. Dynamic Import

런타임에 필요한 시점에 모듈을 로딩한다.

```javascript
import React, { Suspense, lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));
const Chart = lazy(() => import('./Chart'));

function App() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <HeavyComponent />
      </Suspense>

      {showChart && (
        <Suspense fallback={<Spinner />}>
          <Chart data={chartData} />
        </Suspense>
      )}

      <button onClick={() => setShowChart(true)}>
        Show Chart
      </button>
    </div>
  );
}
```

---

### 2. Code-Splitting

번들을 여러 개의 작은 청크로 나눈다.

**Route-based Splitting**:

```javascript
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

**Webpack Magic Comments**:

```javascript
// 청크 이름 지정
const Dashboard = lazy(() =>
  import(/* webpackChunkName: "dashboard" */ './Dashboard')
);

// Prefetch (브라우저 유휴 시 로딩)
const Settings = lazy(() =>
  import(/* webpackPrefetch: true */ './Settings')
);

// Preload (즉시 병렬 로딩)
const Profile = lazy(() =>
  import(/* webpackPreload: true */ './Profile')
);
```

---

### 3. PRPL 패턴

Google이 제안한 웹 로딩 최적화 전략이다.

| 단계 | 설명 | 구현 방법 |
|------|------|----------|
| **Push** | 중요한 리소스 푸시 | HTTP/2 Server Push, `<link rel="preload">` |
| **Render** | 초기 라우트 빠르게 렌더링 | SSR, Critical CSS |
| **Pre-cache** | 나머지 리소스 미리 캐싱 | Service Worker |
| **Lazy-load** | 필요할 때 나머지 로딩 | Dynamic Import |

```html
<head>
  <!-- Critical CSS 인라인 -->
  <style>/* critical styles */</style>

  <!-- 중요 리소스 Preload -->
  <link rel="preload" href="/main.js" as="script">
  <link rel="preload" href="/api/initial-data" as="fetch">

  <!-- 다른 라우트 Prefetch -->
  <link rel="prefetch" href="/dashboard.js">
</head>
```

---

### 4. List Virtualization

보이는 항목만 DOM에 렌더링한다.

```javascript
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={400}
      width="100%"
      itemCount={items.length}
      itemSize={50}
    >
      {Row}
    </FixedSizeList>
  );
}
```

**라이브러리 비교**:

| 라이브러리 | 특징 | 사용 사례 |
|-----------|------|----------|
| react-window | 경량, 심플 | 단순 리스트/그리드 |
| react-virtualized | 풍부한 기능 | 복잡한 테이블 |
| @tanstack/virtual | 프레임워크 무관 | 다양한 프레임워크 |

---

## 패턴 선택 가이드

```
페이지 유형?
    │
    ├─ 개인화된 콘텐츠?
    │       └─ Yes → SSR
    │
    └─ 데이터 갱신 빈도?
            ├─ 거의 없음 → Static
            ├─ 간헐적 → ISR
            └─ 실시간 → SEO 중요?
                    ├─ Yes → SSR
                    └─ No → CSR
```

### 페이지별 추천 패턴

| 페이지 유형 | 추천 패턴 | 이유 |
|------------|----------|------|
| 랜딩 페이지 | Static + Edge | 빠른 초기 로딩 |
| 블로그 | ISR + Streaming | 동적 데이터 + 빠른 FCP |
| 대시보드 | SSR + Progressive Hydration | 개인화 + 최적화된 TTI |
| 제품 상세 | ISR | 로딩 성능 + 동적 데이터 |
| 실시간 앱 | CSR | 완전한 상호작용 |

### 하이브리드 접근

```
/              → Static (랜딩 페이지)
/about         → Static (소개 페이지)
/blog          → ISR (블로그 목록)
/blog/[slug]   → ISR (블로그 상세)
/products      → ISR (제품 목록)
/dashboard     → SSR (개인화 대시보드)
/app           → CSR (SPA 기능)
```

---

## 트레이드오프

### DO (권장)

- 라우트 기반 Code-Splitting 기본 적용
- 무거운 라이브러리(Chart, Editor 등) 동적 임포트
- 대용량 리스트는 항상 가상화 적용
- 사용자 행동 예측하여 Prefetch 적용

### DON'T (주의)

- 너무 작은 단위로 분할하면 오히려 성능 저하
- 초기 렌더링에 필요한 컴포넌트는 lazy 사용 주의
- 모든 리스트에 가상화 적용 불필요 (100개 이하는 일반 렌더링)
- Preload 남용 시 네트워크 경쟁 발생

### 최적화 순서

1. **측정**: Lighthouse, Bundle Analyzer로 현황 파악
2. **분석**: 병목 지점 식별 (큰 번들, 느린 컴포넌트)
3. **적용**: 가장 효과 큰 것부터 순차 적용
4. **검증**: 적용 후 다시 측정하여 효과 확인

---

## 면접 포인트

**Q**: CSR, SSR, Static Rendering의 차이점은?

**A**: CSR은 클라이언트에서 JavaScript로 렌더링하여 빈 HTML을 받고 JS가 콘텐츠를 생성한다. SSR은 서버에서 매 요청마다 HTML을 생성하여 완성된 페이지를 전송한다. Static Rendering은 빌드 시점에 HTML을 생성하여 CDN에 캐싱한다. CSR은 SEO에 불리하고 초기 로딩이 느리지만 상호작용이 많은 앱에 적합하고, SSR은 개인화 콘텐츠에, Static은 변경이 적은 콘텐츠에 적합하다.

**Q**: ISR이란 무엇이며 언제 사용하는가?

**A**: ISR(Incremental Static Regeneration)은 빌드 후에도 정적 페이지를 재생성할 수 있는 패턴이다. revalidate 옵션으로 갱신 주기를 설정하거나 On-Demand로 트리거할 수 있다. 제품 카탈로그처럼 간헐적으로 업데이트되지만 실시간은 아닌 데이터에 적합하다. Static의 빠른 로딩과 SSR의 데이터 신선도를 결합한다.

**Q**: Code-Splitting의 이점과 구현 방법은?

**A**: Code-Splitting은 번들을 작은 청크로 나누어 필요할 때만 로딩하여 초기 번들 크기를 줄인다. React에서는 lazy()와 Suspense로 구현하며, 주로 라우트 기반 또는 컴포넌트 기반으로 분할한다. Webpack Magic Comments로 prefetch/preload를 제어할 수 있다.

---

## 참고 자료

- [Next.js 렌더링 문서](https://nextjs.org/docs/rendering)
- [Core Web Vitals](https://web.dev/vitals/)
- [Vercel ISR](https://vercel.com/docs/incremental-static-regeneration)
- [react-window](https://react-window.vercel.app/)
- [Astro](https://docs.astro.build/)
