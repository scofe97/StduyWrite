# React Server Components

## 개요

**정의**: React Server Components(RSC)는 서버에서만 렌더링되어 JavaScript 번들에 포함되지 않으며, 데이터베이스에 직접 접근할 수 있는 새로운 컴포넌트 패턴이다.

**목적**: CSR의 성능 문제(느린 초기 로딩, SEO 불리, 워터폴 요청)를 해결하고, 서버 리소스를 효율적으로 활용하여 최적의 사용자 경험을 제공한다.

---

## 핵심 개념

### CSR의 문제점

```
[Client-Side Rendering 흐름]

브라우저                              서버
   │                                   │
   ├──(1) 페이지 요청───────────────→  │
   │←────────────(2) 빈 HTML 반환────  │
   │                                   │
   ├──(3) JS 번들 요청──────────────→  │
   │←──────────(4) 큰 JS 번들 반환───  │
   │                                   │
   │ (5) JS 파싱 & 실행                │
   │ (6) 컴포넌트 렌더링               │
   │                                   │
   ├──(7) 데이터 요청──────────────→   │
   │←──────────(8) JSON 데이터 반환──  │
   │                                   │
   │ (9) 최종 UI 렌더링                │
   └───────────────────────────────────┘
```

| 문제 | 설명 | 영향 |
|------|------|------|
| **느린 초기 로딩** | JS 번들 다운로드 후에야 렌더링 시작 | 사용자 이탈 증가 |
| **SEO 불리** | 검색 엔진이 빈 HTML만 인덱싱 | 검색 순위 하락 |
| **워터폴 요청** | HTML → JS → 데이터 순차 요청 | 네트워크 병목 |
| **큰 번들 크기** | 모든 컴포넌트가 JS에 포함 | 대역폭 낭비 |

---

### Server Components vs Client Components

| 특성 | Server Component | Client Component |
|------|------------------|------------------|
| **실행 위치** | 서버만 | 서버 + 브라우저 |
| **async/await** | 가능 | 불가 |
| **DB 직접 접근** | 가능 | 불가 |
| **useState/useEffect** | 불가 | 가능 |
| **이벤트 핸들러** | 불가 | 가능 |
| **브라우저 API** | 불가 | 가능 |
| **JS 번들 포함** | 미포함 | 포함 |
| **리렌더링** | 없음 | 가능 |

---

### 컴포넌트 선택 결정 트리

```
컴포넌트 필요
    │
    ├─ 데이터베이스 접근 필요?
    │       └─ Yes → Server Component
    │
    ├─ useState/useEffect 필요?
    │       └─ Yes → Client Component
    │
    ├─ 이벤트 핸들러 (onClick 등) 필요?
    │       └─ Yes → Client Component
    │
    ├─ 브라우저 API (localStorage 등) 필요?
    │       └─ Yes → Client Component
    │
    └─ 그 외
            └─ Server Component (기본값)
```

---

## 구현 패턴

### 1. Server Component 데이터 페칭

```typescript
// app/page.tsx - 기본적으로 Server Component
type Product = {
  id: number;
  title: string;
  description: string;
};

async function getProducts(): Promise<Product[]> {
  // 서버에서 직접 데이터 페칭
  const response = await fetch('https://api.example.com/products');
  return response.json();
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <main>
      <h1>Products</h1>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            <h2>{product.title}</h2>
            <p>{product.description}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

---

### 2. Client Component 정의

```typescript
// components/Counter.tsx
'use client';  // 파일 최상단에 선언

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

---

### 3. Hydration 이해

```
[Hydration 프로세스]

서버                                 브라우저
   │                                    │
   │ (1) Client Component도             │
   │     HTML로 렌더링                  │
   │                                    │
   ├───(2) 정적 HTML 전송────────────→  │
   │                                    │
   │                         (3) HTML 즉시 표시
   │                         (비인터랙티브)
   │                                    │
   ├───(4) JS 번들 전송──────────────→  │
   │                                    │
   │                         (5) Hydration
   │                         (이벤트 핸들러 연결)
   │                                    │
   │                         (6) 인터랙티브!
   └────────────────────────────────────┘
```

**Hydration**: 서버에서 생성된 정적 HTML에 JavaScript 기능(이벤트 핸들러 등)을 연결하는 과정

---

### 4. Client Boundary

```
[컴포넌트 트리와 Client Boundary]

                RootLayout (Server)
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    Header         Page         Footer
   (Server)      (Server)       (Server)
                    │
    ┌───────────────┼───────────────┐
    │               │               │
ProductList  ColorModeToggle    Sidebar
 (Server)       (Client)        (Server)
                    │
            ════════╪════════ Client Boundary
                    │
              자식 컴포넌트
             (자동 Client)
```

**중요**: Client Component의 자식은 자동으로 Client Component가 된다.

---

### 5. Server Component를 Client Component에 전달

**패턴: children으로 Server Component 전달**

```typescript
// components/InteractiveWrapper.tsx (Client)
'use client';

import { ReactNode, useState } from 'react';

export function InteractiveWrapper({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div>
      <button onClick={() => setExpanded(e => !e)}>
        {expanded ? '접기' : '펼치기'}
      </button>
      {expanded && children}
    </div>
  );
}

// app/page.tsx (Server)
import { InteractiveWrapper } from '@/components/InteractiveWrapper';
import { ProductList } from '@/components/ProductList'; // Server Component

export default async function Page() {
  return (
    <InteractiveWrapper>
      {/* Server Component가 children으로 전달됨 */}
      <ProductList />
    </InteractiveWrapper>
  );
}
```

---

### 6. Zod로 타입 안전성 확보

```typescript
// src/data/schema.ts
import { z } from 'zod';

export const postSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
});

export const postsSchema = z.array(postSchema);

// 타입 추론
type Post = z.infer<typeof postSchema>;

// src/data/queries.ts
export async function getAllPosts() {
  const client = createClient({ url: process.env.DB_URL ?? '' });
  const data = await client.execute('SELECT id, title, description FROM posts');
  client.close();

  // parse()로 런타임 타입 검증
  return postsSchema.parse(data.rows);
}
```

---

### 7. React Suspense로 로딩 처리

```typescript
// src/app/posts/page.tsx
import { Suspense } from 'react';
import { Loading } from '@/components/Loading';
import { PostList } from '@/components/PostList';

export default async function Posts({ searchParams }: Props) {
  const criteria = (await searchParams).criteria;

  return (
    <main>
      <h2>Posts</h2>
      <Suspense fallback={<Loading />}>
        <PostList criteria={criteria} />
      </Suspense>
    </main>
  );
}
```

**Suspense 스트리밍**:

```
서버                                    브라우저
   │ (1) Page RSC 실행                       │
   │     └─ <Suspense> 발견                  │
   │                                         │
   ├──(2) 첫 번째 청크 전송──────────────→   │
   │   (헤딩 + Loading 폴백)                 │
   │                                 (3) 즉시 표시
   │                                         │
   │ (4) 자식 컴포넌트 데이터 페칭           │
   │                                         │
   ├──(5) 두 번째 청크 전송──────────────→   │
   │   (실제 데이터)                         │
   │                                 (6) Loading → 데이터
   └─────────────────────────────────────────┘
```

---

### 8. Error Boundary로 에러 처리

```typescript
// src/components/ErrorBoundary.tsx
'use client';

import { ErrorBoundary as ReactErrorBoundary } from 'react-error-boundary';

export function ErrorBoundary({ children }: { children: ReactNode }) {
  return (
    <ReactErrorBoundary
      FallbackComponent={({ error, resetErrorBoundary }) => (
        <div role="alert">
          <h3>Something went wrong</h3>
          <p>{error.message}</p>
          <button onClick={resetErrorBoundary}>Retry</button>
        </div>
      )}
    >
      {children}
    </ReactErrorBoundary>
  );
}

// 페이지에 적용
export default async function Posts() {
  return (
    <Suspense fallback={<Loading />}>
      <ErrorBoundary>
        <PostList />
      </ErrorBoundary>
    </Suspense>
  );
}
```

---

### 9. Server Function (Server Actions)

**정의 및 사용**:

```typescript
// src/data/createPost.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(title: string, description: string) {
  const client = createClient({ url: process.env.DB_URL ?? '' });

  try {
    const result = await client.execute({
      sql: 'INSERT INTO posts(title, description) VALUES (?, ?)',
      args: [title, description],
    });

    // Next.js 캐시 무효화
    revalidatePath('/posts');

    return { ok: true, id: result.lastInsertRowid };
  } catch {
    return { ok: false };
  } finally {
    client.close();
  }
}

// Client Component에서 호출
'use client';

import { createPost } from '@/data/createPost';

export function NewPost() {
  const [status, setStatus] = useState<'pending' | 'error' | 'success'>('pending');

  async function handleClick() {
    const result = await createPost('New Post', 'Description');
    setStatus(result.ok ? 'success' : 'error');
  }

  return (
    <button onClick={handleClick}>Create New Post</button>
  );
}
```

---

## 트레이드오프

### 서버사이드 vs 클라이언트사이드 데이터 페칭

| 특성 | 서버사이드 | 클라이언트사이드 |
|------|------------|------------------|
| **초기 로딩 속도** | 빠름 | 느림 |
| **HTTP 요청 수** | 적음 | 많음 (워터폴) |
| **쿠키 접근** | 가능 | 불가 |
| **데이터 새로고침** | 페이지 리로드 필요 | 자유롭게 가능 |
| **무한 스크롤** | 불가 | 가능 |
| **페이지네이션** | 페이지 리로드 필요 | 자유롭게 가능 |

### Server Function vs API Route

| 특성 | Server Function | API Route |
|------|-----------------|-----------|
| **코드량** | 적음 | 많음 |
| **타입 안전성** | 자동 | 수동 설정 필요 |
| **호출 방식** | 함수 호출 | fetch() |
| **HTTP 메서드** | POST 고정 | 자유롭게 선택 |
| **캐싱** | 브라우저 캐시 안됨 | GET 캐싱 가능 |
| **용도** | 데이터 뮤테이션 | 데이터 페칭 + 뮤테이션 |

---

## 실무 적용

### 'use client' 경계 최적화

```typescript
// 비효율적 - 전체가 Client
'use client';
export function ProductPage() {
  const [filter, setFilter] = useState('');
  return (
    <div>
      <input onChange={e => setFilter(e.target.value)} />
      <ProductList products={products} />  {/* 정적 부분도 Client */}
    </div>
  );
}

// 효율적 - 인터랙티브 부분만 Client
// ProductFilter.tsx (Client)
'use client';
export function ProductFilter({ onFilter }) {
  const [filter, setFilter] = useState('');
  return <input onChange={e => onFilter(e.target.value)} />;
}

// ProductPage.tsx (Server)
export async function ProductPage() {
  const products = await getProducts();
  return (
    <div>
      <ProductFilter />
      <ProductList products={products} />  {/* Server */}
    </div>
  );
}
```

### 패턴 선택 가이드

```yaml
server_component:
  use_when:
    - 초기 로딩 속도가 중요
    - SEO가 중요
    - 데이터베이스 직접 접근 필요
    - 쿠키 기반 인증 필요
  avoid_when:
    - 실시간 데이터 갱신 필요
    - 무한 스크롤/페이지네이션

client_component:
  use_when:
    - 사용자 상호작용 필요
    - 브라우저 API 사용
    - 실시간 업데이트 필요
  minimize:
    - 가능한 작은 단위로 분리
    - children으로 Server Component 전달
```

---

## 면접 포인트

**Q**: React Server Components와 SSR의 차이는?

**A**: RSC는 컴포넌트 단위로 서버/클라이언트를 결정하여 번들 크기를 최적화하고, SSR은 전체 페이지 HTML을 서버에서 생성하여 초기 렌더링을 가속한다. 둘은 대체 관계가 아니라 함께 사용하면 최적의 결과를 얻는다. RSC는 "어떤 컴포넌트를 서버에서 실행할지", SSR은 "HTML을 어디서 생성할지"에 관한 것이다.

**Q**: Hydration이란 무엇인가?

**A**: Hydration은 서버에서 렌더링된 정적 HTML에 JavaScript 이벤트 핸들러를 연결하여 상호작용 가능하게 만드는 과정이다. Client Component는 서버에서 HTML로 먼저 렌더링되고, 클라이언트에서 JS가 로드된 후 Hydration되어 인터랙티브해진다.

**Q**: Server Component에서 useState를 사용할 수 없는 이유는?

**A**: Server Component는 서버에서 한 번만 실행되고 클라이언트에 JS가 전송되지 않는다. useState는 클라이언트에서 상태를 관리하고 리렌더링을 트리거하는데, Server Component는 리렌더링 개념이 없으므로 useState가 의미가 없다. 상호작용이 필요하면 Client Component를 사용해야 한다.

---

## 참고 자료

- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [React Server Components RFC](https://github.com/reactjs/rfcs/pull/188)
- [React Suspense](https://react.dev/reference/react/Suspense)
- [Zod Documentation](https://zod.dev/)
