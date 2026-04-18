# Chapter 6. Next.js로 멀티 페이지 앱 만들기 (Creating a Multi-Page App with Next.js)

---

### 📌 핵심 요약
> Next.js 앱 라우터는 **폴더 구조**와 **page.tsx** 파일로 라우트를 정의한다. **Link 컴포넌트**는 RSC에서도 사용 가능한 클라이언트 사이드 네비게이션을 제공하고, **layout.tsx**는 공유 레이아웃을 구현한다. **동적 라우트**는 `[param]` 폴더명으로 정의하며, **검색 파라미터**는 URL의 `?` 이후 값을 처리한다. 이 모든 기능을 조합해 블로그 앱처럼 여러 화면을 가진 앱을 구현할 수 있다.

---

### 🎯 학습 목표
- Next.js 앱 라우터에서 폴더 구조로 라우트를 생성할 수 있다
- Link 컴포넌트와 useRouter 훅으로 네비게이션을 구현할 수 있다
- layout.tsx로 공유 레이아웃을 만들 수 있다
- 동적 라우트와 라우트 파라미터를 활용할 수 있다
- 검색 파라미터로 필터링 기능을 구현할 수 있다

---

### 📖 본문 정리

#### 1. 라우트 생성하기 (Creating Routes)

##### Next.js 앱 라우터 구조

```
[폴더 구조 = URL 경로]

src/app/
├── page.tsx           → /
├── layout.tsx         → 모든 페이지 공유 레이아웃
├── globals.css
│
├── posts/
│   └── page.tsx       → /posts
│
└── settings/
    └── page.tsx       → /settings
```

##### 라우트 정의 규칙

| 파일/폴더 | 역할 | 예시 |
|-----------|------|------|
| `page.tsx` | 라우트의 UI 정의 | 해당 경로에서 렌더링될 컴포넌트 |
| 폴더명 | URL 세그먼트 | `posts/` → `/posts` |
| `layout.tsx` | 공유 레이아웃 | 헤더, 푸터 등 |

##### 라우트 컴포넌트 작성

```typescript
// src/app/posts/page.tsx
import { posts } from '@/data/posts';

export default function Posts() {
  return (
    <main>
      <h2>Posts</h2>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <span>{post.title}</span>
            <p>{post.description}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

**중요**: 컴포넌트는 반드시 **default export**여야 함. Next.js가 자동으로 감지하려면 필수!

---

#### 2. 네비게이션 구현하기 (Creating Navigation)

##### Link 컴포넌트

```typescript
import Link from 'next/link';

// RSC에서도 사용 가능!
export default function Posts() {
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <Link href={`/posts/${post.id}`}>
            {post.title}
          </Link>
        </li>
      ))}
    </ul>
  );
}
```

##### Link vs useRouter 비교

```
[네비게이션 방식 비교]

Link 컴포넌트                    useRouter 훅
─────────────────────────────────────────────────
✅ RSC에서 사용 가능             ❌ Client Component만
✅ 선언적 방식                   ✅ 프로그래밍 방식
✅ HTML <a> 태그로 렌더링        ✅ 조건부 네비게이션
✅ 권장 방식                     ✅ 복잡한 로직 필요시
```

##### useRouter 사용 예시

```typescript
'use client';  // Client Component 필수!

import { useRouter } from 'next/navigation';

function SomeComponent() {
  const router = useRouter();

  function handleClick() {
    if (someCheck()) {
      router.push('/some-path');      // 히스토리 추가
    } else {
      router.replace('/other-path');  // 히스토리 교체
    }
  }

  return <button onClick={handleClick}>Action</button>;
}
```

##### useRouter 주요 메서드

| 메서드 | 설명 | 사용 예시 |
|--------|------|-----------|
| `push(path)` | 네비게이션 + 히스토리 추가 | 일반적인 페이지 이동 |
| `replace(path)` | 네비게이션, 히스토리 교체 | 로그인 후 리다이렉트 |
| `refresh()` | 현재 라우트 새로고침 | 상태 유지하며 데이터 갱신 |
| `back()` | 뒤로 가기 | 이전 페이지로 |

---

#### 3. 공유 레이아웃 만들기 (Creating Shared Layout)

##### layout.tsx 구조

```
[레이아웃 컴포넌트 동작]

                    ┌─────────────────────┐
                    │   RootLayout        │
                    │   (layout.tsx)      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      <Header />     │
                    ├─────────────────────┤
                    │     {children}      │ ← 페이지 컴포넌트
                    ├─────────────────────┤
                    │      <Footer />     │
                    └─────────────────────┘
```

##### layout.tsx 구현

```typescript
// src/app/layout.tsx
import { Header } from '@/components/Header';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <Header />
        {children}  {/* 각 라우트의 page.tsx */}
      </body>
    </html>
  );
}
```

##### 활성 링크 스타일링 (usePathname)

```typescript
// src/components/Header.tsx
'use client';  // usePathname은 Client Component에서만!

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Header() {
  const pathname = usePathname();

  return (
    <header>
      <Link
        href="/"
        className={pathname === '/' ? 'active' : ''}
      >
        Home
      </Link>
      <Link
        href="/posts"
        className={pathname === '/posts' ? 'active' : ''}
      >
        Posts
      </Link>
    </header>
  );
}
```

---

#### 4. 동적 라우트 만들기 (Creating Dynamic Routes)

##### 동적 라우트 구조

```
[동적 라우트 폴더 구조]

src/app/posts/
├── page.tsx           → /posts (목록)
└── [id]/              → 대괄호 = 동적 세그먼트
    └── page.tsx       → /posts/1, /posts/2, ...
```

##### params prop으로 파라미터 접근

```typescript
// src/app/posts/[id]/page.tsx
import { notFound } from 'next/navigation';
import { posts } from '@/data/posts';

export default async function Post({
  params,
}: {
  params: Promise<{ id: string }>;  // 비동기!
}) {
  const id = Number((await params).id);

  // 유효성 검사
  if (!Number.isInteger(id)) {
    notFound();  // 404 페이지 표시
  }

  const post = posts.find((post) => post.id === id);

  if (!post) {
    notFound();
  }

  return (
    <main>
      <h2>{post.title}</h2>
      <p>{post.description}</p>
    </main>
  );
}
```

##### useParams 훅 (Client Component)

```typescript
'use client';

import { useParams } from 'next/navigation';

export function PostTitle() {
  const params = useParams<{ id: string }>();

  return <h3>Blog post {params.id}</h3>;
}
```

##### 파라미터 접근 방법 비교

| 방식 | 사용 위치 | 비동기 | 예시 |
|------|-----------|--------|------|
| `params` prop | RSC/Client | ✅ Promise | `(await params).id` |
| `useParams()` | Client Only | ❌ 동기 | `params.id` |

---

#### 5. 검색 파라미터 사용하기 (Using Search Parameters)

##### 검색 파라미터란?

```
URL: /posts?criteria=react&sort=newest
           ├────────────────────────┘
           └─ 검색 파라미터 (Query Parameters)

criteria = "react"
sort = "newest"
```

##### searchParams prop 사용

```typescript
// src/app/posts/page.tsx
export default async function Posts({
  searchParams,
}: {
  searchParams: Promise<{
    [key: string]: string | string[] | undefined;
  }>;
}) {
  const criteria = (await searchParams).criteria;

  const filteredPosts =
    typeof criteria === 'string'
      ? posts.filter((post) =>
          post.title.toLowerCase().includes(criteria.toLowerCase())
        )
      : posts;

  return (
    <main>
      <h2>{criteria ? `Posts for ${criteria}` : 'Posts'}</h2>
      <ul>
        {filteredPosts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </main>
  );
}
```

##### Next.js Form 컴포넌트

```typescript
// src/components/Header.tsx
import Form from 'next/form';

export function Header() {
  return (
    <header>
      {/* ... 링크들 ... */}
      <Form action="/posts">
        <input
          type="search"
          name="criteria"
          placeholder="Search"
          aria-label="Search blog posts"
        />
      </Form>
    </header>
  );
}
```

**Form 특징**: 전체 페이지 리로드 없이 네비게이션 + 검색 파라미터 전달

##### useSearchParams 훅 (Client Component)

```typescript
'use client';

import { useSearchParams } from 'next/navigation';

export function SearchResults() {
  const searchParams = useSearchParams();
  const criteria = searchParams.get('criteria');  // URLSearchParams API

  return <p>Searching: {criteria}</p>;
}
```

##### 파라미터 타입 비교

| 파라미터 유형 | URL 예시 | 접근 방법 |
|---------------|----------|-----------|
| **라우트 파라미터** | `/posts/123` | `params.id` |
| **검색 파라미터** | `/posts?id=123` | `searchParams.id` |

---

### 🔍 심화 학습

#### 전체 앱 구조 다이어그램

```
[블로그 앱 라우팅 구조]

src/app/
│
├── layout.tsx ─────────────────────────────────────┐
│   │                                               │
│   └── <Header /> ← usePathname (활성 링크)        │
│       ├── Home 링크 → /                           │
│       ├── Posts 링크 → /posts                     │
│       └── <Form> → /posts?criteria=xxx            │
│                                                   │
├── page.tsx ──────────── / (Home)                  │
│                                                   │
└── posts/                                          │
    ├── page.tsx ──────── /posts                    │
    │   └── searchParams.criteria로 필터링          │
    │                                               │
    └── [id]/                                       │
        └── page.tsx ── /posts/1, /posts/2, ...     │
            └── params.id로 게시물 조회             │
                                                    │
                {children} ◄────────────────────────┘
```

#### 라우트 vs 레이아웃 vs 페이지

```
[파일 역할 정리]

파일명          역할                      예시
────────────────────────────────────────────────────
page.tsx       라우트의 고유 UI           게시물 목록, 상세 페이지
layout.tsx     공유 UI 래퍼               헤더, 사이드바, 푸터
loading.tsx    로딩 UI (Suspense)         스켈레톤 UI
error.tsx      에러 UI                    에러 메시지
not-found.tsx  404 UI                     "페이지를 찾을 수 없습니다"
```

#### 네비게이션 선택 가이드

```
네비게이션 필요

├─ 단순 링크?
│   └─ Yes → Link 컴포넌트 사용
│
├─ 조건부 네비게이션?
│   └─ Yes → useRouter 사용
│
├─ 폼 제출 후 이동?
│   └─ Yes → Form 컴포넌트 (검색 파라미터 자동 추가)
│
└─ RSC에서 사용?
    ├─ Yes → Link 컴포넌트만 가능
    └─ No → Link 또는 useRouter
```

---

### 💡 실무 적용 포인트

1. **폴더 = URL**: Next.js 앱 라우터에서 폴더 구조가 곧 URL 경로. 직관적인 폴더명 사용

2. **Link 우선**: 대부분의 네비게이션은 Link 컴포넌트로 충분. useRouter는 복잡한 조건부 로직에만

3. **동적 라우트 유효성 검사**: `params`로 받은 값은 항상 문자열. 숫자 변환 및 `notFound()` 처리 필수

4. **검색 파라미터 타입 가드**: `searchParams`의 값은 `string | string[] | undefined`. typeof 체크 필요

5. **레이아웃 중첩**: 특정 라우트에만 적용되는 레이아웃은 해당 폴더에 `layout.tsx` 추가

6. **Form 컴포넌트 활용**: 검색 기능 구현 시 `next/form`의 Form 사용. 페이지 리로드 없이 검색 파라미터 전달

---

### ✅ 정리 체크리스트

- [ ] 폴더 구조와 `page.tsx`로 라우트를 정의하는 방법을 안다
- [ ] 라우트 컴포넌트가 반드시 default export여야 하는 이유를 안다
- [ ] Link 컴포넌트가 RSC에서도 사용 가능함을 안다
- [ ] useRouter 훅의 push, replace, refresh 메서드 차이를 안다
- [ ] layout.tsx에서 children prop으로 페이지를 렌더링하는 구조를 이해한다
- [ ] usePathname으로 현재 경로를 가져와 활성 링크를 스타일링할 수 있다
- [ ] `[param]` 폴더명으로 동적 라우트를 만들 수 있다
- [ ] params prop이 Promise이므로 await가 필요함을 안다
- [ ] notFound() 함수로 404 페이지를 표시할 수 있다
- [ ] searchParams prop과 useSearchParams 훅의 차이를 안다
- [ ] Form 컴포넌트로 검색 기능을 구현할 수 있다

---

### 🔗 참고 자료

- *Learn React with TypeScript - Third Edition* (Carl Rippon)
- [Next.js Layouts and Pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages)
- [Next.js Link Component](https://nextjs.org/docs/app/api-reference/components/link)
- [Next.js useRouter](https://nextjs.org/docs/app/api-reference/functions/use-router)
- [Next.js Dynamic Routes](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes)
- [Next.js useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params)
- [MDN URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams)
