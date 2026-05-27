# Phase 1: Engage - TypeScript 패턴 기초

## 준비 질문

### 질문 1: 제네릭
```tsx
// 제네릭 없이
function getFirst(arr: number[]): number { return arr[0] }
function getFirstStr(arr: string[]): string { return arr[0] }

// 제네릭 사용
function getFirst<T>(arr: T[]): T { return arr[0] }
```

**Q1**: 제네릭의 핵심 이점은 무엇인가요?

### 질문 2: 유틸리티 타입
```tsx
interface User {
  id: string
  name: string
  email: string
  createdAt: Date
}

// 어떤 타입이 될까요?
type CreateUserInput = Omit<User, "id" | "createdAt">
type UpdateUserInput = Partial<User>
type UserPreview = Pick<User, "id" | "name">
```

**Q2**: 각 유틸리티 타입의 결과는?

### 질문 3: Discriminated Unions
```tsx
type ApiResponse<T> =
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string }

function handleResponse(response: ApiResponse<User>) {
  if (response.status === "success") {
    // 여기서 response.data의 타입은?
  }
}
```

**Q3**: 왜 `status` 필드로 타입을 구분할 수 있나요?

### 질문 4: as const
```tsx
const PROVIDERS = ["github", "gitlab", "bitbucket"] as const

type Provider = typeof PROVIDERS[number]

// vs
const PROVIDERS2 = ["github", "gitlab", "bitbucket"]
type Provider2 = typeof PROVIDERS2[number]  // string
```

**Q4**: `as const`가 타입에 미치는 영향은?

---

## 답변 작성

### A1:

### A2:

### A3:

### A4:
