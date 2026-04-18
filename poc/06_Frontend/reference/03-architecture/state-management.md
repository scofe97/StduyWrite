# 상태 관리 (State Management)

## 개요

**정의**: 상태 관리는 애플리케이션의 데이터를 효율적으로 저장, 업데이트, 공유하는 체계적인 접근 방식이다.

**목적**: 컴포넌트 간 데이터 흐름을 예측 가능하게 만들고, 복잡한 UI 상태를 효과적으로 관리한다.

---

## 핵심 개념

### 상태의 6가지 유형

```
┌──────────────────────────────────────────────────────────┐
│                    React 상태 유형                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Server State ──── RSC 또는 TanStack Query              │
│   Form State ────── useActionState, React Hook Form      │
│   URL State ─────── 라우트/검색 파라미터                   │
│   Local State ───── useState, useReducer                 │
│   Derived State ─── 계산된 값 (useMemo)                   │
│   Shared State ──── Context, Zustand                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

| 상태 유형 | 설명 | 권장 관리 방법 |
|----------|------|----------------|
| **Server State** | 서버에서 가져온 데이터 | RSC, TanStack Query |
| **Form State** | 필드 값, 검증 에러, 제출 상태 | useActionState, React Hook Form |
| **URL State** | URL에 저장된 UI 상태 | 라우트/검색 파라미터 |
| **Local State** | 단일 컴포넌트 전용 상태 | useState, useReducer |
| **Derived State** | 다른 상태에서 계산된 값 | 직접 계산 또는 useMemo |
| **Shared State** | 여러 컴포넌트가 공유하는 상태 | Context, Zustand |

### 파생 상태 (Derived State)

```javascript
// 나쁜 예: 상태 중복 + useEffect 동기화
const [items, setItems] = useState([...]);
const [filteredItems, setFilteredItems] = useState([]);
useEffect(() => {
    setFilteredItems(items.filter(item => item.active));
}, [items]);

// 좋은 예: 파생 상태 (계산된 값)
const [items, setItems] = useState([...]);
const filteredItems = items.filter(item => item.active);

// 최적화: 비용이 큰 계산에만 useMemo 적용
const filteredItems = useMemo(() => {
    return items.filter(item => item.active);
}, [items]);
```

---

## 구현 패턴

### 1. Prop Drilling

**정의**: 상위 컴포넌트에서 하위 컴포넌트로 props를 순차적으로 전달

```
┌──────────────────────────────────────────────────────────┐
│                    Prop Drilling                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Home (state: userName, permissions)                    │
│       │                                                  │
│       ├── Header (props: userName) ✓ 사용               │
│       │                                                  │
│       └── Main (props: userName, permissions)            │
│               │                                          │
│               └── Content (props: permissions) ✓ 사용   │
│                                                          │
│   문제: Main은 permissions를 사용하지 않지만 전달해야 함  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

```javascript
// 상위 컴포넌트 - 상태 소유
function Home() {
    const [userName, setUserName] = useState();
    const [permissions, setPermissions] = useState();

    return (
        <>
            <Header userName={userName} />
            <Main userName={userName} permissions={permissions} />
        </>
    );
}

// 중간 컴포넌트 - permissions 사용 안 함
function Main({ userName, permissions }) {
    return (
        <main>
            <p>{userName ? `Hello ${userName}!` : 'Please sign in'}</p>
            <Content permissions={permissions} /> {/* 전달만 */}
        </main>
    );
}

// 하위 컴포넌트 - 실제 사용
function Content({ permissions }) {
    if (permissions?.includes('admin')) {
        return <p>Admin content</p>;
    }
    return <p>Insufficient permissions</p>;
}
```

#### Composition으로 개선

```javascript
// children을 사용하여 중간 컴포넌트 우회
function Main({ userName, children }) {
    return (
        <main>
            <p>{userName ? `Hello ${userName}!` : 'Please sign in'}</p>
            {children}
        </main>
    );
}

// Home에서 Content를 직접 전달
<Main userName={userName}>
    <Content permissions={permissions} />
</Main>
```

| 장점 | 단점 |
|------|------|
| 가장 단순한 방식 | 깊은 중첩 시 번거로움 |
| 데이터 흐름 추적 용이 | 중간 컴포넌트에 불필요한 props |
| 인접한 컴포넌트에 적합 | 리팩토링 어려움 |

---

### 2. React Context

**정의**: 컴포넌트 트리 전체에 데이터를 전달하는 React 내장 메커니즘

```
┌──────────────────────────────────────────────────────────┐
│                    React Context                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   UserProvider (Context Provider)                        │
│       │                                                  │
│       ├── Header ─────── use(UserContext)               │
│       │                                                  │
│       ├── Main ──────── use(UserContext)                │
│       │                                                  │
│       └── Content ───── use(UserContext)                │
│                                                          │
│   Prop Drilling 없이 어디서든 접근 가능                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### Context 생성 및 Provider

```typescript
// UserContext.ts
import { createContext } from 'react';

type UserState = {
    userName: string | undefined;
    permissions: string[] | undefined;
    loading: boolean;
    handleSignIn: () => Promise<void>;
    handleSignOut: () => Promise<void>;
};

export const UserContext = createContext<UserState>({
    userName: undefined,
    permissions: undefined,
    loading: false,
    handleSignIn: () => new Promise(() => {}),
    handleSignOut: () => new Promise(() => {}),
});

// UserProvider.tsx
'use client';

import { useState, useCallback, type ReactNode } from 'react';

export function UserProvider({ children }: { children: ReactNode }) {
    const [userName, setUserName] = useState<string>();
    const [permissions, setPermissions] = useState<string[]>();
    const [loading, setLoading] = useState(false);

    const handleSignIn = useCallback(async () => {
        setLoading(true);
        const user = await signIn();
        setUserName(user.name);
        setPermissions(user.permissions);
        setLoading(false);
    }, []);

    return (
        <UserContext value={{
            userName, permissions, loading,
            handleSignIn, handleSignOut
        }}>
            {children}
        </UserContext>
    );
}
```

#### Context 사용

```typescript
// Header.tsx
'use client';

import { use } from 'react';
import { UserContext } from '@/state/UserContext';

export function Header() {
    const { userName, handleSignIn, loading } = use(UserContext);

    return (
        <header>
            {userName ? (
                <span>{userName} has signed in</span>
            ) : (
                <button onClick={handleSignIn} disabled={loading}>
                    Sign in
                </button>
            )}
        </header>
    );
}
```

#### Context 리렌더링 문제

```
┌──────────────────────────────────────────────────────────┐
│              Context 리렌더링 문제                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   permissions 변경 시:                                   │
│                                                          │
│   Provider ──→ Header ✗ 리렌더 (불필요)                 │
│            ──→ Main   ✗ 리렌더 (불필요)                 │
│            ──→ Content ✓ 리렌더 (필요)                  │
│                                                          │
│   모든 Consumer가 리렌더됨 → 성능 문제 가능              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

| 장점 | 단점 |
|------|------|
| Prop Drilling 해결 | 모든 하위 컴포넌트 리렌더링 |
| React 내장 (번들 크기 0) | 최적화 어려움 |
| 전역 설정(테마, 로케일)에 적합 | 복잡한 상태에 부적합 |

---

### 3. Zustand

**정의**: 선택적 구독을 지원하는 경량 상태 관리 라이브러리

```
┌──────────────────────────────────────────────────────────┐
│                Zustand vs Context                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Context: 방송국 - 한 채널 변경 시 모든 TV에 신호       │
│   Zustand: 구독 서비스 - 구독한 채널만 알림 수신         │
│                                                          │
│   permissions 변경 시:                                   │
│                                                          │
│   Store ──✗─→ Header (userName 구독)    리렌더 안 함    │
│         ──✗─→ Main (userName 구독)      리렌더 안 함    │
│         ──✓─→ Content (permissions 구독) 리렌더!        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### Store 생성

```typescript
// useUserStore.ts
import { create } from 'zustand';

type UserState = {
    userName: string | undefined;
    permissions: string[] | undefined;
    loading: boolean;
    handleSignIn: () => Promise<void>;
    handleSignOut: () => Promise<void>;
};

export const useUserStore = create<UserState>((set) => ({
    userName: undefined,
    permissions: undefined,
    loading: false,

    handleSignIn: async () => {
        set({ loading: true });
        const user = await signIn();
        set({
            userName: user.name,
            permissions: user.permissions,
            loading: false,
        });
    },

    handleSignOut: async () => {
        set({ loading: true });
        await signOut();
        set({
            userName: undefined,
            permissions: undefined,
            loading: false,
        });
    },
}));
```

#### 선택적 구독

```typescript
// Header.tsx - Provider 불필요!
'use client';

import { useUserStore } from '@/state/useUserStore';

export function Header() {
    // 각 상태를 개별적으로 구독 → 해당 상태 변경 시에만 리렌더
    const userName = useUserStore((state) => state.userName);
    const loading = useUserStore((state) => state.loading);
    const handleSignIn = useUserStore((state) => state.handleSignIn);

    return (
        <header>
            {userName ? (
                <span>{userName}</span>
            ) : (
                <button onClick={handleSignIn} disabled={loading}>
                    Sign in
                </button>
            )}
        </header>
    );
}

// Content.tsx - permissions만 구독
export function Content() {
    const permissions = useUserStore((state) => state.permissions);
    // permissions가 변경될 때만 리렌더!

    if (permissions?.includes('admin')) {
        return <p>Admin content</p>;
    }
    return <p>Insufficient permissions</p>;
}
```

#### Zustand 미들웨어

```typescript
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';

const useStore = create(
    devtools(  // DevTools 연동
        persist(  // localStorage 영속화
            (set) => ({
                count: 0,
                inc: () => set((state) => ({ count: state.count + 1 })),
            }),
            { name: 'counter-storage' }
        )
    )
);
```

#### React Context vs Zustand

| 특성 | React Context | Zustand |
|------|---------------|---------|
| Provider 필요 | O | X |
| 설정 복잡도 | 중간 | 낮음 |
| 리렌더링 범위 | 모든 하위 컴포넌트 | 구독한 컴포넌트만 |
| 성능 | 낮음 (최적화 필요) | 높음 (기본 최적화) |
| 번들 크기 | 0 (React 내장) | ~2KB |

---

### 4. TanStack Query와 URL 파라미터

#### TanStack Query로 서버 상태 공유

```typescript
// 같은 queryKey로 캐시 공유
function useGetUser(userId: string | undefined) {
    return useQuery({
        queryKey: ['user', userId],
        queryFn: async () => {
            const response = await fetch(`/api/users/${userId}`);
            return response.json();
        },
        enabled: userId !== undefined,
    });
}

// Header.tsx
export function Header() {
    const { data: user } = useGetUser(userId);
    return <span>{user?.name}</span>;
}

// Main.tsx - 같은 키로 캐시된 데이터 사용
export function Main() {
    const { data: user } = useGetUser(userId);
    return <p>Hello {user?.name}!</p>;
}
```

#### URL 파라미터로 UI 상태 공유

```typescript
// Tab.tsx - URL로 활성 탭 관리
'use client';

import { useSearchParams, useRouter } from 'next/navigation';

export function Tab({ name, label }: { name: string; label: string }) {
    const params = useSearchParams();
    const activeTab = params.get('tab') ?? 'address';
    const router = useRouter();

    return (
        <button
            className={activeTab === name ? 'active' : ''}
            onClick={() => router.push(`/?tab=${name}`)}
        >
            {label}
        </button>
    );
}
```

**URL 상태의 장점**:
- 공유 가능: URL 공유로 동일한 UI 상태
- 북마크 가능: 특정 상태 저장
- 뒤로가기 지원: 브라우저 히스토리 통합
- SSR 친화적: 서버에서 초기 상태 접근

---

## 트레이드오프

### 상태 관리 선택 가이드

| 상황 | 권장 방식 |
|------|-----------|
| 2-3개 인접 컴포넌트 간 공유 | Prop Drilling |
| 테마, 로케일 등 앱 전역 설정 | React Context |
| 복잡한 클라이언트 상태, 성능 중요 | Zustand |
| 서버 데이터 공유 | TanStack Query |
| 필터, 정렬, 탭 등 UI 상태 | URL 파라미터 |
| 폼 상태 | useActionState, React Hook Form |

### 주의사항

- 과도한 전역 상태: 로컬로 충분한 상태를 전역으로 올리면 복잡도 증가
- Context 리렌더 무시: 성능 문제 발생 시 Zustand나 상태 분리 고려
- URL 상태와 React 상태 중복: 동기화 로직이 복잡해지므로 하나만 사용
- 파생 상태를 useState로 관리: useEffect 동기화 대신 직접 계산

---

## 면접 포인트

**Q**: Prop Drilling의 장단점은?

**A**: 장점은 단순함과 데이터 흐름 추적 용이성이다. 단점은 깊은 중첩 시 번거롭고 중간 컴포넌트에 불필요한 props가 전달되는 것이다. 2-3단계 이내에서는 가장 권장되는 방식이다.

**Q**: React Context의 리렌더링 문제와 해결 방법은?

**A**: Context value가 변경되면 모든 Consumer 컴포넌트가 리렌더된다. 해결 방법은 상태 분리(여러 Context), useMemo로 value 메모이제이션, 또는 Zustand 같은 선택적 구독 라이브러리 사용이다.

**Q**: Zustand가 Context보다 성능이 좋은 이유는?

**A**: Zustand는 selector 함수로 구독할 상태를 지정하여, 해당 상태가 변경될 때만 컴포넌트가 리렌더된다. Context는 value 전체가 변경되면 모든 Consumer가 리렌더되는 반면, Zustand는 세밀한 구독 제어가 가능하다.

**Q**: 파생 상태(Derived State)란 무엇이고 왜 사용하나요?

**A**: 다른 상태에서 계산된 값이다. 별도 상태로 관리하면 동기화 로직(useEffect)이 필요하고 버그 위험이 있다. 직접 계산하면 코드가 단순해지고 항상 최신 값이 보장된다.

---

## 참고 자료

- [React Context 공식 문서](https://react.dev/reference/react/createContext)
- [Zustand 공식 문서](https://zustand.docs.pmnd.rs/)
- [TanStack Query 공식 문서](https://tanstack.com/query/latest)
- [Next.js useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params)
