# Phase 1: Engage - Zustand 기초

## 준비 질문

### 질문 1: 클라이언트 상태 관리의 복잡성
```tsx
// Context API 방식
const ThemeContext = createContext()
const UserContext = createContext()
const SettingsContext = createContext()

// 중첩된 Provider
<ThemeContext.Provider>
  <UserContext.Provider>
    <SettingsContext.Provider>
      <App />
    </SettingsContext.Provider>
  </UserContext.Provider>
</ThemeContext.Provider>
```

**Q1**: Context API의 문제점은 무엇인가요?
- Provider 중첩? 불필요한 리렌더링? 셀렉터 부재?

### 질문 2: Zustand의 단순함
```tsx
import { create } from "zustand"

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// 사용
function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>{count}</button>
}
```

**Q2**: Zustand는 Provider가 필요 없는데, 어떻게 상태를 공유하나요?

### 질문 3: 셀렉터와 리렌더링
```tsx
const useStore = create((set) => ({
  user: { name: "Kim", age: 25 },
  theme: "dark",
  setTheme: (theme) => set({ theme }),
}))

// 방법 1: 전체 상태 구독
const { user, theme } = useStore()

// 방법 2: 셀렉터로 필요한 것만
const theme = useStore((state) => state.theme)
```

**Q3**: 두 방법의 리렌더링 차이는?

### 질문 4: Middleware
```tsx
import { create } from "zustand"
import { devtools, persist } from "zustand/middleware"

const useStore = create(
  devtools(
    persist(
      (set) => ({
        count: 0,
        increment: () => set((state) => ({ count: state.count + 1 })),
      }),
      { name: "counter-storage" }
    )
  )
)
```

**Q4**: persist middleware는 어디에 상태를 저장하나요?

---

## 답변 작성

### A1:

### A2:

### A3:

### A4:
