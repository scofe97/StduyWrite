# Phase 2: Investigate - TypeScript 패턴 실험

## 실험 과제

### 실험 1: 제네릭 함수와 컴포넌트

```tsx
// src/experiments/generics.ts

// 제네릭 함수
function identity<T>(arg: T): T {
  return arg
}

// 타입 추론 확인
const num = identity(42)        // number로 추론?
const str = identity("hello")   // string으로 추론?
const obj = identity({ a: 1 })  // { a: number }로 추론?

// 제네릭 제약
interface Lengthwise {
  length: number
}

function logLength<T extends Lengthwise>(arg: T): T {
  console.log(arg.length)
  return arg
}

logLength("hello")     // OK - string has length
logLength([1, 2, 3])   // OK - array has length
// logLength(123)      // Error - number has no length

// 제네릭 컴포넌트
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
  keyExtractor: (item: T) => string
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  )
}

// 사용
interface User { id: string; name: string }
const users: User[] = [{ id: "1", name: "Kim" }]

<List<User>
  items={users}
  renderItem={(user) => user.name}  // user는 User 타입으로 추론
  keyExtractor={(user) => user.id}
/>
```

**관찰할 것**:
- [ ] 각 identity 호출의 반환 타입
- [ ] extends로 제네릭 제약
- [ ] 컴포넌트에서 제네릭 사용

### 실험 2: 유틸리티 타입

```tsx
// src/experiments/utility-types.ts

interface User {
  id: string
  name: string
  email: string
  password: string
  createdAt: Date
  updatedAt: Date
}

// Pick: 특정 프로퍼티만 선택
type UserPublic = Pick<User, "id" | "name" | "email">
// 결과: { id: string; name: string; email: string }

// Omit: 특정 프로퍼티 제외
type UserWithoutDates = Omit<User, "createdAt" | "updatedAt">
// 결과: { id: string; name: string; email: string; password: string }

// Partial: 모든 프로퍼티를 선택적으로
type UserUpdate = Partial<User>
// 결과: { id?: string; name?: string; ... }

// Required: 모든 프로퍼티를 필수로
type UserRequired = Required<Partial<User>>
// 결과: 다시 모든 프로퍼티가 필수

// Readonly: 모든 프로퍼티를 읽기 전용으로
type ReadonlyUser = Readonly<User>
// const user: ReadonlyUser = { ... }
// user.name = "new"  // Error!

// Record: 키-값 매핑 타입
type Provider = "github" | "gitlab" | "bitbucket"
type ProviderConfig = Record<Provider, { apiUrl: string; token: string }>
// 결과: { github: {...}; gitlab: {...}; bitbucket: {...} }

// 조합 사용
type CreateUserInput = Omit<User, "id" | "createdAt" | "updatedAt">
type UpdateUserInput = Partial<Omit<User, "id" | "createdAt" | "updatedAt">>
```

**관찰할 것**:
- [ ] 각 유틸리티 타입의 결과
- [ ] 유틸리티 타입 조합
- [ ] IDE에서 타입 정보 확인 (hover)

### 실험 3: Discriminated Unions

```tsx
// src/experiments/discriminated-unions.ts

// 상태 기반 타입
type LoadingState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string }

// 타입 가드
function handleState<T>(state: LoadingState<T>) {
  switch (state.status) {
    case "idle":
      // state.data  // Error: property 'data' does not exist
      return "Ready to load"

    case "loading":
      return "Loading..."

    case "success":
      // state.data exists and is T
      return `Data: ${state.data}`

    case "error":
      // state.error exists
      return `Error: ${state.error}`

    default:
      // exhaustiveness check
      const _exhaustive: never = state
      return _exhaustive
  }
}

// API 응답 예제
interface Repository { id: string; name: string }

type RepositoryState = LoadingState<Repository[]>

function RepositoryList({ state }: { state: RepositoryState }) {
  if (state.status === "loading") {
    return <div>Loading...</div>
  }

  if (state.status === "error") {
    return <div>Error: {state.error}</div>
  }

  if (state.status === "success") {
    return (
      <ul>
        {state.data.map((repo) => (
          <li key={repo.id}>{repo.name}</li>
        ))}
      </ul>
    )
  }

  return <div>Click to load</div>
}
```

**관찰할 것**:
- [ ] status 필드에 따른 타입 좁히기
- [ ] 각 분기에서 접근 가능한 프로퍼티
- [ ] never를 사용한 exhaustiveness check

### 실험 4: 타입 좁히기와 가드

```tsx
// src/experiments/type-narrowing.ts

// typeof 가드
function processValue(value: string | number) {
  if (typeof value === "string") {
    // value는 string
    return value.toUpperCase()
  }
  // value는 number
  return value.toFixed(2)
}

// in 연산자 가드
interface Bird { fly(): void }
interface Fish { swim(): void }

function move(animal: Bird | Fish) {
  if ("fly" in animal) {
    animal.fly()
  } else {
    animal.swim()
  }
}

// instanceof 가드
class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message)
  }
}

function handleError(error: Error) {
  if (error instanceof ApiError) {
    // error는 ApiError
    console.log(`API Error ${error.statusCode}: ${error.message}`)
  } else {
    // 일반 Error
    console.log(`Error: ${error.message}`)
  }
}

// 커스텀 타입 가드
function isString(value: unknown): value is string {
  return typeof value === "string"
}

function process(value: unknown) {
  if (isString(value)) {
    // value는 string으로 좁혀짐
    console.log(value.length)
  }
}

// Array 타입 가드
function isArrayOfStrings(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string")
}
```

**관찰할 것**:
- [ ] 각 가드 이후 타입 변화
- [ ] value is Type 반환 타입의 의미
- [ ] unknown과 타입 가드 조합

---

## 실험 결과 기록

### 실험 1 결과:

### 실험 2 결과:

### 실험 3 결과:

### 실험 4 결과:
